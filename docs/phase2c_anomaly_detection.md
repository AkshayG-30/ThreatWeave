# Phase 2C Anomaly Detection (Isolation Forest)

## 1. Objective
The purpose of this phase is to implement an independent anomaly-detection layer capable of identifying behavior that differs from the normal training distribution. This model does not explicitly detect "zero-day" attacks yet (that requires unseen attack categories), but sets up the framework for discovering unknown anomalous patterns.

## 2. Training Data
The Isolation Forest is trained exclusively on the **BENIGN** subset of the training split. This ensures the model learns the baseline distribution of normal traffic rather than attempting to model the malicious distribution.

## 3. Feature Set
The anomaly detector shares the exact same 41 numeric features as the supervised XGBoost model to maintain alignment and simplify the preprocessing pipeline. Identifier variables (IPs) and Target variables (Label/Attack) were strictly excluded.

## 4. Score Definition
The `decision_function` from sklearn's `IsolationForest` returns positive scores for normal behavior and negative for anomalies. To follow standard ThreatWeave conventions, this score is negated:
**Higher Anomaly Score = More Anomalous**.

## 5. Threshold Strategy
Instead of blindly relying on the `contamination` parameter, the threshold was explicitly tuned against the Validation Set. The threshold was optimized to maximize the F1-score on the validation data, balancing False Positive Rate and Recall.

## 6. Test Results & Overlap
(Refer to the main Phase 2C report for exact metrics). The results show the anomaly detector works entirely independently of the supervised XGBoost model. By categorizing test events into SUPERVISED, ANOMALY, BOTH, or NONE, the Correlation Engine can prioritize alerts.

## 7. Limitations
**Important:** It is not claimed that this model can detect zero-day attacks yet. While it has successfully detected anomalies, true zero-day validation requires holding out specific attack classes (e.g., Worms or Shellcode) from the training phase entirely and testing if the anomaly detector flags them. This will be explored in future correlation phases.
