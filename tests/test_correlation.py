import pytest
import networkx as nx
from app.services.correlation import CorrelationEngine

@pytest.fixture
def correlation_engine():
    return CorrelationEngine(temporal_window=30.0, edge_threshold=1.0)

def test_same_source_ip_weak_relationship(correlation_engine):
    # Only share source IP -> Weak (0.4). Edge should not be formed.
    events = [
        {"event_id": "1", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2"},
        {"event_id": "2", "source_ip": "1.1.1.1", "destination_ip": "3.3.3.3"}
    ]
    G = correlation_engine.correlate(events)
    assert G.number_of_edges() == 0

def test_strong_multi_signal_relationship(correlation_engine):
    # Share source, dest, and port -> Same Src/Dst (0.6) + Same Port (0.3) + Agreement (0.2) = 1.1 >= 1.0 (MEDIUM)
    events = [
        {"event_id": "1", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2", "destination_port": 80, "detection_source": "BOTH"},
        {"event_id": "2", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2", "destination_port": 80, "detection_source": "BOTH"}
    ]
    G = correlation_engine.correlate(events)
    assert G.number_of_edges() == 1
    edge_data = G.get_edge_data("1", "2")
    assert edge_data["evidence_strength"] in ["MEDIUM", "STRONG"]

def test_temporal_correlation(correlation_engine):
    # temporal (0.6) + same source (0.2) + same dest (0.2) = 1.0 >= 1.0 -> MEDIUM
    events = [
        {"event_id": "1", "timestamp": 1000.0, "timestamp_source": "DEMO_REPLAY", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2"},
        {"event_id": "2", "timestamp": 1025.0, "timestamp_source": "DEMO_REPLAY", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2"}
    ]
    G = correlation_engine.correlate(events)
    assert G.number_of_edges() == 1

def test_temporal_boundary(correlation_engine):
    # same source and dest (0.6), but outside temporal window -> 0.6 < 1.0 -> NO EDGE
    events = [
        {"event_id": "1", "timestamp": 1000.0, "timestamp_source": "DEMO_REPLAY", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2"},
        {"event_id": "2", "timestamp": 1031.0, "timestamp_source": "DEMO_REPLAY", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2"}
    ]
    G = correlation_engine.correlate(events)
    assert G.number_of_edges() == 0

def test_unrelated_noise_remains_separate(correlation_engine):
    events = [
        {"event_id": "1", "timestamp": 1000.0, "timestamp_source": "DEMO_REPLAY", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2"},
        {"event_id": "2", "timestamp": 1005.0, "timestamp_source": "DEMO_REPLAY", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2"},
        {"event_id": "NOISE", "timestamp": 1002.0, "timestamp_source": "DEMO_REPLAY", "source_ip": "9.9.9.9", "destination_ip": "8.8.8.8"}
    ]
    G = correlation_engine.correlate(events)
    # The noise event shouldn't connect to 1 or 2 because temporal alone (0.6) < 1.0
    assert G.degree("NOISE") == 0

def test_graph_edge_evidence(correlation_engine):
    events = [
        {"event_id": "1", "timestamp": 1000.0, "timestamp_source": "DEMO_REPLAY", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2", "detection_source": "BOTH"},
        {"event_id": "2", "timestamp": 1005.0, "timestamp_source": "DEMO_REPLAY", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2", "detection_source": "BOTH"}
    ]
    G = correlation_engine.correlate(events)
    reasons = G.get_edge_data("1", "2")["reasons"]
    types = [r["edge_type"] for r in reasons]
    assert "TEMPORAL" in types
    assert "SAME_SRC_AND_DST" in types

def test_large_repeated_source_group_does_not_explode(correlation_engine):
    # 500 events sharing only a source IP
    events = [{"event_id": str(i), "source_ip": "1.1.1.1", "destination_ip": f"2.2.2.{i}"} for i in range(500)]
    G = correlation_engine.correlate(events)
    # Since Same Source IP is 0.2 < 1.0, NO edges should be formed, bounded generation handles this fast.
    assert G.number_of_edges() == 0

def test_deterministic_clustering(correlation_engine):
    events = [
        {"event_id": "1", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2", "destination_port": 80, "detection_source": "BOTH"},
        {"event_id": "2", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2", "destination_port": 80, "detection_source": "BOTH"},
        {"event_id": "3", "source_ip": "8.8.8.8", "destination_ip": "9.9.9.9", "destination_port": 443, "detection_source": "BOTH"},
        {"event_id": "4", "source_ip": "8.8.8.8", "destination_ip": "9.9.9.9", "destination_port": 443, "detection_source": "BOTH"}
    ]
    G = correlation_engine.correlate(events)
    incidents = correlation_engine.get_candidate_incidents(G)
    assert len(incidents) == 2
