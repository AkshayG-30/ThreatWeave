# Unseen Attack-Family Generalization Evaluation

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
| Fuzzers | 1400 | 961 | 439 | 0.6864 | 0.9312 | 0.7903 | 0.0025 |
| Reconnaissance | 802 | 802 | 0 | 1.0000 | 0.8746 | 0.9331 | 0.0040 |

## 7. Interpretation
The results measure supervised generalization. If recall is high, the model learned a generalized representation of malicious flow dynamics. If recall is poor, it confirms that supervised Tree models act largely as signature-matchers and fail drastically on truly unseen attack families.

## 8. Limitations
- This is a dataset-level family holdout, NOT true zero-day detection (which would involve entirely novel protocols/vulnerabilities).
- Generalization applies only to withheld families within the same network distribution.

## 9. Relationship to ThreatWeave
This experiment motivates ThreatWeave's multi-layered architecture. Supervised models inherently suffer blind spots on unseen attack vectors. ThreatWeave's Phase 2C Isolation Forest anomaly detection and Phase 3 Graph Correlation are required to catch precisely the zero-day families missed by the XGBoost layer.

## 10. MVP Impact
MVP architecture unchanged. These models are purely experimental and stored in `experiments/unseen_attack/models/`.
