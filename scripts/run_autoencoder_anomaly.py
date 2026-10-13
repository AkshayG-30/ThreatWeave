import sys
import json
import time
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error

sys.path.append('backend')
from app.services.pipeline import DataPipeline

def main():
    EXP_DIR = Path("D:/Zephyr/ThreatWeave/experiments/anomaly_benchmark")
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    
    DATA_PATH = Path("D:/Zephyr/ThreatWeave/data/processed/nf_unsw_nb15_v2_sample_150k.csv")
    FEATURES_PATH = Path("D:/Zephyr/ThreatWeave/models/feature_columns.json")
    
    with open(FEATURES_PATH, 'r') as f:
        feature_columns = json.load(f)
        
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    pipeline = DataPipeline(random_state=42)
    train_df, val_df, test_df = pipeline.split_data(df, stratify_col='Attack')
    
    X_train_raw, y_train, _ = pipeline.select_features(train_df)
    X_val_raw, y_val, _ = pipeline.select_features(val_df)
    X_test_raw, y_test, attack_test = pipeline.select_features(test_df)
    
    X_train_num = pipeline.numeric_conversion(X_train_raw)
    X_val_num = pipeline.numeric_conversion(X_val_raw)
    X_test_num = pipeline.numeric_conversion(X_test_raw)
    
    X_train = pipeline.normalize(X_train_num, is_train=True)
    X_val = pipeline.normalize(X_val_num, is_train=False)
    X_test = pipeline.normalize(X_test_num, is_train=False)
    
    X_train = X_train[feature_columns]
    X_val = X_val[feature_columns]
    X_test = X_test[feature_columns]
    
    # Train only on benign
    benign_mask = (y_train == 0)
    X_train_benign = X_train[benign_mask]
    
    print("Training CPU-friendly MLP Autoencoder...")
    # 41 -> 32 -> 16 -> 8 -> 16 -> 32 -> 41
    autoencoder = MLPRegressor(
        hidden_layer_sizes=(32, 16, 8, 16, 32),
        activation='relu',
        solver='adam',
        max_iter=100,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.1
    )
    
    start_time = time.time()
    autoencoder.fit(X_train_benign, X_train_benign)
    train_time = time.time() - start_time
    
    print("Optimizing threshold on validation set...")
    # Calculate MSE per sample
    def get_anomaly_scores(model, X):
        preds = model.predict(X)
        # Mean squared error per row
        mse = np.mean(np.square(X - preds), axis=1)
        return mse
        
    val_scores = get_anomaly_scores(autoencoder, X_val)
    test_scores = get_anomaly_scores(autoencoder, X_test)
    
    best_threshold = 0
    best_f1 = 0
    thresholds = np.percentile(val_scores, np.linspace(90, 99.9, 50))
    
    for thresh in thresholds:
        preds = (val_scores > thresh).astype(int)
        f1 = f1_score(y_val, preds, zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = float(thresh)
            
    print("Evaluating on test set...")
    start_inf = time.time()
    y_pred = (test_scores > best_threshold).astype(int)
    inf_time = time.time() - start_inf
    
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
    
    ae_metrics = {
        "Accuracy": float(acc), "Precision": float(prec), "Recall": float(rec),
        "F1": float(f1), "Macro-F1": float(macro_f1), "Specificity": float(spec), "FPR": float(fpr),
        "TP": int(tp), "TN": int(tn), "FP": int(fp), "FN": int(fn),
        "TrainingTime_s": float(train_time),
        "InferenceTime_s": float(inf_time)
    }
    
    with open(EXP_DIR / "metrics.json", "w") as f:
        json.dump(ae_metrics, f, indent=4)
        
    # Baseline comparison provided by user
    if_metrics = {
        "Model": "Isolation Forest",
        "Precision": 0.2496,
        "Recall": 0.5508,
        "F1": 0.3436,
        "FPR": 0.0686
    }
    
    ae_comp = {
        "Model": "Autoencoder",
        "Precision": ae_metrics['Precision'],
        "Recall": ae_metrics['Recall'],
        "F1": ae_metrics['F1'],
        "FPR": ae_metrics['FPR']
    }
    
    comp_df = pd.DataFrame([if_metrics, ae_comp])
    comp_df.to_csv(EXP_DIR / "comparison.csv", index=False)
    
    with open(EXP_DIR / "comparison.json", "w") as f:
        json.dump([if_metrics, ae_comp], f, indent=4)
        
    # Attack category support
    cat_recall = {}
    for cat in attack_test.unique():
        if cat == 'Benign': continue
        mask = (attack_test == cat)
        total = mask.sum()
        if total > 0:
            detected = y_pred[mask].sum()
            cat_recall[cat] = {
                "Support": int(total),
                "Detected": int(detected),
                "Recall": float(detected / total)
            }
            
    with open(EXP_DIR / "category_recall.json", "w") as f:
        json.dump(cat_recall, f, indent=4)
        
    # Report
    better_recall = ae_metrics['Recall'] > if_metrics['Recall']
    better_fpr = ae_metrics['FPR'] < if_metrics['FPR']
    better_f1 = ae_metrics['F1'] > if_metrics['F1']
    
    adv = []
    if better_recall: adv.append("better recall")
    if better_fpr: adv.append("lower FPR")
    if better_f1: adv.append("better F1")
    
    if len(adv) > 0:
        advantage_str = f"The Autoencoder demonstrates {', '.join(adv)}."
    else:
        advantage_str = "The Autoencoder does not provide a meaningful quantitative advantage over Isolation Forest."

    report = f"""# Autoencoder Anomaly Detection Benchmark

## 1. Objective
Evaluate whether a benign-trained neural autoencoder provides a useful complementary anomaly signal compared to the existing Isolation Forest layer.

## 2. Experimental Protocol
- **Dataset**: NF-UNSW-NB15-v2 150k sample
- **Model**: Scikit-Learn MLPRegressor functioning as a dense autoencoder (41->32->16->8->16->32->41).
- **Training**: Fitted exclusively on benign training samples using Mean Squared Error (MSE) reconstruction loss.
- **Threshold**: Chosen by maximizing F1 score on the validation split.

## 3. Results Comparison
| Model | Precision | Recall | F1 | FPR |
|---|---|---|---|---|
| Isolation Forest (Reference) | 0.2496 | 0.5508 | 0.3436 | 0.0686 |
| Autoencoder (MLP) | {ae_metrics['Precision']:.4f} | {ae_metrics['Recall']:.4f} | {ae_metrics['F1']:.4f} | {ae_metrics['FPR']:.4f} |

## 4. Evaluation Context
{advantage_str}

## 5. Scientific Interpretation
This is a benchmark of baseline unsupervised anomaly detection architectures.
- **Is this zero-day detection?** No. This evaluates unsupervised discrimination of withheld attacks within the same network distribution.
- **Does this replace the production detector?** Absolutely not. The primary XGBoost detector yields 99.8% recall with <0.4% FPR.
- **Value to ThreatWeave**: If the Autoencoder provides complementary coverage of anomalies, it could theoretically serve alongside Isolation Forest, but structural bounded correlation (Phase 3) remains strictly necessary to mitigate the natively high FPR associated with all unsupervised methods.

## 6. MVP Status
MVP architecture is completely unmodified. This is a strictly isolated experiment.
"""
    with open(EXP_DIR / "report.md", "w") as f:
        f.write(report)
        
    print("Autoencoder benchmark complete.")

if __name__ == "__main__":
    main()
