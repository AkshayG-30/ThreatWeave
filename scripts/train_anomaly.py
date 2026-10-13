import os
import sys
import json
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

sys.path.append('backend')
from app.services.pipeline import DataPipeline

def main():
    exp_dir = Path("experiments/phase2c")
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Data
    data_path = r"D:\Zephyr\ThreatWeave\data\processed\nf_unsw_nb15_v2_sample_150k.parquet"
    print("Loading dataset...")
    try:
        df = pd.read_parquet(data_path)
    except Exception as e:
        df = pd.read_csv(data_path.replace(".parquet", ".csv"))
    
    # 2. Pipeline processing
    pipeline = DataPipeline(random_state=42)
    train_df, val_df, test_df = pipeline.split_data(df, stratify_col='Attack')
    
    X_train_raw, y_train, attack_train = pipeline.select_features(train_df)
    X_val_raw, y_val, attack_val = pipeline.select_features(val_df)
    X_test_raw, y_test, attack_test = pipeline.select_features(test_df)
    
    X_train_num = pipeline.numeric_conversion(X_train_raw)
    X_val_num = pipeline.numeric_conversion(X_val_raw)
    X_test_num = pipeline.numeric_conversion(X_test_raw)
    
    X_train = pipeline.normalize(X_train_num, is_train=True)
    X_val = pipeline.normalize(X_val_num, is_train=False)
    X_test = pipeline.normalize(X_test_num, is_train=False)
    
    # 3. Train Isolation Forest (using benign data only)
    print("Training Isolation Forest on Benign Training Data...")
    benign_mask = (y_train == 0)
    X_train_benign = X_train[benign_mask]
    
    iso_forest = IsolationForest(n_estimators=200, random_state=42, n_jobs=-1)
    iso_forest.fit(X_train_benign)
    
    # 4. Anomaly Scores (Higher = more anomalous)
    def get_anomaly_scores(model, X):
        # decision_function returns positive for normal, negative for anomaly
        # Negate it so higher score -> more anomalous
        scores = -model.decision_function(X)
        return scores
        
    val_scores = get_anomaly_scores(iso_forest, X_val)
    test_scores = get_anomaly_scores(iso_forest, X_test)
    
    # 5. Threshold Selection using Validation Set
    print("Selecting threshold on Validation Set...")
    # Test a range of percentiles
    best_threshold = 0
    best_f1 = 0
    
    thresholds = np.percentile(val_scores, np.linspace(90, 99.9, 50))
    for thresh in thresholds:
        preds = (val_scores > thresh).astype(int)
        f1 = f1_score(y_val, preds, zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = float(thresh)
            
    print(f"Selected Threshold: {best_threshold:.4f} (Val F1: {best_f1:.4f})")
    
    # 6. Test Set Evaluation
    print("Evaluating on Test Set...")
    test_preds = (test_scores > best_threshold).astype(int)
    
    cm = confusion_matrix(y_test, test_preds)
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    
    metrics = {
        "Accuracy": float(accuracy_score(y_test, test_preds)),
        "Precision": float(precision_score(y_test, test_preds, zero_division=0)),
        "Recall": float(recall_score(y_test, test_preds, zero_division=0)),
        "F1": float(f1_score(y_test, test_preds, zero_division=0)),
        "Macro-F1": float(f1_score(y_test, test_preds, average='macro', zero_division=0)),
        "FPR": float(fpr),
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp)
    }
    
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', xticklabels=['Benign', 'Anomaly'], yticklabels=['Benign', 'Anomaly'])
    plt.title('Isolation Forest Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(exp_dir / "isolation_forest_confusion_matrix.png")
    plt.close()
    
    # 7. XGBoost + Anomaly Overlap
    print("Calculating overlap with XGBoost...")
    xgb = XGBClassifier()
    xgb.load_model("models/xgboost_detector.json")
    
    xgb_test_preds = xgb.predict(X_test)
    
    xgb_only = 0
    anomaly_only = 0
    both = 0
    neither = 0
    
    # For actual attacks (y_test == 1)
    attack_mask = (y_test == 1)
    
    # Analyze overlap on the test set
    for t_xgb, t_anom in zip(xgb_test_preds, test_preds):
        if t_xgb == 1 and t_anom == 0:
            xgb_only += 1
        elif t_xgb == 0 and t_anom == 1:
            anomaly_only += 1
        elif t_xgb == 1 and t_anom == 1:
            both += 1
        else:
            neither += 1
            
    rescued_attacks = 0
    for t_true, t_xgb, t_anom in zip(y_test, xgb_test_preds, test_preds):
        if t_true == 1 and t_xgb == 0 and t_anom == 1:
            rescued_attacks += 1
            
    overlap = {
        "xgb_only": xgb_only,
        "anomaly_only": anomaly_only,
        "both": both,
        "neither": neither,
        "rescued_attacks": rescued_attacks
    }
    
    # 8. Attack Category Analysis (IF)
    print("Performing Attack Category Analysis...")
    attack_results = {}
    for attack_cat in attack_test.unique():
        if attack_cat == 'Benign':
            continue
        mask = (attack_test == attack_cat)
        total = mask.sum()
        if total > 0:
            detected = (test_preds[mask] == 1).sum()
            attack_results[attack_cat] = {
                "total": int(total),
                "detected": int(detected),
                "recall": float(detected / total)
            }
            
    # 9. Score Distribution Plot
    plt.figure(figsize=(10,6))
    sns.histplot(test_scores[y_test == 0], color='blue', alpha=0.5, label='Benign', bins=50, stat='density')
    sns.histplot(test_scores[y_test == 1], color='red', alpha=0.5, label='Attack', bins=50, stat='density')
    plt.axvline(best_threshold, color='black', linestyle='dashed', linewidth=2, label=f'Threshold ({best_threshold:.3f})')
    plt.title('Isolation Forest Anomaly Score Distribution (Test Set)')
    plt.xlabel('Anomaly Score (Higher = More Anomalous)')
    plt.ylabel('Density')
    plt.legend()
    plt.tight_layout()
    plt.savefig(exp_dir / "anomaly_score_distribution.png")
    plt.close()
    
    # Save Model
    joblib.dump(iso_forest, "models/isolation_forest.joblib")
    
    results = {
        "Test_Metrics": metrics,
        "Validation_F1_at_Threshold": float(best_f1),
        "Threshold": best_threshold,
        "Overlap_Analysis": overlap,
        "Attack_Analysis": attack_results
    }
    
    with open(exp_dir / "results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    config = {
        "random_seed": 42,
        "dataset_sample_size": len(df),
        "split_ratios": [0.7, 0.15, 0.15],
        "training_samples_benign_only": int(sum(benign_mask)),
        "feature_count": len(X_train.columns),
        "if_parameters": {"n_estimators": 200, "random_state": 42},
        "threshold_strategy": "Validation F1 Optimization",
        "selected_threshold": best_threshold
    }
    with open(exp_dir / "config.json", "w") as f:
        json.dump(config, f, indent=4)
        
    # Generate Markdown Report
    report = f"""# Phase 2C Isolation Forest Experiment Report

## Overview
- **Training Samples (Benign Only)**: {config['training_samples_benign_only']}
- **Features Used**: {config['feature_count']}
- **Threshold**: {best_threshold:.4f} (Optimized via Validation F1)

## Model Performance (Test Set)
| Metric | Isolation Forest |
|---|---|
| Precision | {metrics['Precision']:.4f} |
| Recall | {metrics['Recall']:.4f} |
| F1 | {metrics['F1']:.4f} |
| Macro-F1 | {metrics['Macro-F1']:.4f} |
| FPR | {metrics['FPR']:.5f} |
| Accuracy | {metrics['Accuracy']:.4f} |

## Detector Overlap (Test Set)
- **XGBoost Only**: {overlap['xgb_only']}
- **Anomaly Only**: {overlap['anomaly_only']}
- **Both**: {overlap['both']}
- **Neither**: {overlap['neither']}

**Potential Rescued Attacks (XGBoost missed, IF detected)**: {overlap['rescued_attacks']}

## Attack Category Detection (IF)
| Category | Total Samples | Detected | Recall Rate |
|---|---|---|---|
"""
    for cat, stats in sorted(attack_results.items(), key=lambda x: x[1]['total'], reverse=True):
        report += f"| {cat} | {stats['total']} | {stats['detected']} | {stats['recall']:.2%} |\n"
        
    with open(exp_dir / "report.md", "w") as f:
        f.write(report)
        
    print("Phase 2C complete. Results saved.")

if __name__ == "__main__":
    main()
