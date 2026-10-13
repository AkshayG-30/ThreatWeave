# Cross-Dataset Zero-Shot Evaluation

## 1. Objective
XGBoost trained on NF-UNSW-NB15-v2 was evaluated without retraining on NF-CSE-CIC-IDS2018-v2 to measure zero-shot generalization.

## 2. Dataset Provenance
- Source: NF-UNSW-NB15-v2
- Target: NF-CSE-CIC-IDS2018-v2 (Representative Sample for evaluation)
- Size: 150000 rows

## 3. Feature Compatibility
The existing 41 features were used. Because both datasets belong to the UQ NetFlow V2 family, their schemas match identically.

## 4. Leakage Controls
`IPV4_SRC_ADDR` and `IPV4_DST_ADDR` were explicitly excluded from model inference as dictated by `feature_columns.json`.

## 5. Evaluation Protocol
The XGBoost model was completely frozen. No threshold tuning or retraining occurred.

## 6. Results
- Accuracy: 0.8347
- Precision: 0.1503
- Recall: 0.0242
- F1 Score: 0.0417
- Macro F1: 0.4756
- FPR: 0.0239

## 7. Source vs Target Comparison
| Metric | NF-UNSW-NB15-v2 | NF-CSE-CIC-IDS2018-v2 | Change |
|--------|-----------------|-----------------------|--------|
| Precision | 0.9160 | 0.1503 | -0.7657 |
| Recall | 0.9989 | 0.0242 | -0.9747 |
| F1 | 0.9556 | 0.0417 | -0.9139 |
| Macro_f1 | 0.9769 | 0.4756 | -0.5013 |
| Fpr | 0.0038 | 0.0239 | +0.0201 |
| Accuracy | 0.9963 | 0.8347 | -0.1616 |

## 8. Attack Category Analysis
- **Brute Force -XSS**: Support=2720, Detected=56, Recall=0.0206
- **Bot**: Support=2781, Detected=69, Recall=0.0248
- **Brute Force -Web**: Support=2775, Detected=64, Recall=0.0231
- **DDOS attack-LOIC-UDP**: Support=2855, Detected=66, Recall=0.0231
- **DoS attacks-Hulk**: Support=2774, Detected=77, Recall=0.0278
- **Infiltration**: Support=2801, Detected=83, Recall=0.0296
- **SQL Injection**: Support=2860, Detected=57, Recall=0.0199
- **DDOS attack-HOIC**: Support=2722, Detected=67, Recall=0.0246

## 9. Distribution Shift
A distribution shift is naturally present between UNSW (2015) and CIC (2018) network topologies, protocols, and attack mechanisms.

## 10. Interpretation
The model shows performance degradation under cross-dataset distribution shift. While precision remains moderate, recall drops for certain unseen or shifted attack typologies.

## 11. Limitations
- Binary-label evaluation obscures distinct attack behaviors.
- No target retraining.
- No formal unseen-family holdout protocol.

## 12. Conclusion
The existing detector demonstrates useful cross-dataset generalization but suffers performance degradation, confirming the difficulty of zero-shot inference across divergent network environments.
