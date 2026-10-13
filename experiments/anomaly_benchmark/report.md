# Autoencoder Anomaly Detection Benchmark

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
| Autoencoder (MLP) | 0.3901 | 0.5374 | 0.4521 | 0.0348 |

## 4. Evaluation Context
The Autoencoder demonstrates lower FPR, better F1.

## 5. Scientific Interpretation
This is a benchmark of baseline unsupervised anomaly detection architectures.
- **Is this zero-day detection?** No. This evaluates unsupervised discrimination of withheld attacks within the same network distribution.
- **Does this replace the production detector?** Absolutely not. The primary XGBoost detector yields 99.8% recall with <0.4% FPR.
- **Value to ThreatWeave**: If the Autoencoder provides complementary coverage of anomalies, it could theoretically serve alongside Isolation Forest, but structural bounded correlation (Phase 3) remains strictly necessary to mitigate the natively high FPR associated with all unsupervised methods.

## 6. MVP Status
MVP architecture is completely unmodified. This is a strictly isolated experiment.
