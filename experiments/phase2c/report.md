# Phase 2C Isolation Forest Experiment Report

## Overview
- **Training Samples (Benign Only)**: 100825
- **Features Used**: 41
- **Threshold**: 0.0094 (Optimized via Validation F1)

## Model Performance (Test Set)
| Metric | Isolation Forest |
|---|---|
| Precision | 0.2496 |
| Recall | 0.5508 |
| F1 | 0.3436 |
| Macro-F1 | 0.6494 |
| FPR | 0.06860 |
| Accuracy | 0.9163 |

## Detector Overlap (Test Set)
- **XGBoost Only**: 443
- **Anomaly Only**: 1442
- **Both**: 533
- **Neither**: 20082

**Potential Rescued Attacks (XGBoost missed, IF detected)**: 1

## Attack Category Detection (IF)
| Category | Total Samples | Detected | Recall Rate |
|---|---|---|---|
| Exploits | 297 | 97 | 32.66% |
| Fuzzers | 210 | 106 | 50.48% |
| Generic | 156 | 138 | 88.46% |
| Reconnaissance | 121 | 74 | 61.16% |
| DoS | 54 | 36 | 66.67% |
| Analysis | 22 | 18 | 81.82% |
| Backdoor | 20 | 17 | 85.00% |
| Shellcode | 14 | 6 | 42.86% |
| Worms | 1 | 1 | 100.00% |
