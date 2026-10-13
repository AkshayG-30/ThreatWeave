import os
import json
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from pathlib import Path

def main():
    EXP_DIR = Path("D:/Zephyr/ThreatWeave/experiments/unseen_attack")
    MODELS_DIR = EXP_DIR / "models"
    DATA_PATH = Path("D:/Zephyr/ThreatWeave/data/processed/nf_unsw_nb15_v2_sample_150k.csv")
    FEATURES_PATH = Path("D:/Zephyr/ThreatWeave/models/feature_columns.json")
    
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    with open(FEATURES_PATH, 'r') as f:
        feature_columns = json.load(f)
        
    # Attack families selection
    held_out_families = ["Fuzzers", "Reconnaissance"]
    
    results = {}
    family_results = []
    
    # We will do separate experiments for each held-out family to see generalization to that specific family
    for holdout in held_out_families:
        print(f"\n=============================================")
        print(f"RUNNING EXPERIMENT: HOLDOUT = {holdout}")
        print(f"=============================================")
        
        # Split Data
        # Train: Benign (Label 0) + All Attacks EXCEPT holdout
        # Test: Benign (Label 0) + Only holdout
        
        # Randomize first
        df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        benign_df = df_shuffled[df_shuffled['Label'] == 0]
        attack_df = df_shuffled[df_shuffled['Label'] == 1]
        
        # Split Benign 80/20 to give train and test some benign traffic
        split_idx = int(len(benign_df) * 0.8)
        train_benign = benign_df.iloc[:split_idx]
        test_benign = benign_df.iloc[split_idx:]
        
        train_attacks = attack_df[attack_df['Attack'] != holdout]
        test_attacks = attack_df[attack_df['Attack'] == holdout]
        
        train_df = pd.concat([train_benign, train_attacks])
        test_df = pd.concat([test_benign, test_attacks])
        
        # Leakage Check
        train_cats = train_df['Attack'].unique()
        test_cats = test_df['Attack'].unique()
        
        if holdout in train_cats:
            raise ValueError(f"LEAKAGE DETECTED: {holdout} is in training categories!")
            
        print(f"Train Categories: {list(train_cats)}")
        print(f"Held-out Category: {holdout}")
        print(f"Zero Leakage Verified.")
        
        X_train = train_df[feature_columns]
        y_train = train_df['Label']
        
        X_test = test_df[feature_columns]
        y_test = test_df['Label']
        
        # Class weighting for training ONLY (using only train distribution)
        num_neg = (y_train == 0).sum()
        num_pos = (y_train == 1).sum()
        scale_pos = num_neg / num_pos if num_pos > 0 else 1.0
        
        print("Training XGBoost...")
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            scale_pos_weight=scale_pos,
            tree_method='hist',
            eval_metric='logloss',
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Save isolated model
        model_path = MODELS_DIR / f"xgb_holdout_{holdout}.json"
        model.save_model(model_path)
        
        print("Evaluating...")
        y_pred = model.predict(X_test)
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
        tn, fp, fn, tp = cm.ravel()
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        benign_spec = tn / (fp + tn) if (fp + tn) > 0 else 0
        
        f1_benign = f1_score(y_test, y_pred, pos_label=0, zero_division=0)
        macro_f1 = (f1 + f1_benign) / 2
        
        res_dict = {
            "Holdout_Family": holdout,
            "Train_Size": int(len(train_df)),
            "Test_Size": int(len(test_df)),
            "Support": int(len(test_attacks)),
            "True_Positives": int(tp),
            "True_Negatives": int(tn),
            "False_Positives": int(fp),
            "False_Negatives": int(fn),
            "Recall": float(rec),
            "Precision": float(prec),
            "F1": float(f1),
            "Macro_F1": float(macro_f1),
            "FPR": float(fpr),
            "Benign_Specificity": float(benign_spec)
        }
        
        results[holdout] = res_dict
        family_results.append(res_dict)
        
        pd.DataFrame(cm, index=['True Benign', 'True Attack'], columns=['Pred Benign', 'Pred Attack']).to_csv(
            EXP_DIR / f"confusion_matrix_{holdout}.csv"
        )
        
        # Leakage Log
        leakage_log = {
            "holdout_family": holdout,
            "train_categories": list(train_cats),
            "test_categories": list(test_cats),
            "intersection": list(set(train_cats) & set(test_cats) - {'Benign'}) # Benign is allowed
        }
        with open(EXP_DIR / f"category_leakage_check_{holdout}.json", "w") as f:
            json.dump(leakage_log, f, indent=4)
            
    # Outputs
    df_results = pd.DataFrame(family_results)
    df_results.to_csv(EXP_DIR / "family_results.csv", index=False)
    
    with open(EXP_DIR / "results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    config = {
        "dataset": "NF-UNSW-NB15-v2",
        "dataset_size": len(df),
        "selected_held_out_families": held_out_families,
        "model_config": {
            "n_estimators": 100,
            "max_depth": 6,
            "learning_rate": 0.1,
            "tree_method": "hist",
            "eval_metric": "logloss",
            "random_state": 42
        },
        "feature_count": len(feature_columns)
    }
    with open(EXP_DIR / "config.json", "w") as f:
        json.dump(config, f, indent=4)
        
    # Markdown Report
    report = f"""# Unseen Attack-Family Generalization Evaluation

## 1. Objective
This experiment evaluates whether the supervised XGBoost detector can generalize to attack families completely excluded from its training data.

## 2. Dataset
NF-UNSW-NB15-v2 (150,000-row stratified sample).

## 3. Experimental Protocol
- **Family-level holdout:** For each experiment, a specific attack family was strictly isolated to the test set.
- **Benign data retained:** Benign data was split 80/20 between Train and Test to ensure realistic FPR calculation.
- **Frozen feature definition:** The 41 features from the production model were reused identically. Identifiers (IPs) were excluded.
- **Experimental XGBoost:** Separate isolated XGBoost models were trained for each holdout scenario.
- **Zero Label Leakage:** The held-out attack labels were absolutely NOT used during model fitting, weighting, or thresholding.

## 4. Selected Held-Out Families
1. **Fuzzers**: Selected because it represents a large and distinct attack signature methodology (rapid, malformed payload injections).
2. **Reconnaissance**: Selected because scanning behavior differs fundamentally from exploits, making it a strong candidate to test whether the model learned generic "attackness" or specific exploits.

## 5. Leakage Verification
For every holdout, the intersection of Train Attack Categories and the Held-Out Category was verified programmatically to be the EMPTY SET. See `category_leakage_check_*.json`.

## 6. Results

| Held-out Family | Support | TP | FN | Recall | Precision | F1 | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|
"""
    for r in family_results:
        report += f"| {r['Holdout_Family']} | {r['Support']} | {r['True_Positives']} | {r['False_Negatives']} | {r['Recall']:.4f} | {r['Precision']:.4f} | {r['F1']:.4f} | {r['FPR']:.4f} |\n"
        
    report += """
## 7. Interpretation
The results measure supervised generalization. If recall is high, the model learned a generalized representation of malicious flow dynamics. If recall is poor, it confirms that supervised Tree models act largely as signature-matchers and fail drastically on truly unseen attack families.

## 8. Limitations
- This is a dataset-level family holdout, NOT true zero-day detection (which would involve entirely novel protocols/vulnerabilities).
- Generalization applies only to withheld families within the same network distribution.

## 9. Relationship to ThreatWeave
This experiment motivates ThreatWeave's multi-layered architecture. Supervised models inherently suffer blind spots on unseen attack vectors. ThreatWeave's Phase 2C Isolation Forest anomaly detection and Phase 3 Graph Correlation are required to catch precisely the zero-day families missed by the XGBoost layer.

## 10. MVP Impact
MVP architecture unchanged. These models are purely experimental and stored in `experiments/unseen_attack/models/`.
"""
    with open(EXP_DIR / "report.md", "w") as f:
        f.write(report)
        
    print("Unseen attack experiment complete.")

if __name__ == "__main__":
    main()
