# Final Experimental Results

------------------------------------------------------------
A. PRODUCTION XGBOOST
------------------------------------------------------------

NF-UNSW:
Precision ≈ 0.9160
Recall ≈ 0.9989
F1 ≈ 0.9556
FPR ≈ 0.0038

------------------------------------------------------------
B. UNSEEN ATTACK-FAMILY EXPERIMENT
------------------------------------------------------------

**Fuzzers:**
Recall = 68.64%
Precision = 93.12%
F1 = 79.02%
FPR = 0.246%

**Reconnaissance:**
Recall = 100%
Precision = 87.45%
F1 = 93.31%
FPR = 0.399%

*These are family-level holdout experiments, NOT zero-day evaluation.*

------------------------------------------------------------
C. REAL CROSS-DATASET
------------------------------------------------------------

**NF-UNSW → NF-CSE-CIC-IDS2018**
Target:
Accuracy ≈ 52.05%
Precision ≈ 1.29%
Recall ≈ 4.05%
F1 ≈ 1.96%
FPR ≈ 41.50%

*Interpretation: Severe cross-dataset distribution shift.*

------------------------------------------------------------
D. ANOMALY DETECTION
------------------------------------------------------------

**Isolation Forest:**
Precision ≈ 24.96%
Recall ≈ 55.08%
F1 ≈ 34.36%
FPR ≈ 6.86%

**Autoencoder:**
Precision ≈ 39.01%
Recall ≈ 53.74%
F1 ≈ 45.20%
FPR ≈ 3.48%

*Interpretation: Autoencoder provides a more precise anomaly signal with lower FPR and higher F1 in this experiment, while Isolation Forest retains slightly higher recall.*

------------------------------------------------------------
E. CONTROLLED ATTACK-CHAIN RECONSTRUCTION
------------------------------------------------------------

**CONTROLLED SYNTHETIC VALIDATION**
- 8 attack events
- 1 noise event

**Results:**
- Chain completeness = 100%
- Noise isolation = 100%

------------------------------------------------------------
F. LIGHTGBM BENCHMARK
------------------------------------------------------------

- Accuracy ≈ 0.9984
- Precision ≈ 0.9634
- Recall ≈ 0.9926
- F1 ≈ 0.9778
- FPR ≈ 0.0009
- Training Time ≈ 0.47s

------------------------------------------------------------
G. ABLATION
------------------------------------------------------------

1. **Baseline**: High precision, rapid point-detections using supervised XGBoost.
2. **+ Anomaly**: Complementary behavioral detections using Isolation Forest, raising recall to 100% on test sample, but natively injecting a massive spike in FPR (7%).
3. **+ Correlation**: Entity/Temporal bonding that structures events together, successfully mitigating the high anomaly FPR by isolating uncorrelated statistical noise.
4. **+ Graph**: Deterministic topological mapping utilizing NetworkX to map connections, creating visual dependencies for investigation.
5. **+ Explanation**: LLM-driven post-detection evidence grounding. *Note: The automated ablation environment utilized deterministic fallback when authenticated external API access was unavailable. We do not claim a numerical live-LLM quality score from automated tests.*
