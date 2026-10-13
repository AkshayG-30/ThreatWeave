from pydantic import BaseModel, Field

class IntegratedDetectorOutput(BaseModel):
    """
    Contract for integrated detector output. Every analysis result must produce this format.
    """
    event_id: str = Field(..., description="Identifier of the analyzed event")
    supervised_prediction: str = Field(..., description="Prediction result: 'attack' or 'benign'")
    supervised_score: float = Field(..., description="Probability or confidence score of supervised prediction")
    anomaly_prediction: str = Field(..., description="Prediction result: 'anomaly' or 'normal'")
    anomaly_score: float = Field(..., description="Continuous anomaly score (higher = more anomalous)")
    detection_source: str = Field(..., description="Source of detection: SUPERVISED, ANOMALY, BOTH, NONE")
