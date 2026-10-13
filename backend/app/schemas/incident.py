from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class EvidenceItem(BaseModel):
    evidence_id: str
    type: str
    description: str
    source_event_ids: List[str]
    source_edge_ids: Optional[List[str]] = None
    strength: str

class MitreMapping(BaseModel):
    technique_id: Optional[str]
    technique_name: Optional[str]
    tactic: Optional[str]
    evidence: str
    confidence: str
    source_event_ids: List[str]

class IncidentEvent(BaseModel):
    event_id: str
    source_ip: str
    destination_ip: str
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    protocol: str
    supervised_score: float
    anomaly_score: float
    detection_source: str
    timestamp: Optional[float] = None
    timestamp_source: Optional[str] = None

class StructuredIncident(BaseModel):
    incident_id: str
    event_count: int
    events: List[IncidentEvent]
    edges: List[Dict[str, Any]]
    correlation_score: float
    detection_summary: Dict[str, Any]
    mitre_mappings: List[MitreMapping]
    evidence_items: List[EvidenceItem]
    confidence: str
    timestamp_source: Optional[str]
    limitations: List[str]
    scenario_id: Optional[str] = None
    execution_mode: Optional[str] = "CONTROLLED_REPLAY"
    source_dataset: Optional[str] = None

class LLMExplanation(BaseModel):
    model_config = {"protected_namespaces": ()}

    summary: str
    attack_chain: str
    evidence: str
    mitre_techniques: str
    confidence: str
    limitations: str
    investigation_recommendations: str
    scenario_id: Optional[str] = "TC-10"
    incident_id: Optional[str] = "INC_1"
    provider: str = "deterministic"
    fallback_used: bool = False
    model_name: Optional[str] = None
