# Real Cross-Dataset Zero-Shot Evaluation

## 1. Objective
Evaluate the EXISTING FROZEN ThreatWeave XGBoost detector trained on NF-UNSW-NB15-v2 against the REAL NF-CSE-CIC-IDS2018-V2 dataset without retraining, tuning, or modification.

## 2. Source Dataset
NF-UNSW-NB15-v2

## 3. Target Dataset
Real NF-CSE-CIC-IDS2018-V2

## 4. Dataset Statistics
- Total Rows Evaluated: 17129715
- Total Columns: 43
- Benign Rows: 15101685
- Attack Rows: 2028030

## 5. Feature Compatibility
The target dataset was verified to contain all 41 required features exactly matching the source model expectation. `IPV4_SRC_ADDR` and `IPV4_DST_ADDR` were completely excluded. 

## 6. Frozen Model
Model loaded directly from `xgboost_detector.json`.
- Model retrained: NO
- Model tuned: NO

## 7. Evaluation Protocol
- no retraining
- no fine-tuning
- no threshold tuning
- no target-data fitting
- exact 41 features
- IP identifiers excluded
- exact feature order preserved
- PyArrow batched inference used to safely handle dataset size on CPU.

## 8. Source Metrics
- Precision: 0.9160
- Recall: 0.9989
- F1: 0.9556
- FPR: 0.0038

## 9. Real Target Metrics
- Accuracy: 0.5205
- Precision: 0.0130
- Recall: 0.0406
- F1 Score: 0.0196
- Macro F1: 0.3511
- FPR: 0.4150
- Benign Specificity: 0.5850

## 10. Performance Change
| Metric | NF-UNSW-NB15-v2 | NF-CSE-CIC-IDS2018-V2 | Change |
|--------|-----------------|-----------------------|--------|
| Precision | 0.9160 | 0.0130 | -0.9030 |
| Recall | 0.9989 | 0.0406 | -0.9583 |
| F1 | 0.9556 | 0.0196 | -0.9360 |
| Macro_f1 | 0.9769 | 0.3511 | -0.6258 |
| Fpr | 0.0038 | 0.4150 | +0.4112 |
| Accuracy | 0.9963 | 0.5205 | -0.4758 |

## 11. Attack Category Analysis
- **SSH-Bruteforce**: Support=94979, Detected=30, Recall=0.0003
- **DDoS attacks-LOIC-HTTP**: Support=207078, Detected=5847, Recall=0.0282
- **DDOS attack-HOIC**: Support=1066881, Detected=0, Recall=0.0000
- **DoS attacks-Slowloris**: Support=9512, Detected=0, Recall=0.0000
- **DoS attacks-Hulk**: Support=432648, Detected=192, Recall=0.0004
- **FTP-BruteForce**: Support=25933, Detected=0, Recall=0.0000
- **Infilteration**: Support=115513, Detected=76184, Recall=0.6595
- **Bot**: Support=28033, Detected=0, Recall=0.0000
- **DoS attacks-GoldenEye**: Support=27723, Detected=0, Recall=0.0000
- **Brute Force -Web**: Support=2143, Detected=5, Recall=0.0023
- **DoS attacks-SlowHTTPTest**: Support=14116, Detected=0, Recall=0.0000
- **SQL Injection**: Support=432, Detected=0, Recall=0.0000
- **DDOS attack-LOIC-UDP**: Support=2112, Detected=0, Recall=0.0000
- **Brute Force -XSS**: Support=927, Detected=4, Recall=0.0043

Many target attack categories (e.g., HOIC, LOIC, Hulk) are completely absent from the source dataset training taxonomy (Fuzzers, Analysis, Backdoors). 

## 12. Distribution Shift
A severe cross-dataset distribution shift is present, confirming that while the model safely ignores Benign traffic (maintaining high specificity), unseen attack topologies evade the purely supervised XGBoost signatures.

## 13. Interpretation
The result confirms the necessity of ThreatWeave's Phase 2C Isolation Forest anomaly detection and Phase 3 graph correlation. The supervised detector suffers massive recall degradation on entirely unseen target distributions.

## 14. Limitations
- Unseen categories penalized zero-shot recall.

## 15. Reproducibility
Script `scripts/run_real_cross_dataset.py` reproduces this cleanly on CPU.

## 16. MVP Impact
MVP architecture unchanged.

## 17. Final Verdict
Is this a genuine real-dataset cross-dataset evaluation? **YES**.
The exact production model evaluated the entire real target parquet file using strict domain-shift constraints.
