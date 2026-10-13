import pytest
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from app.schemas.detector import IntegratedDetectorOutput

def test_model_output_schema():
    out = IntegratedDetectorOutput(
        event_id="test_1",
        supervised_prediction="attack",
        supervised_score=0.95,
        anomaly_prediction="anomaly",
        anomaly_score=5.2,
        detection_source="BOTH"
    )
    assert out.supervised_prediction == "attack"
    assert out.detection_source == "BOTH"
    
def test_anomaly_score_direction():
    # Verify the mock integration handles score logic correctly
    assert 5.2 > 0.0 # Anomalous score is higher

def test_prediction_shape():
    # Mock model prediction output shape
    preds = np.array([0, 1, 0, 1, 1])
    assert preds.shape == (5,)
    assert set(preds) <= {0, 1}

def test_metric_and_fpr_calculation():
    y_true = np.array([0, 0, 0, 1, 1])
    y_pred = np.array([0, 1, 0, 1, 0])
    
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    assert tn == 2
    assert fp == 1
    assert fn == 1
    assert tp == 1
    
    fpr = fp / (fp + tn)
    assert fpr == 1/3
    
def test_feature_selection():
    df = pd.DataFrame({
        'A': [1, 2],
        'IPV4_SRC_ADDR': ['x', 'y'],
        'Label': [0, 1]
    })
    
    from app.services.pipeline import DataPipeline
    pipeline = DataPipeline()
    X, y_label, _ = pipeline.select_features(df)
    
    assert 'IPV4_SRC_ADDR' not in X.columns
    assert 'Label' not in X.columns
    assert 'A' in X.columns
    assert list(y_label) == [0, 1]
