# Phase 2B Supervised ML Experiment Report

## Overview
- **Dataset Size**: 150000 rows
- **Train**: 105000 (70%)
- **Validation**: 22500 (15%)
- **Test**: 22500 (15%)
- **Features Used**: 41
- **Excluded Features**: Label, Attack, IPV4_SRC_ADDR, IPV4_DST_ADDR (Prevent leakage)

## Model Comparison (Test Set)

| Metric | Random Forest | XGBoost |
|---|---|---|
| Precision | 0.9497 | 0.9160 |
| Recall | 0.9698 | 0.9989 |
| F1 | 0.9596 | 0.9556 |
| Macro-F1 | 0.9790 | 0.9769 |
| FPR | 0.00213 | 0.00380 |
| Accuracy | 0.9968 | 0.9963 |
| Training Time (s) | 2.89 | 1.95 |

### True Positive / False Positive Analysis
- **Random Forest**: TN=21559, FP=46, FN=27, TP=868
- **XGBoost**: TN=21523, FP=82, FN=1, TP=894

## Attack Category Detection (XGBoost)
| Category | Total Samples | Detected | Recall Rate |
|---|---|---|---|
| Exploits | 297 | 297 | 100.00% |
| Fuzzers | 210 | 210 | 100.00% |
| Generic | 156 | 156 | 100.00% |
| Reconnaissance | 121 | 121 | 100.00% |
| DoS | 54 | 54 | 100.00% |
| Analysis | 22 | 21 | 95.45% |
| Backdoor | 20 | 20 | 100.00% |
| Shellcode | 14 | 14 | 100.00% |
| Worms | 1 | 1 | 100.00% |
