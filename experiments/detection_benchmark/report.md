# Detection Benchmark: LightGBM vs XGBoost vs Random Forest

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
| Random Forest | 0.9968 | 0.9497 | 0.9698 | 0.9596 | 0.00213 | 2.89 |
| XGBoost | 0.9963 | 0.9160 | 0.9989 | 0.9556 | 0.00380 | 1.95 |
| LightGBM | 0.9962 | 0.9167 | 0.9955 | 0.9545 | 0.00375 | 1.18 |

## 4. NF-ToN-IoT-v2 Status
NF-ToN-IoT-v2 was listed as an additional cross-source target in the planned architecture but was not included in the final MVP due to time/data-access constraints. NF-CSE-CIC-IDS2018-v2 was used as the primary real cross-dataset evaluation.

## 5. MVP Impact
MVP architecture unchanged. The production XGBoost model (`models/xgboost_detector.json`) was strictly preserved. LightGBM is purely an experimental artifact.
