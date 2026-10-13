import os
import sys
import json
import time
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

sys.path.append('backend')
from app.services.pipeline import DataPipeline

def main():
    # Setup directories
    Path("models").mkdir(parents=True, exist_ok=True)
    exp_dir = Path("experiments/phase2b")
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Data
    data_path = r"D:\Zephyr\ThreatWeave\data\processed\nf_unsw_nb15_v2_sample_150k.parquet"
    print(f"Loading data from {data_path}...")
    try:
        df = pd.read_parquet(data_path)
    except Exception as e:
        df = pd.read_csv(data_path.replace(".parquet", ".csv"))
    
    # 2. Pipeline processing
    print("Processing pipeline...")
    pipeline = DataPipeline(random_state=42)
    
    # Keep the attack column attached temporarily for split, pipeline handles this
    train_df, val_df, test_df = pipeline.split_data(df, stratify_col='Attack')
    
    # Extract targets and features
    X_train_raw, y_train, attack_train = pipeline.select_features(train_df)
    X_val_raw, y_val, attack_val = pipeline.select_features(val_df)
    X_test_raw, y_test, attack_test = pipeline.select_features(test_df)
    
    # Numeric conversion
    X_train_num = pipeline.numeric_conversion(X_train_raw)
    X_val_num = pipeline.numeric_conversion(X_val_raw)
    X_test_num = pipeline.numeric_conversion(X_test_raw)
    
    # Normalize (Fit on train only)
    X_train = pipeline.normalize(X_train_num, is_train=True)
    X_val = pipeline.normalize(X_val_num, is_train=False)
    X_test = pipeline.normalize(X_test_num, is_train=False)
    
    features = list(X_train.columns)
    with open("models/feature_columns.json", "w") as f:
        json.dump(features, f)
        
    print(f"Train size: {len(X_train)}, Val size: {len(X_val)}, Test size: {len(X_test)}")
    print(f"Features count: {len(features)}")
    
    # Calculate scale_pos_weight for XGBoost
    num_neg = (y_train == 0).sum()
    num_pos = (y_train == 1).sum()
    scale_pos_weight = float(num_neg / num_pos) if num_pos > 0 else 1.0

    # 3. Train Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)
    start_time = time.time()
    rf.fit(X_train, y_train)
    rf_time = time.time() - start_time
    print(f"RF training took {rf_time:.2f}s")
    joblib.dump(rf, "models/random_forest_baseline.joblib")
    
    # 4. Train XGBoost
    print("Training XGBoost...")
    xgb = XGBClassifier(
        n_estimators=100, 
        max_depth=6, 
        learning_rate=0.1, 
        scale_pos_weight=scale_pos_weight, 
        random_state=42, 
        n_jobs=-1,
        eval_metric='logloss',
        tree_method='hist' # Fast on CPU
    )
    start_time = time.time()
    xgb.fit(X_train, y_train)
    xgb_time = time.time() - start_time
    print(f"XGBoost training took {xgb_time:.2f}s")
    xgb.save_model("models/xgboost_detector.json")
    
    # 5. Evaluate
    print("Evaluating models on untouched test set...")
    def eval_model(model, name, X_t, y_t):
        preds = model.predict(X_t)
        cm = confusion_matrix(y_t, preds)
        tn, fp, fn, tp = cm.ravel()
        
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        
        metrics = {
            "Accuracy": accuracy_score(y_t, preds),
            "Precision": precision_score(y_t, preds, zero_division=0),
            "Recall": recall_score(y_t, preds, zero_division=0),
            "F1": f1_score(y_t, preds, zero_division=0),
            "Macro-F1": f1_score(y_t, preds, average='macro', zero_division=0),
            "FPR": fpr,
            "TN": int(tn),
            "FP": int(fp),
            "FN": int(fn),
            "TP": int(tp),
            "Benign_Recall": tn / (tn + fp) if (tn + fp) > 0 else 0,
            "Attack_Recall": tp / (tp + fn) if (tp + fn) > 0 else 0
        }
        
        # Plot CM
        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Benign', 'Attack'], yticklabels=['Benign', 'Attack'])
        plt.title(f'{name} Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(exp_dir / f"{name.lower().replace(' ', '_')}_confusion_matrix.png")
        plt.close()
        
        return metrics, preds
        
    rf_metrics, rf_preds = eval_model(rf, "Random Forest", X_test, y_test)
    xgb_metrics, xgb_preds = eval_model(xgb, "XGBoost", X_test, y_test)
    
    # 6. Attack Category Analysis (using XGBoost predictions as primary example, or both)
    print("Performing Attack Category Analysis...")
    def analyze_attacks(preds, y_true, attacks_true):
        attack_results = {}
        for attack_cat in attacks_true.unique():
            if attack_cat == 'Benign':
                continue
            mask = (attacks_true == attack_cat)
            total = mask.sum()
            if total > 0:
                detected = (preds[mask] == 1).sum()
                attack_results[attack_cat] = {
                    "total": int(total),
                    "detected": int(detected),
                    "recall": float(detected / total)
                }
        return attack_results
        
    rf_attack_perf = analyze_attacks(rf_preds, y_test, attack_test)
    xgb_attack_perf = analyze_attacks(xgb_preds, y_test, attack_test)
    
    # 7. Save Results
    results = {
        "Random_Forest": rf_metrics,
        "XGBoost": xgb_metrics,
        "Attack_Analysis_RF": rf_attack_perf,
        "Attack_Analysis_XGB": xgb_attack_perf,
        "Training_Time_s": {
            "Random_Forest": rf_time,
            "XGBoost": xgb_time
        }
    }
    
    with open(exp_dir / "results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    # Generate Markdown Report
    report = f"""# Phase 2B Supervised ML Experiment Report

## Overview
- **Dataset Size**: {len(df)} rows
- **Train**: {len(X_train)} (70%)
- **Validation**: {len(X_val)} (15%)
- **Test**: {len(X_test)} (15%)
- **Features Used**: {len(features)}
- **Excluded Features**: Label, Attack, IPV4_SRC_ADDR, IPV4_DST_ADDR (Prevent leakage)

## Model Comparison (Test Set)

| Metric | Random Forest | XGBoost |
|---|---|---|
| Precision | {rf_metrics['Precision']:.4f} | {xgb_metrics['Precision']:.4f} |
| Recall | {rf_metrics['Recall']:.4f} | {xgb_metrics['Recall']:.4f} |
| F1 | {rf_metrics['F1']:.4f} | {xgb_metrics['F1']:.4f} |
| Macro-F1 | {rf_metrics['Macro-F1']:.4f} | {xgb_metrics['Macro-F1']:.4f} |
| FPR | {rf_metrics['FPR']:.5f} | {xgb_metrics['FPR']:.5f} |
| Accuracy | {rf_metrics['Accuracy']:.4f} | {xgb_metrics['Accuracy']:.4f} |
| Training Time (s) | {rf_time:.2f} | {xgb_time:.2f} |

### True Positive / False Positive Analysis
- **Random Forest**: TN={rf_metrics['TN']}, FP={rf_metrics['FP']}, FN={rf_metrics['FN']}, TP={rf_metrics['TP']}
- **XGBoost**: TN={xgb_metrics['TN']}, FP={xgb_metrics['FP']}, FN={xgb_metrics['FN']}, TP={xgb_metrics['TP']}

## Attack Category Detection (XGBoost)
| Category | Total Samples | Detected | Recall Rate |
|---|---|---|---|
"""
    for cat, stats in sorted(xgb_attack_perf.items(), key=lambda x: x[1]['total'], reverse=True):
        report += f"| {cat} | {stats['total']} | {stats['detected']} | {stats['recall']:.2%} |\n"
        
    with open(exp_dir / "report.md", "w") as f:
        f.write(report)
        
    # Config / Reproducibility Metadata
    config = {
        "random_seed": 42,
        "dataset_sample_size": len(df),
        "split_ratios": [0.7, 0.15, 0.15],
        "feature_count": len(features),
        "excluded_columns": pipeline.drop_for_ml + pipeline.targets,
        "rf_parameters": {"n_estimators": 100, "class_weight": "balanced", "random_state": 42},
        "xgb_parameters": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1, "scale_pos_weight": scale_pos_weight, "tree_method": "hist"},
        "threshold": 0.5
    }
    with open(exp_dir / "config.json", "w") as f:
        json.dump(config, f, indent=4)
        
    print("Experiment complete. Results saved in experiments/phase2b/")

if __name__ == "__main__":
    main()
