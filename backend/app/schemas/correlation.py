from pydantic import BaseModel, Field
from typing import List

class CorrelatedCampaign(BaseModel):
    """
    Contract for the correlation engine output.
    Groups suspicious events into a cohesive campaign.
    """
    campaign_id: str = Field(..., description="Unique identifier for the correlated campaign")
    event_ids: List[str] = Field(..., description="List of event IDs belonging to this campaign")
    start_time: float = Field(..., description="Timestamp of the first event in the campaign")
    end_time: float = Field(..., description="Timestamp of the last event in the campaign")
    involved_entities: List[str] = Field(..., description="IPs, hosts, or users involved in the campaign")
    confidence_score: float = Field(..., description="Confidence that this represents a true attack chain")
    suggested_mitre_tactics: List[str] = Field(default_factory=list, description="Mapped MITRE ATT&CK tactics")
