import pytest
from app.services.mitre_mapper import MitreMapper
from app.services.llm_explainer import LLMExplainer
from app.schemas.incident import StructuredIncident, IncidentEvent, MitreMapping, EvidenceItem

@pytest.fixture
def empty_incident():
    return StructuredIncident(
        incident_id="INC_001",
        event_count=0,
        events=[],
        edges=[],
        correlation_score=0.0,
        detection_summary={},
        mitre_mappings=[],
        evidence_items=[],
        confidence="LOW",
        timestamp_source=None,
        limitations=["No events"]
    )

def test_mitre_mapping_null():
    mapper = MitreMapper()
    events = [{"event_id": "EV_01_NOISE"}]
    edges = []
    mappings = mapper.map_incident(events, edges)
    assert len(mappings) == 1
    assert mappings[0].technique_id is None

def test_mitre_mapping_recon():
    mapper = MitreMapper()
    events = [{"event_id": "EV_01_RECON"}, {"event_id": "EV_02_RECON"}]
    edges = []
    mappings = mapper.map_incident(events, edges)
    assert any(m.technique_id == "T1046" for m in mappings)

def test_llm_fallback(empty_incident):
    # Ensure fallback works when API key is missing or invalid
    explainer = LLMExplainer()
    # Force client to None to test deterministic fallback
    explainer.client = None
    
    explanation = explainer.explain(empty_incident)
    assert "Deterministic fallback explanation" in explanation.limitations
    
def test_llm_no_hallucination_timestamps(empty_incident):
    explainer = LLMExplainer()
    explainer.client = None
    # If no timestamps exist in the structured incident, the fallback must not invent them
    explanation = explainer.explain(empty_incident)
    assert "2024" not in explanation.attack_chain

def test_incident_schema_validates():
    ev = IncidentEvent(
        event_id="EV",
        source_ip="1.1.1.1",
        destination_ip="2.2.2.2",
        protocol="TCP",
        supervised_score=0.9,
        anomaly_score=0.1,
        detection_source="SUPERVISED"
    )
    assert ev.source_ip == "1.1.1.1"
