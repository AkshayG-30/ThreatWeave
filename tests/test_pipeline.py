import pytest
import pandas as pd
import numpy as np
from app.services.pipeline import DataPipeline

@pytest.fixture
def mock_raw_data():
    return pd.DataFrame({
        'IPV4_SRC_ADDR': ['192.168.1.1', '10.0.0.1', '172.16.0.1'],
        'IPV4_DST_ADDR': ['8.8.8.8', '8.8.4.4', '1.1.1.1'],
        'L4_SRC_PORT': [1024, 2048, 4096],
        'L4_DST_PORT': [80, 443, 53],
        'PROTOCOL': [6, 6, 17],
        'IN_BYTES': [500, 1000, np.nan], # Inject NaN for handling test
        'Label': [0, 1, 0],
        'Attack': ['Benign', 'DoS', 'Benign']
    })

def test_pipeline_validation(mock_raw_data):
    pipeline = DataPipeline()
    assert pipeline.validate_schema(mock_raw_data) == True
    
    with pytest.raises(ValueError):
        pipeline.validate_schema(mock_raw_data.drop(columns=['Label']))

def test_missing_values(mock_raw_data):
    pipeline = DataPipeline()
    cleaned = pipeline.handle_missing_values(mock_raw_data)
    assert len(cleaned) == 2 # One row had NaN

def test_feature_selection(mock_raw_data):
    pipeline = DataPipeline()
    X, y_label, y_attack = pipeline.select_features(mock_raw_data)
    assert 'IPV4_SRC_ADDR' not in X.columns
    assert 'Label' not in X.columns
    assert 'IN_BYTES' in X.columns
    assert len(y_label) == 3

def test_normalization(mock_raw_data):
    pipeline = DataPipeline()
    cleaned = pipeline.handle_missing_values(mock_raw_data)
    X, _, _ = pipeline.select_features(cleaned)
    X_num = pipeline.numeric_conversion(X)
    
    # Train normalizer
    X_norm = pipeline.normalize(X_num, is_train=True)
    assert not X_norm.isna().any().any()
    
    # Check that inf is handled if scaling generated it (unlikely here but handled in code)
    assert not np.isinf(X_norm).any().any()

def test_canonical_conversion(mock_raw_data):
    pipeline = DataPipeline()
    events = pipeline.process_to_canonical(mock_raw_data)
    
    assert len(events) == 3
    assert events[0].source_ip == '192.168.1.1'
    assert events[0].label == 0
    assert events[1].attack_type == 'DoS'
    # Assert missing fields remain None (not fabricated)
    assert events[0].host is None

def test_train_test_split(mock_raw_data):
    pipeline = DataPipeline()
    # Need larger mock data to avoid train_test_split stratification errors on tiny sets
    large_mock = pd.concat([mock_raw_data] * 10, ignore_index=True)
    train, val, test = pipeline.split_data(large_mock, stratify_col='Attack')
    
    assert len(train) + len(val) + len(test) == len(large_mock)
    assert len(train) > len(val)
    assert abs(len(val) - len(test)) <= 1
