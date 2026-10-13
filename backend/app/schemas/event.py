from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class CanonicalEvent(BaseModel):
    """
    Canonical internal event representation for ThreatWeave.
    Different datasets are mapped to this schema after preprocessing.
    """
    event_id: str = Field(..., description="Unique identifier for the event")
    timestamp: float = Field(..., description="Epoch timestamp of the event")
    source_ip: Optional[str] = Field(None, description="Source IP address")
    destination_ip: Optional[str] = Field(None, description="Destination IP address")
    source_port: Optional[int] = Field(None, description="Source port")
    destination_port: Optional[int] = Field(None, description="Destination port")
    protocol: Optional[str] = Field(None, description="Network protocol (e.g., TCP, UDP)")
    
    # Host and user context (often null for purely network-based datasets)
    host: Optional[str] = Field(None, description="Hostname involved in the event")
    user: Optional[str] = Field(None, description="Username associated with the event")
    process: Optional[str] = Field(None, description="Process name or ID")
    
    event_type: str = Field(..., description="Type of event (e.g., flow, log, alert)")
    
    # Ground truth (if available)
    label: Optional[int] = Field(None, description="Ground truth label: 0 for benign, 1 for malicious")
    attack_type: Optional[str] = Field(None, description="Specific attack class if malicious")
    
    # Model scores (populated during inference)
    supervised_score: Optional[float] = Field(None, description="Probability of attack from supervised model")
    anomaly_score: Optional[float] = Field(None, description="Anomaly score from unsupervised model")
    
    detection_source: Optional[str] = Field(None, description="Name of the detector that flagged this event")
    
    # Preserve original data to prevent information loss
    original_data: Optional[Dict[str, Any]] = Field(None, description="Original raw event fields")

