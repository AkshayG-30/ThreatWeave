"""Phase 12E: Verified Scenario Implementation Test Suite.

Validates that all supported scenarios (TC-01..TC-04, TC-06..TC-10) conform to the
StructuredIncident data contract, derive from verified dataset/model inference or
recorded evaluation artifacts, that TC-05 is safely and explicitly disabled, and that
the explanation engine accurately services all enabled scenarios.
"""
import os
import json
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.incident import StructuredIncident
from app.services.llm_explainer import LLMExplainer

client = TestClient(app)

ENABLED_SCENARIOS = ["TC-01", "TC-02", "TC-03", "TC-04", "TC-06", "TC-07", "TC-08", "TC-09", "TC-10"]
LIVE_INFERENCE_SCENARIOS = ["TC-01", "TC-02", "TC-03", "TC-04", "TC-06", "TC-07"]
RECORDED_EVAL_SCENARIOS = ["TC-08", "TC-09"]
CONTROLLED_REPLAY_SCENARIOS = ["TC-10"]


def test_catalogue_contains_ten_scenarios():
    """Verify scenario catalogue returns exactly 10 scenarios with valid flags."""
    response = client.get("/api/demo/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    scenario_ids = [s.get("id") or s.get("scenario_id") for s in data]
    expected_ids = [f"TC-{i:02d}" for i in range(1, 11)]
    assert scenario_ids == expected_ids

    tc05 = next(s for s in data if (s.get("id") or s.get("scenario_id")) == "TC-05")
    assert tc05["is_executable"] is False
    assert tc05["status"] in ["EXPERIMENTAL ARTIFACT PRESENT", "DISABLED"]

    for sid in ENABLED_SCENARIOS:
        entry = next(s for s in data if (s.get("id") or s.get("scenario_id")) == sid)
        assert entry["is_executable"] is True
        assert entry["status"] in ["VERIFIED", "GROUNDED BENCHMARK"]


def test_live_inference_scenarios_contract():
    """Verify live inference scenarios return valid StructuredIncident with LIVE_INFERENCE mode."""
    for sid in LIVE_INFERENCE_SCENARIOS:
        response = client.get(f"/api/demo/scenario/{sid}")
        assert response.status_code == 200, f"Scenario {sid} failed"
        data = response.json()
        incident = StructuredIncident(**data)
        assert incident.scenario_id == sid
        assert incident.execution_mode == "LIVE_INFERENCE"
        assert "NF-UNSW-NB15-v2" in incident.source_dataset
        assert len(incident.events) > 0
        assert incident.correlation_score >= 0.0


def test_tc01_benign_traffic_behavior():
    """Verify TC-01 benign traffic has low correlation, 0 edges, and 0 MITRE techniques."""
    response = client.get("/api/demo/scenario/TC-01")
    assert response.status_code == 200
    data = response.json()
    incident = StructuredIncident(**data)
    assert incident.correlation_score < 0.2
    assert len(incident.edges) == 0
    assert len(incident.mitre_mappings) == 0
    for ev in incident.events:
        assert ev.detection_source == "NONE"
        assert ev.supervised_score < 0.5


def test_tc06_consensus_detection_source():
    """Verify TC-06 consensus detection events all have detection_source == 'BOTH'."""
    response = client.get("/api/demo/scenario/TC-06")
    assert response.status_code == 200
    data = response.json()
    incident = StructuredIncident(**data)
    assert len(incident.events) > 0
    for ev in incident.events:
        assert ev.detection_source == "BOTH"


def test_tc07_detector_disagreement_sources():
    """Verify TC-07 includes both SUPERVISED-only and ANOMALY-only detection events."""
    response = client.get("/api/demo/scenario/TC-07")
    assert response.status_code == 200
    data = response.json()
    incident = StructuredIncident(**data)
    sources = {ev.detection_source for ev in incident.events}
    assert "SUPERVISED" in sources
    assert "ANOMALY" in sources


def test_recorded_evaluation_scenarios_contract():
    """Verify TC-08 and TC-09 return RECORDED_EVALUATION mode and correct dataset provenance."""
    for sid in RECORDED_EVAL_SCENARIOS:
        response = client.get(f"/api/demo/scenario/{sid}")
        assert response.status_code == 200, f"Recorded scenario {sid} failed"
        data = response.json()
        incident = StructuredIncident(**data)
        assert incident.scenario_id == sid
        assert incident.execution_mode == "RECORDED_EVALUATION"
        assert "NF-UNSW-NB15-v2" in incident.source_dataset
        assert len(incident.events) > 0


def test_controlled_replay_tc10_preserved():
    """Verify TC-10 multi-stage incident preserves original baseline structure."""
    response = client.get("/api/demo/scenario/TC-10")
    assert response.status_code == 200
    data = response.json()
    incident = StructuredIncident(**data)
    assert incident.scenario_id == "TC-10"
    assert incident.incident_id == "INC_1"
    assert incident.execution_mode == "CONTROLLED_REPLAY"
    assert len(incident.events) == 8
    assert len(incident.edges) == 20
    assert len(incident.mitre_mappings) >= 3


def test_tc05_autoencoder_explicitly_disabled():
    """Verify TC-05 execution is blocked with HTTP 404 and clear explanation of missing weights."""
    response = client.get("/api/demo/scenario/TC-05")
    assert response.status_code == 404
    detail = response.json()["detail"]
    assert "disabled" in detail.lower()
    assert "autoencoder" in detail.lower()


def test_explanation_works_for_all_enabled_scenarios(monkeypatch):
    """Verify /api/demo/explanation produces valid explanations for all enabled scenarios."""
    # Force deterministic fallback so test runs instantaneously and is offline-capable
    monkeypatch.setattr(LLMExplainer, "__init__", lambda self: setattr(self, "client", None))
    for sid in ENABLED_SCENARIOS:
        response = client.get(f"/api/demo/explanation?scenario_id={sid}")
        assert response.status_code == 200, f"Explanation failed for {sid}: {response.text}"
        data = response.json()
        assert data["scenario_id"] == sid
        assert len(data["summary"]) > 0
        assert data["provider"] == "deterministic"
        assert data["fallback_used"] is True


def test_explanation_tc05_disabled():
    """Verify explanation endpoint also rejects TC-05 with HTTP 404."""
    response = client.get("/api/demo/explanation?scenario_id=TC-05")
    assert response.status_code == 404
    detail = response.json()["detail"]
    assert "disabled" in detail.lower()
    assert "autoencoder" in detail.lower()
