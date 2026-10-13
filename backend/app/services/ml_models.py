"""
ML Architecture Implementation Interfaces
"""
from app.schemas.detector import DetectorOutput, AnomalyDetectorOutput
from app.schemas.event import CanonicalEvent

class SupervisedModel:
    def __init__(self, model_type: str = "xgboost"):
        self.model_type = model_type
        self.is_trained = False
        # self.model = None

    def train(self, X, y):
        """Trains the supervised model."""
        pass

    def predict(self, event: CanonicalEvent) -> DetectorOutput:
        """
        Predicts if a canonical event is an attack.
        Returns DetectorOutput contract.
        """
        if not self.is_trained:
            raise RuntimeError("Model is not trained yet.")
        # Inference logic here
        pass

class AnomalyDetector:
    def __init__(self, model_type: str = "isolation_forest"):
        self.model_type = model_type
        self.is_trained = False

    def train(self, X):
        """Trains the unsupervised model on ostensibly normal data."""
        pass

    def predict(self, event: CanonicalEvent) -> AnomalyDetectorOutput:
        """
        Calculates anomaly score for an event.
        Returns AnomalyDetectorOutput contract.
        """
        if not self.is_trained:
            raise RuntimeError("Model is not trained yet.")
        # Inference logic here
        pass
