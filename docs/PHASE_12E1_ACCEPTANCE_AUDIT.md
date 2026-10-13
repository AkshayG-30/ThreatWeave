# ThreatWeave Phase 12E.1: Scenario Provenance & Acceptance Audit Report

**Milestone:** Phase 12E.1 — Scenario Provenance & Regression Acceptance Audit  
**Date:** October 9, 2026  
**Auditor / Agent:** Google DeepMind Agentic Pair Programmer (Antigravity IDE)  
**Status:** **ACCEPTED & VERIFIED (Zero Defect / Regression Clean)**  

---

## 1. Executive Summary

This acceptance audit rigorously verifies the completed Phase 12E implementation against the physical codebase, model files, experimental artifacts, and API endpoints of ThreatWeave (`D:\Zephyr\ThreatWeave`).

Key audit findings:
1. **TC-08 Identity Formally Resolved**: Authoritative physical artifacts prove that TC-08 is **Held-Out Fuzzers Evaluation** (`experiments/unseen_attack/models/xgb_holdout_Fuzzers.json`), not Backdoor. No Backdoor holdout model exists in the repository. The physical cache (`TC-08.json`), backend catalogue (`scenarios.json`), and React metadata (`scenario.ts`) correctly implemented Fuzzers; the discrepancy was isolated to an errant label in the Phase 12E markdown documentation, which is now corrected.
2. **Live Inference Provenance Confirmed**: TC-01, TC-02, TC-03, TC-04, TC-06, and TC-07 execute real model inference on genuine flows from the untouched $22,500$-row test split of `NF-UNSW-NB15-v2`. TC-01 zero-alert status was confirmed to originate from true inference scores ($p=0.0$, anomaly scores $-0.028$ to $-0.125$), not artificial list clearing.
3. **Consensus & Divergence Integrity**: TC-06 agreement and TC-07 disagreement samples derive directly from matched row IDs scored simultaneously by `models/xgboost_detector.json` and `models/isolation_forest.joblib`.
4. **Zero-Day Evaluation Provenance**: TC-08 and TC-09 metrics were audited directly against `experiments/unseen_attack/results.json`. Exact metrics (Fuzzers recall $68.64\%$, Reconnaissance recall $100.0\%$) are now aligned with zero rounding discrepancies across all configuration caches.
5. **Regression Verification**: 17 of 17 backend tests pass ($100\%$), production React builds with zero errors ($29.14\text{s}$), legacy frontend builds with zero errors ($814\text{ms}$), and all production model SHA-256 hashes remain perfectly immutable.

---

## 2. Priority 1 — Resolution of TC-08 Identity

### 2.1 Physical Investigation of `experiments/unseen_attack/`

An exhaustive directory inspection of `experiments/unseen_attack/` reveals the following files:
- `config.json` (396 bytes)
- `results.json` (1,051 bytes)
- `family_results.csv` (468 bytes)
- `confusion_matrix_Fuzzers.csv` (69 bytes)
- `confusion_matrix_Reconnaissance.csv` (68 bytes)
- `category_leakage_check_Fuzzers.json` (353 bytes)
- `category_leakage_check_Reconnaissance.json` (360 bytes)
- `models/xgb_holdout_Fuzzers.json` (303,334 bytes, SHA-256: `baa9d09a0126dde5...`)
- `models/xgb_holdout_Reconnaissance.json` (314,604 bytes, SHA-256: `f0ed3cf34ed8a356...`)

No model file named `xgb_holdout_Backdoor.json` exists in `experiments/unseen_attack/models/` or anywhere else in the repository.

### 2.2 Authoritative Evidence from Configuration & Results

1. **`experiments/unseen_attack/config.json`**:
   ```json
   {
       "dataset": "NF-UNSW-NB15-v2",
       "dataset_size": 150000,
       "selected_held_out_families": [
           "Fuzzers",
           "Reconnaissance"
       ],
       ...
   }
   ```
2. **`experiments/unseen_attack/results.json`**:
   ```json
   {
       "Fuzzers": {
           "Holdout_Family": "Fuzzers",
           "Train_Size": 119793,
           "Test_Size": 30207,
           "Support": 1400,
           "True_Positives": 961,
           "True_Negatives": 28736,
           "False_Positives": 71,
           "False_Negatives": 439,
           "Recall": 0.6864285714285714,
           "Precision": 0.9312015503875969,
           "F1": 0.790296052631579,
           "Macro_F1": 0.8907501097209842,
           "FPR": 0.002464678723921269,
           "Benign_Specificity": 0.9975353212760787
       },
       "Reconnaissance": {
           "Holdout_Family": "Reconnaissance",
           "Train_Size": 120391,
           "Test_Size": 29609,
           "Support": 802,
           "True_Positives": 802,
           "True_Negatives": 28692,
           "False_Positives": 115,
           "False_Negatives": 0,
           "Recall": 1.0,
           "Precision": 0.8745910577971646,
           "F1": 0.9331006399069226,
           "Macro_F1": 0.9655503025618545,
           "FPR": 0.003992085257055577,
           "Benign_Specificity": 0.9960079147429445
       }
   }
   ```

### 2.3 Diagnosis & Remediation

- **Root Cause of Ambiguity**: In `docs/PHASE_12E_IMPLEMENTATION_REPORT.md`, the documentation narrative mistakenly designated TC-08 as "Zero-Day Detection Holdout (Backdoor)". However, the generator script `scripts/generate_verified_scenarios.py`, the cache file `backend/app/cache/TC-08.json`, the catalogue `backend/app/cache/scenarios.json`, and the frontend specification `frontend-react/src/types/scenario.ts` had already physically implemented `Held-Out Fuzzers Evaluation`.
- **Action Taken**:
  1. Updated `docs/PHASE_12E_IMPLEMENTATION_REPORT.md` replacing all errant references to Backdoor with `Held-Out Fuzzers Evaluation`.
  2. Adjusted `fuzzers_recall` in `backend/app/cache/TC-08.json` from approximate $65.36\%$ to the exact experimental metric $68.64\%$.
  3. Aligned `statusReason` in `frontend-react/src/types/scenario.ts` with the exact $68.64\%$ test metric on $1,400$ Fuzzers support flows.

---

## 3. Priority 2 — Verification of Live-Inference Scenarios

The live-inference scenarios (TC-01, TC-02, TC-03, TC-04, TC-06, TC-07) were audited against the data split and model inference logic:

| Scenario | Execution Mode | Dataset & Split | Underlying Model(s) | Grounded Evaluation Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | `LIVE_INFERENCE` | `NF-UNSW-NB15-v2` Test ($22.5\text{k}$) | `xgboost_detector.json` + `isolation_forest.joblib` | **Zero-Alert Benign Traffic**: 6 genuine benign test rows. XGBoost $p = 0.0000$; Isolation Forest anomaly scores $\in [-0.1255, -0.0282]$ (strictly below threshold $+0.0094$). $0$ alerts, $0$ correlation edges, $0$ MITRE techniques. |
| **TC-02** | `LIVE_INFERENCE` | `NF-UNSW-NB15-v2` Test ($22.5\text{k}$) | `xgboost_detector.json` | **Known Exploits**: 5 genuine exploit flows from test split. Supervised scores $p \in [0.9984, 0.9995]$. Correlated along exploit attack family; MITRE T1210. |
| **TC-03** | `LIVE_INFERENCE` | `NF-UNSW-NB15-v2` Test ($22.5\text{k}$) | `xgboost_detector.json` | **Known DoS / Generic**: 6 genuine test flows. Supervised scores $p \in [0.9959, 0.9999]$. Volumetric signature matching; MITRE T1499/T1498. |
| **TC-04** | `LIVE_INFERENCE` | `NF-UNSW-NB15-v2` Test ($22.5\text{k}$) | `isolation_forest.joblib` | **Behavioral Outlier**: 5 test flows. Supervised scores $p = 0.0000$, but anomaly scores $\in [0.0810, 0.1893]$ (exceeding threshold $+0.0094$). `detection_source: "ANOMALY"`. |
| **TC-06** | `LIVE_INFERENCE` | `NF-UNSW-NB15-v2` Test ($22.5\text{k}$) | `xgboost_detector.json` + `isolation_forest.joblib` | **Detector Agreement Consensus**: 6 test flows from the $533$ dual-positive population. $p \ge 0.5107$, anomaly scores $\ge 0.0113$. $100\%$ events exhibit `detection_source: "BOTH"`. |
| **TC-07** | `LIVE_INFERENCE` | `NF-UNSW-NB15-v2` Test ($22.5\text{k}$) | `xgboost_detector.json` + `isolation_forest.joblib` | **Detector Disagreement**: 3 flows with `xgb_pred=1, if_pred=0` (from $443$ test flows) and 3 flows with `xgb_pred=0, if_pred=1` (from $1,442$ test flows). Exhibits model complementarity. |

### Zero-Alert TC-01 Validation

Audit of `backend/app/cache/TC-01.json`:
- `events[0].supervised_score`: `0.0`
- `events[0].anomaly_score`: `-0.1255`
- `events[1].supervised_score`: `0.0`
- `events[1].anomaly_score`: `-0.0986`
- `events[2].supervised_score`: `0.0`
- `events[2].anomaly_score`: `-0.1170`
- `events[3].supervised_score`: `0.0`
- `events[3].anomaly_score`: `-0.0282`
- `events[4].supervised_score`: `0.0`
- `events[4].anomaly_score`: `-0.1082`
- `events[5].supervised_score`: `0.0`
- `events[5].anomaly_score`: `-0.0975`

**Conclusion**: The zero-alert state for TC-01 is mathematically authentic and results from true frozen model predictions on genuine normal network flows. No alerts were manually removed or suppressed.

---

## 4. Priority 3 — Verification of Evaluation Provenance

### 4.1 Discrimination: Live Inference vs Recorded Evaluation

- **Live Inference (`LIVE_INFERENCE`)**: Scenarios TC-01, TC-02, TC-03, TC-04, TC-06, and TC-07 represent active inference passing test-split flows through production models in memory.
- **Recorded Evaluation (`RECORDED_EVALUATION`)**: Scenarios TC-08 and TC-09 display pre-computed macro evaluation benchmarks from controlled zero-shot experiments (`experiments/unseen_attack/`), where entire attack families were excluded during training to test inductive generalization.

### 4.2 Exact Metrics Alignment

| Attribute | TC-08 (Fuzzers Holdout) | TC-09 (Reconnaissance Holdout) | Source of Truth Artifact |
| :--- | :--- | :--- | :--- |
| **Holdout Family** | `Fuzzers` | `Reconnaissance` | `experiments/unseen_attack/config.json` |
| **Training Samples** | $119,793$ (0 Fuzzers) | $120,391$ (0 Recon) | `experiments/unseen_attack/results.json` |
| **Total Test Support** | $30,207$ flows | $29,609$ flows | `experiments/unseen_attack/results.json` |
| **Held-Out Class Support** | $1,400$ flows | $802$ flows | `experiments/unseen_attack/results.json` |
| **True Positives (TP)** | $961$ | $802$ | `experiments/unseen_attack/results.json` |
| **Zero-Shot Recall** | **$68.64\%$** ($961 / 1,400$) | **$100.0\%$** ($802 / 802$) | `experiments/unseen_attack/results.json` |
| **Precision** | $93.12\%$ | $87.46\%$ | `experiments/unseen_attack/results.json` |
| **Macro F1** | $89.08\%$ (F1: $79.03\%$) | $96.56\%$ (F1: $93.31\%$) | `experiments/unseen_attack/results.json` |
| **False Positive Rate (FPR)** | $0.25\%$ ($71 / 28,807$) | $0.40\%$ ($115 / 28,807$) | `experiments/unseen_attack/results.json` |
| **Model Artifact** | `models/xgb_holdout_Fuzzers.json` | `models/xgb_holdout_Reconnaissance.json` | `experiments/unseen_attack/models/` |

---

## 5. Priority 4 — Regression Verification

### 5.1 Verification Script Execution

Executed automated script:
```powershell
.\.venv\Scripts\python.exe scripts/verify_phase12e1_regression.py
```

**Observed Output:**
```
=== 1. PRODUCTION & ARTIFACT INTEGRITY ===
  models/xgboost_detector.json: sha256=bdcfc8484749e204... (321463 bytes)
  models/isolation_forest.joblib: sha256=ac4e91ea7ef67bff... (2089821 bytes)
  models/feature_columns.json: sha256=dc1bb7b3cb41e12c... (822 bytes)
  experiments/unseen_attack/models/xgb_holdout_Fuzzers.json: sha256=baa9d09a0126dde5... (303334 bytes)
  experiments/unseen_attack/models/xgb_holdout_Reconnaissance.json: sha256=f0ed3cf34ed8a356... (314604 bytes)
  experiments/unseen_attack/results.json: sha256=cd8824ac9726f6df... (1051 bytes)
  experiments/unseen_attack/config.json: sha256=0eae41bcf7a28630... (396 bytes)

=== 2. TC-10 VERIFICATION ===
  TC-10 incident: INC_1
  Events: 8
  Edges: 20
  MITRE mappings: 4

=== 3. TC-05 DISABLED VERIFICATION ===
  TC-05 status: 404, detail: Scenario 'TC-05' is disabled: Autoencoder model weights do not exist on disk for live inference.

=== 4. SCENARIO-AWARE EXPLANATIONS ===
  TC-01: scenario_id=TC-01, incident_id=INC_TC01, provider=deterministic, fallback=True
  TC-02: scenario_id=TC-02, incident_id=INC_TC02, provider=groq, fallback=False
  TC-08: scenario_id=TC-08, incident_id=INC_TC08, provider=deterministic, fallback=True
  TC-10: scenario_id=TC-10, incident_id=INC_1, provider=deterministic, fallback=True

=== 5. TC-08 PHYSICAL EVIDENCE CHECK ===
  Holdout Family: Fuzzers
  Test Support: 1400 Fuzzers flows, 30207 total test flows
  Recall: 68.64% (961/1400)
  Precision: 93.12%
  F1: 79.03%
  FPR: 0.25%

=== ALL CHECKS PASSED SUCCESSFULLY ===
```

### 5.2 State Transition & Freshness Audit

1. **Incident Context Synchronization**: In `frontend-react/src/context/IncidentContext.tsx`, `selectScenario(id)` and `executeScenarioReplay(id)` invoke `loadScenarioData(id)` and `loadExplanation(id)` simultaneously.
2. **Stale View Prevention**:
   - `AttackGraph.tsx` observes `incident.events` and `incident.edges` directly. When switching to TC-01, it receives empty edges and cleanly renders a baseline notification with zero residual nodes from TC-10.
   - `MitreMapping.tsx` observes `incident.mitre_mappings` and re-indexes techniques exclusively for the active incident.
   - `AiExplanation.tsx` displays the active `explanation` object whose `scenario_id` matches `selectedScenarioId`.
3. **Report Generation Isolation**: In `AiExplanation.tsx`:
   - Download filename is explicitly templated: `ThreatWeave_${selectedScenarioId}_Incident_${incident.incident_id}_Report.md`.
   - Report body dynamically generates sections from `incident.events`, `incident.mitre_mappings`, and `explanation.summary`, ensuring no cross-contamination between scenarios.

---

## 6. Build & Test Execution Results

### 6.1 Backend Pytest Regression Suite

Command:
```powershell
$env:PYTHONPATH="backend"; .\.venv\Scripts\pytest.exe tests/test_scenarios_phase12e.py tests/test_scenario_explanation.py -v
```

**Results:**
```
======================= 17 passed, 2 warnings in 27.29s =======================
```
- Total tests: **17**
- Passed: **17 (100%)**
- Failed: **0**

### 6.2 React Frontend Production Build

Command:
```powershell
npm run build (in frontend-react/)
```

**Results:**
```
✓ 1606 modules transformed.
dist/index.html                   0.81 kB │ gzip:   0.45 kB
dist/assets/index-Dr9efc3C.css    9.39 kB │ gzip:   2.57 kB
dist/assets/index-CMU3Wn9z.js   719.83 kB │ gzip: 216.02 kB
✓ built in 29.14s
```
- TypeScript check (`tsc`): **Passed (0 errors)**
- Vite production build: **Passed (0 errors)**

### 6.3 Legacy Frontend Production Build

Command:
```powershell
npm run build (in frontend/)
```

**Results:**
```
✓ 8 modules transformed.
dist/index.html                   0.70 kB │ gzip:   0.40 kB
dist/assets/index-Dz0hM0O7.css    4.93 kB │ gzip:   1.47 kB
dist/assets/index-BHOUDNJS.js   449.09 kB │ gzip: 141.32 kB
✓ built in 814ms
```
- TypeScript check (`tsc`): **Passed (0 errors)**
- Vite production build: **Passed (0 errors)**

---

## 7. Discrepancy & Resolution Summary

| Discrepancy Identified | Affected Component | Resolution Implemented | Verification Status |
| :--- | :--- | :--- | :--- |
| **TC-08 Labeled as Backdoor in Doc** | `docs/PHASE_12E_IMPLEMENTATION_REPORT.md` | Corrected to `Held-Out Fuzzers Evaluation` with authoritative model `xgb_holdout_Fuzzers.json`. | Verified |
| **TC-08 Metric Inconsistency ($65.36\%$ vs $68.64\%$)** | `TC-08.json` & `scenario.ts` | Aligned to exact experimental result $68.64\%$ from `results.json` ($961/1,400$). | Verified |
| **TC-09 Metric Inconsistency ($0.22\%$ vs $0.40\%$ FPR)** | `TC-09.json` | Aligned to exact experimental result $0.40\%$ FPR from `results.json`. | Verified |

---

## 8. Readiness Recommendation

The ThreatWeave Phase 12E implementation has undergone a comprehensive provenance and regression audit with all 4 priority objectives satisfied:
- TC-08 identity is definitively resolved as **Held-Out Fuzzers Evaluation** with zero fabricated artifacts.
- All 6 live-inference scenarios are strictly grounded in genuine test-split flows and verified frozen model predictions.
- TC-08 and TC-09 recorded evaluations precisely mirror physical experimental benchmarks.
- Full regression tests pass across backend and both frontend builds without touching production weights or altering historical results.

The codebase is in an audited, clean, and stable state. In accordance with instructions, work stops here for user review.
