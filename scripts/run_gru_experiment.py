import sys
import json
import pandas as pd
from pathlib import Path

def main():
    EXP_DIR = Path("D:/Zephyr/ThreatWeave/experiments/gru_temporal")
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    
    DATA_PATH = Path("D:/Zephyr/ThreatWeave/data/processed/nf_unsw_nb15_v2_sample_150k.csv")
    
    print("Loading NF-UNSW-NB15-v2 sample to check for temporal ground truth...")
    df = pd.read_csv(DATA_PATH)
    
    # Check for chronological columns
    time_cols = [c for c in df.columns if 'time' in c.lower() or 'date' in c.lower() or 'timestamp' in c.lower()]
    
    if not time_cols:
        print("\nGRU experiment not scientifically validated because the available production dataset lacks reliable temporal ground truth.")
        print("NF-UNSW-NB15-v2 lacks strict chronological timestamps required for sequential training.")
        
        # Save empty/null metrics
        metrics = {
            "status": "FAILED_DUE_TO_NO_TEMPORAL_DATA",
            "Accuracy": None,
            "Precision": None,
            "Recall": None,
            "F1": None,
            "TrainingTime_s": None,
            "InferenceTime_s": None,
            "SequenceLength": None,
            "NumberOfSamples": None
        }
        with open(EXP_DIR / "metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)
            
        config = {
            "dataset": "NF-UNSW-NB15-v2",
            "model_type": "GRU(32) -> Dense -> Binary",
            "status": "aborted",
            "reason": "missing_temporal_features"
        }
        with open(EXP_DIR / "config.json", "w") as f:
            json.dump(config, f, indent=4)
            
        report = """# GRU Temporal Experiment Status

## 1. Objective
Create a CPU-friendly GRU experiment demonstrating sequential event modelling as a complement to deterministic correlation.

## 2. Experimental Verdict
**GRU experiment not scientifically validated because the available production dataset lacks reliable temporal ground truth.**

## 3. Explanation
The NF-UNSW-NB15-v2 dataset does not provide the absolute chronological timestamps required to window events into ordered sequences for Recurrent Neural Network (RNN/GRU) training. While a single controlled synthetic sequence (8 events) exists for correlation testing (Phase 3/4), this is severely insufficient for training a neural network, which requires thousands of genuine chronological sequences. 

Fabricating timestamps or randomly shuffling data to simulate sequences was explicitly forbidden by project integrity rules. Thus, the experiment was correctly halted to preserve scientific validity.
"""
        with open(EXP_DIR / "report.md", "w") as f:
            f.write(report)
            
    else:
        print("Temporal columns found! Proceeding with GRU...")
        # (This block will not execute for this dataset)

if __name__ == "__main__":
    main()
