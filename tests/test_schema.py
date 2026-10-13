from app.schemas.event import CanonicalEvent
from app.schemas.detector import IntegratedDetectorOutput
from app.schemas.incident import StructuredIncident

def test_canonical_event_schema():
    event = CanonicalEvent(
        event_id="test_1",
        timestamp=1690000000.0,
        source_ip="192.168.1.10",
        event_type="flow",
        label=0
    )
    assert event.event_id == "test_1"
    assert event.label == 0

def test_detector_output_schema():
    out = IntegratedDetectorOutput(
        event_id="test_1",
        supervised_prediction="attack",
        supervised_score=0.95,
        anomaly_prediction="anomaly",
        anomaly_score=0.90,
        detection_source="BOTH"
    )
    assert out.supervised_prediction == "attack"
    assert out.detection_source == "BOTH"

