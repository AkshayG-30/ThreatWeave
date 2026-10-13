import os
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.llm_explainer import LLMExplainer
from app.schemas.incident import StructuredIncident

client = TestClient(app)

def test_explanation_default_backward_compatible():
    """Verify endpoint without scenario_id defaults safely to TC-10."""
    response = client.get("/api/demo/explanation")
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_id"] == "TC-10"
    assert data["incident_id"] == "INC_1"
    assert data["provider"] in ["groq", "deterministic"]
    assert isinstance(data["fallback_used"], bool)
    assert len(data["summary"]) > 0
    assert len(data["attack_chain"]) > 0

def test_explanation_explicit_scenario_tc10():
    """Verify explicit scenario_id=TC-10 returns the verified TC-10 explanation."""
    response = client.get("/api/demo/explanation?scenario_id=TC-10")
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_id"] == "TC-10"
    assert data["incident_id"] == "INC_1"

def test_explanation_unsupported_scenario_fails_explicitly():
    """Verify uncatalogued or unavailable scenarios fail explicitly with 404."""
    response = client.get("/api/demo/explanation?scenario_id=TC-05")
    assert response.status_code == 404
    assert "disabled" in response.json()["detail"].lower()

    response_nonexistent = client.get("/api/demo/explanation?scenario_id=NONEXISTENT_999")
    assert response_nonexistent.status_code == 404

def test_explanation_path_traversal_rejected():
    """Verify attempts with path traversal or illegal characters are rejected with 400."""
    response = client.get("/api/demo/explanation?scenario_id=../../secrets")
    assert response.status_code == 400
    assert "invalid scenario identifier format" in response.json()["detail"].lower()

    response_shell = client.get("/api/demo/explanation?scenario_id=TC-10;cat")
    assert response_shell.status_code == 400

def test_explanation_no_secret_leakage():
    """Verify that Groq API keys or environment secrets are never returned in response."""
    response = client.get("/api/demo/explanation?scenario_id=TC-10")
    assert response.status_code == 200
    raw_text = response.text
    assert "gsk_" not in raw_text
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        assert groq_key not in raw_text

def test_deterministic_fallback_fidelity():
    """Verify deterministic fallback produces grounded explanation with no hallucinated event IDs."""
    with open("backend/app/cache/TC-10.json", "r") as f:
        cache_data = json.load(f)
    incident = StructuredIncident(**cache_data)

    explainer = LLMExplainer()
    explainer.client = None # Force deterministic fallback

    result = explainer.explain(incident, scenario_id="TC-10")
    assert result.provider == "deterministic"
    assert result.fallback_used is True
    assert result.scenario_id == "TC-10"
    assert result.incident_id == "INC_1"
    assert "Deterministic fallback explanation" in result.limitations

    # Verify event chain strictly contains existing event IDs
    incident_event_ids = {e.event_id for e in incident.events}
    for ev_id in incident_event_ids:
        assert ev_id in result.attack_chain

def test_cross_dataset_provenance_verification():
    """Verify physical artifact for cross-dataset evaluation proves NF-CSE-CIC-IDS2018-V2."""
    config_path = "experiments/cross_dataset_real/config.json"
    assert os.path.exists(config_path), "Cross-dataset config must exist"
    with open(config_path, "r") as f:
        cfg = json.load(f)
    assert cfg["target_dataset"] == "Real NF-CSE-CIC-IDS2018-V2"
    assert cfg["rows_processed"] == 17129715
