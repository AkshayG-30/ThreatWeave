import sys
import json
import time
import pandas as pd
import numpy as np
import lightgbm as lgb
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

sys.path.append('backend')
from app.services.pipeline import DataPipeline

def main():
    EXP_DIR = Path("D:/Zephyr/ThreatWeave/experiments/detection_benchmark")
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    
    DATA_PATH = Path("D:/Zephyr/ThreatWeave/data/processed/nf_unsw_nb15_v2_sample_150k.csv")
    FEATURES_PATH = Path("D:/Zephyr/ThreatWeave/models/feature_columns.json")
    PHASE2B_RESULTS_PATH = Path("D:/Zephyr/ThreatWeave/experiments/phase2b/results.json")
    
    with open(FEATURES_PATH, 'r') as f:
        feature_columns = json.load(f)
        
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    pipeline = DataPipeline(random_state=42)
    train_df, val_df, test_df = pipeline.split_data(df, stratify_col='Attack')
    
    X_train_raw, y_train, _ = pipeline.select_features(train_df)
    X_val_raw, y_val, _ = pipeline.select_features(val_df)
    X_test_raw, y_test, _ = pipeline.select_features(test_df)
    
    X_train_num = pipeline.numeric_conversion(X_train_raw)
    X_val_num = pipeline.numeric_conversion(X_val_raw)
    X_test_num = pipeline.numeric_conversion(X_test_raw)
    
    X_train = pipeline.normalize(X_train_num, is_train=True)
    X_val = pipeline.normalize(X_val_num, is_train=False)
    X_test = pipeline.normalize(X_test_num, is_train=False)
    
    X_train = X_train[feature_columns]
    X_test = X_test[feature_columns]
    
    # Class weights
    num_neg = (y_train == 0).sum()
    num_pos = (y_train == 1).sum()
    scale_pos = num_neg / num_pos if num_pos > 0 else 1.0
    
    print("Training LightGBM...")
    model = lgb.LGBMClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        scale_pos_weight=scale_pos,
        random_state=42,
        verbose=-1
    )
    
    start_time = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    model.booster_.save_model(EXP_DIR / "lightgbm_model.txt")
    
    print("Evaluating LightGBM...")
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    spec = tn / (fp + tn) if (fp + tn) > 0 else 0
    f1_b = f1_score(y_test, y_pred, pos_label=0, zero_division=0)
    macro_f1 = (f1 + f1_b) / 2
    
    lgb_metrics = {
        "Accuracy": float(acc), "Precision": float(prec), "Recall": float(rec),
        "F1": float(f1), "Macro-F1": float(macro_f1), "Specificity": float(spec), "FPR": float(fpr),
        "TP": int(tp), "TN": int(tn), "FP": int(fp), "FN": int(fn),
        "TrainingTime_s": float(train_time)
    }
    
    # Load Phase 2B Results to combine
    if PHASE2B_RESULTS_PATH.exists():
        with open(PHASE2B_RESULTS_PATH, 'r') as f:
            p2_res = json.load(f)
            rf_metrics = p2_res.get("Random_Forest", {})
            xgb_metrics = p2_res.get("XGBoost", {})
            times = p2_res.get("Training_Time_s", {})
            
            rf_metrics["Specificity"] = rf_metrics.get("TN", 0) / (rf_metrics.get("TN", 0) + rf_metrics.get("FP", 0))
            xgb_metrics["Specificity"] = xgb_metrics.get("TN", 0) / (xgb_metrics.get("TN", 0) + xgb_metrics.get("FP", 0))
            
            rf_metrics["TrainingTime_s"] = times.get("Random_Forest", 0)
            xgb_metrics["TrainingTime_s"] = times.get("XGBoost", 0)
    else:
        rf_metrics = {}
        xgb_metrics = {}
        
    comparison_data = [
        {"Model": "Random Forest", **rf_metrics},
        {"Model": "XGBoost", **xgb_metrics},
        {"Model": "LightGBM", **lgb_metrics}
    ]
    
    df_comp = pd.DataFrame(comparison_data)
    # Ensure correct column order
    cols = ["Model", "Accuracy", "Precision", "Recall", "F1", "Macro-F1", "Specificity", "FPR", "TP", "TN", "FP", "FN", "TrainingTime_s"]
    df_comp = df_comp[[c for c in cols if c in df_comp.columns]]
    df_comp.to_csv(EXP_DIR / "comparison.csv", index=False)
    
    with open(EXP_DIR / "comparison.json", "w") as f:
        json.dump(comparison_data, f, indent=4)
        
    config = {
        "dataset": "NF-UNSW-NB15-v2",
        "dataset_sample_size": len(df),
        "features": len(feature_columns),
        "random_seed": 42,
        "lgb_parameters": {
            "n_estimators": 100,
            "max_depth": 6,
            "learning_rate": 0.1,
            "random_state": 42
        }
    }
    with open(EXP_DIR / "config.json", "w") as f:
        json.dump(config, f, indent=4)
        
    report = f"""# Detection Benchmark: LightGBM vs XGBoost vs Random Forest

## 1. Objective
Experimentally benchmark LightGBM against the existing Random Forest and XGBoost production candidate models on the NF-UNSW-NB15-v2 dataset. 

## 2. Methodology
- **Dataset**: NF-UNSW-NB15-v2 (150,000-row sample).
- **Features**: Exact same 41 feature sequence.
- **Data Split**: Same 70/15/15 DataPipeline stratification.
- **Preprocessing**: Deterministic StandardScaler fit on training data.
- **Configuration**: LightGBM uses comparable architecture (100 estimators, max depth 6, 0.1 learning rate).

## 3. Results Comparison
| Model | Accuracy | Precision | Recall | F1 | FPR | Training Time (s) |
|---|---:|---:|---:|---:|---:|---:|
"""
    for r in comparison_data:
        # Check if Model exists (just in case phase2b json was empty)
        if "Accuracy" in r:
            report += f"| {r['Model']} | {r['Accuracy']:.4f} | {r.get('Precision', 0):.4f} | {r.get('Recall', 0):.4f} | {r.get('F1', 0):.4f} | {r.get('FPR', 0):.5f} | {r.get('TrainingTime_s', 0):.2f} |\n"
            
    report += """
## 4. NF-ToN-IoT-v2 Status
NF-ToN-IoT-v2 was listed as an additional cross-source target in the planned architecture but was not included in the final MVP due to time/data-access constraints. NF-CSE-CIC-IDS2018-v2 was used as the primary real cross-dataset evaluation.

## 5. MVP Impact
MVP architecture unchanged. The production XGBoost model (`models/xgboost_detector.json`) was strictly preserved. LightGBM is purely an experimental artifact.
"""
    with open(EXP_DIR / "report.md", "w") as f:
        f.write(report)
        
    print("Benchmark complete.")

if __name__ == "__main__":
    main()
