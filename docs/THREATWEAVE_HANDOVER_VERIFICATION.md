# ThreatWeave Handover Verification and Continuation Report

**Project:** ThreatWeave  
**Current Project Root:** `d:\Hackathon\ThreatWeave`  
**Previous Documented Root:** `D:\Zephyr\ThreatWeave`  
**Date of Audit:** October 14, 2026  
**Auditor:** Google DeepMind Agentic Pair Programmer (Antigravity IDE)  
**Verification Baseline:** Post-Phase 12F Demonstration Freeze  
**Overall Status:** **VERIFIED & REPRODUCED** (Zero application code modified; tests and builds reproduced with 100% fidelity)

---

## 1. Executive Summary & Verification Matrix

This verification report establishes the operational and scientific integrity of the ThreatWeave repository following extraction. In accordance with strict kick-start protocols:
- **No application code, model binaries, thresholds, or scenario caches were modified.**
- **No destructive cleanup commands or ad-hoc package updates were performed.**
- **All reported claims were independently rerun and audited against actual command executions.**

### Master Verification Status

| Item | Status | Verification Detail |
| :--- | :---: | :--- |
| **Original Handover Document** | **VERIFIED** | [`docs/THREATWEAVE_COMPLETE_HANDOVER.md`](file:///d:/Hackathon/ThreatWeave/docs/THREATWEAVE_COMPLETE_HANDOVER.md) (45,123 bytes, 595 lines) was found and thoroughly reviewed. |
| **Directory Structure** | **VERIFIED** | Full project tree intact (`backend/`, `frontend-react/`, `frontend/`, `models/`, `experiments/`, `scripts/`, `tests/`, `data/`, `docs/`). |
| **Production Model Inventory** | **VERIFIED** | XGBoost (`models/xgboost_detector.json`) and Isolation Forest (`models/isolation_forest.joblib`) match byte counts exactly. |
| **Experimental Model Inventory** | **VERIFIED** | Random Forest baseline, LightGBM, and held-out zero-shot models (`xgb_holdout_Fuzzers.json`, `xgb_holdout_Reconnaissance.json`) exist on disk. |
| **Scenario Cache Catalogue** | **VERIFIED** | TC-01 through TC-10 (except TC-05) exist in `backend/app/cache/`. TC-05 is explicitly disabled by design. |
| **Backend Test Suite (Pytest)** | **VERIFIED (RERUN)** | 44 of 44 tests passed in 45.76s (100% pass rate). |
| **React Frontend Build** | **VERIFIED (RERUN)** | `npm run build` in `frontend-react` completed in 3.78s with 0 errors (identical hash `index-DtU-q1Nn.js`, 719.86 kB). |
| **Legacy Frontend Build** | **VERIFIED (RERUN)** | `npm run build` in `frontend` completed in 342ms with 0 errors (identical hash `index-BN5Brtut.js`, 449.10 kB). |
| **Backend FastAPI Service** | **VERIFIED (RERUN)** | Service launched on port 8000; endpoints `/health`, `/api/demo/scenarios`, `TC-01`, `TC-10` verified HTTP 200; `TC-05` verified HTTP 404. |
| **React Frontend Dev Server** | **VERIFIED (RERUN)** | Vite v6.4.4 dev server launched on port 5173 ready in 316ms. |
| **Secrets & Isolation** | **VERIFIED** | `.env` securely configured; `GROQ_API_KEY` isolated to backend only; no secrets exposed in client bundles. |
| **Git Repository** | **UNVERIFIED** | Not a git repository (`fatal: not a git repository`). |

---

## 2. Project Root & Directory Structure

- **Physical Extracted Path:** `d:\Hackathon\ThreatWeave`
- **Discrepancy Note:** The original handover documents refer to `D:\Zephyr\ThreatWeave`. All relative path references inside code and configuration function normally under `d:\Hackathon\ThreatWeave`.

```
d:\Hackathon\ThreatWeave/
├── .env                              # Backend environment configuration (contains GROQ_API_KEY)
├── .env.example                      # Template environment configuration
├── .gitignore                        # Git exclusion rules
├── .pytest_cache/                    # Pytest caching directory
├── .venv/                            # Extracted Python virtual environment (site-packages intact)
├── README.md                         # Project overview and architecture guide
├── backend/
│   ├── requirements.txt              # Pinned Python package dependencies
│   └── app/
│       ├── main.py                   # FastAPI REST API entrypoint
│       ├── cache/                    # Pre-computed verified scenario caches (TC-01 to TC-10)
│       ├── schemas/                  # Pydantic data contract definitions
│       ├── services/                 # Detection pipeline, correlation, MITRE, LLM services
│       └── utils/                    # Common backend utilities
├── data/
│   ├── metadata/                     # Profiling, dataset policies, and MITRE schemas
│   ├── processed/                    # Primary 150k sample: nf_unsw_nb15_v2_sample_150k.csv (27.7 MB)
│   ├── raw/                          # Raw datasets: NF-CSE-CIC-IDS2018-V2, NF-ToN-IoT, NF-UNSW-NB15-v2
│   └── samples/                      # Auxiliary sample workspace
├── docs/                             # 18 audit, architecture, and validation reports
├── experiments/                      # 14 benchmark directories (detection, anomaly, unseen_attack, etc.)
├── frontend/                         # Legacy Vanilla TypeScript + Vite dashboard
├── frontend-react/                   # Primary React 18 + Vite SOC dashboard
├── models/                           # Frozen model weights and feature column definitions
├── notebooks/                        # Exploratory notebooks (currently empty)
├── scripts/                          # 20 training, cache generation, and validation scripts
└── tests/                            # 8 pytest files covering 44 automated test cases
```

---

## 3. Original Handover Document Review

The primary handover document [`docs/THREATWEAVE_COMPLETE_HANDOVER.md`](file:///d:/Hackathon/ThreatWeave/docs/THREATWEAVE_COMPLETE_HANDOVER.md) was found and thoroughly inspected. It accurately establishes:
1. **Scientific Integrity Rules:** Pre-computed scenario caches vs. live model inferences are explicitly distinguished.
2. **Phase 12F Verification Baseline:** Master checklist of 20 verification checks.
3. **Execution Reality:** Replays serve offline-generated model predictions to eliminate disk I/O latency, guaranteeing sub-10ms response times for demonstrations.
4. **TC-05 Policy:** Deep Autoencoder is deliberately disabled due to absence of serialized inference weights on disk.
5. **On-Demand LLM Triggering:** Groq API calls are restricted to explicit button clicks to prevent quota exhaustion and cost spikes.

---

## 4. Major Components and Source Paths

| Component | Technology | Primary Source File | Role & Operational Reality |
| :--- | :--- | :--- | :--- |
| **FastAPI Backend** | FastAPI / Uvicorn | [`backend/app/main.py`](file:///d:/Hackathon/ThreatWeave/backend/app/main.py) | Exposes `/health`, `/api/demo/incident`, `/api/demo/explanation`, `/api/demo/scenarios`, `/api/demo/scenario/{id}`. |
| **Demo Scenario Service** | Python / JSON Cache | [`backend/app/services/demo_scenario_service.py`](file:///d:/Hackathon/ThreatWeave/backend/app/services/demo_scenario_service.py) | Whitelists scenario IDs and streams pre-computed incident payloads. |
| **LLM Explainer** | Groq SDK / Rule Fallback | [`backend/app/services/llm_explainer.py`](file:///d:/Hackathon/ThreatWeave/backend/app/services/llm_explainer.py) | Grounded prompt generator with deterministic air-gapped fallback. |
| **Bounded Correlation Engine** | NetworkX | [`backend/app/services/correlation.py`](file:///d:/Hackathon/ThreatWeave/backend/app/services/correlation.py) | Sliding time-window ($\Delta t \le 30\text{s}$) and entity-sharing attack graph builder. |
| **MITRE ATT&CK Mapper** | Python Heuristics | [`backend/app/services/mitre_mapper.py`](file:///d:/Hackathon/ThreatWeave/backend/app/services/mitre_mapper.py) | Deterministic mapping of flow signatures to MITRE ATT&CK technique IDs. |
| **Data Ingestion Pipeline** | Pandas / Scikit-learn | [`backend/app/services/pipeline.py`](file:///d:/Hackathon/ThreatWeave/backend/app/services/pipeline.py) | StandardScaler normalization, categorical encoding, NaN elimination. |
| **React SOC Dashboard** | React 18 / TypeScript / Vite | [`frontend-react/src/App.tsx`](file:///d:/Hackathon/ThreatWeave/frontend-react/src/App.tsx) | Primary analyst interface featuring 9 specialized SOC views. |
| **Incident Context Provider** | React Context API | [`frontend-react/src/context/IncidentContext.tsx`](file:///d:/Hackathon/ThreatWeave/frontend-react/src/context/IncidentContext.tsx) | Synchronizes scenario selection, replay animations, and attack graph state. |
| **Cytoscape Attack Graph** | Cytoscape.js | [`frontend-react/src/pages/AttackGraph.tsx`](file:///d:/Hackathon/ThreatWeave/frontend-react/src/pages/AttackGraph.tsx) | Interactive directed attack chain visualization and node inspector HUD. |
| **Scenario Lab** | React Component | [`frontend-react/src/pages/ScenarioLab.tsx`](file:///d:/Hackathon/ThreatWeave/frontend-react/src/pages/ScenarioLab.tsx) | Replay cockpit for test cases TC-01 through TC-10. |
| **Legacy Frontend** | Vanilla TypeScript / Vite | [`frontend/src/main.ts`](file:///d:/Hackathon/ThreatWeave/frontend/src/main.ts) | Secondary lightweight dashboard maintained for backward compatibility. |

---

## 5. Verified Production and Experimental Model Inventory

| Model Name | Type | Physical Artifact | Byte Size | Status | Operational Role |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **XGBoost Detector** | Supervised GBDT | [`models/xgboost_detector.json`](file:///d:/Hackathon/ThreatWeave/models/xgboost_detector.json) | 321,463 | **VERIFIED** | Production classifier ($p \ge 0.51$). Source of scores in TC-01, TC-02, TC-03, TC-06, TC-07. |
| **Isolation Forest** | Unsupervised Trees | [`models/isolation_forest.joblib`](file:///d:/Hackathon/ThreatWeave/models/isolation_forest.joblib) | 2,089,821 | **VERIFIED** | Production anomaly detector ($s > 0.0094$). Source of scores in TC-01, TC-04, TC-06, TC-07. |
| **Random Forest Baseline** | Supervised Ensemble | [`models/random_forest_baseline.joblib`](file:///d:/Hackathon/ThreatWeave/models/random_forest_baseline.joblib) | 6,375,113 | **VERIFIED** | Comparative baseline; 100 estimators. |
| **Feature Columns Schema** | Metadata / Columns | [`models/feature_columns.json`](file:///d:/Hackathon/ThreatWeave/models/feature_columns.json) | 822 | **VERIFIED** | 41 standardized feature names matching NetFlow v2 schema. |
| **LightGBM Benchmark** | Supervised GBDT | [`experiments/detection_benchmark/lightgbm_model.txt`](file:///d:/Hackathon/ThreatWeave/experiments/detection_benchmark/lightgbm_model.txt) | 341,743 | **VERIFIED** | Baseline benchmark model. |
| **Held-Out Fuzzers XGB** | Zero-Shot Supervised | [`experiments/unseen_attack/models/xgb_holdout_Fuzzers.json`](file:///d:/Hackathon/ThreatWeave/experiments/unseen_attack/models/xgb_holdout_Fuzzers.json) | 303,334 | **VERIFIED** | Source of TC-08 recorded evaluation (68.64% zero-shot recall). |
| **Held-Out Recon XGB** | Zero-Shot Supervised | [`experiments/unseen_attack/models/xgb_holdout_Reconnaissance.json`](file:///d:/Hackathon/ThreatWeave/experiments/unseen_attack/models/xgb_holdout_Reconnaissance.json) | 314,604 | **VERIFIED** | Source of TC-09 recorded evaluation (100.0% zero-shot recall). |
| **Deep MLP Autoencoder** | Neural Reconstruction | Script only: `scripts/run_autoencoder_anomaly.py` | N/A | **DISABLED** | No saved weights exist on disk. Correctly blocked as TC-05. |

---

## 6. Scenario Execution Modes and Data Provenance

All 10 scenarios in the catalogue are governed by explicit execution modes and provenance records:

| Scenario ID | Name | Execution Mode | Click-Time Inference? | Provenance Source | Status |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **TC-01** | Benign Traffic Baseline | `LIVE_INFERENCE` | No (Cached) | 5 benign flows from untouched test split (`NF-UNSW-NB15-v2`). $p \le 0.0001$, 0 alerts. | **VERIFIED** |
| **TC-02** | Known Attack — Exploits | `LIVE_INFERENCE` | No (Cached) | 5 exploit flows from test split. $p \in [0.9984, 0.9995]$, MITRE T1210. | **VERIFIED** |
| **TC-03** | Known Attack — Generic / DoS | `LIVE_INFERENCE` | No (Cached) | 6 DoS flows from test split. $p \ge 0.995$, MITRE T1498/T1499. | **VERIFIED** |
| **TC-04** | Isolation Forest Anomaly | `LIVE_INFERENCE` | No (Cached) | 5 anomaly flows where supervised $p=0.0$, outlier $s > 0.081$, MITRE T1071. | **VERIFIED** |
| **TC-05** | Autoencoder Anomaly | `DISABLED` | No (Blocked) | Offline research benchmark; returns HTTP 404 with exact diagnostic rationale. | **VERIFIED** |
| **TC-06** | Detector Agreement | `LIVE_INFERENCE` | No (Cached) | 6 consensus flows where both XGBoost ($p \ge 0.51$) and Isolation Forest ($s > 0.0094$) trigger. | **VERIFIED** |
| **TC-07** | Detector Disagreement | `LIVE_INFERENCE` | No (Cached) | 3 XGBoost-only flows ($p > 0.99$) + 3 Isolation Forest-only flows ($s > 0.039, p=0.0$). | **VERIFIED** |
| **TC-08** | Held-Out Fuzzers Evaluation | `RECORDED_EVALUATION` | No (Cached) | 5 Fuzzers flows evaluated against holdout model `xgb_holdout_Fuzzers.json` (68.64% recall). | **VERIFIED** |
| **TC-09** | Held-Out Reconnaissance | `RECORDED_EVALUATION` | No (Cached) | 5 Recon flows evaluated against holdout model `xgb_holdout_Reconnaissance.json` (100% recall). | **VERIFIED** |
| **TC-10** | Controlled Multi-Stage APT Replay | `CONTROLLED_REPLAY` | No (Cached) | Synthetic benchmark fixture (8 attack events, 20 edges, 1 isolated noise node `EV_NOISE_99`). | **VERIFIED** |

---

## 7. Dependency and Environment Requirements

### Python Environment
- **Target Version:** Python 3.12 (Host has Python 3.12.10 installed at `C:\Users\wdrag\AppData\Local\Microsoft\WindowsApps\python.exe`).
- **Core Dependencies (all present in `.venv/Lib/site-packages`):**
  - `fastapi==0.111.0`
  - `uvicorn==0.30.1`
  - `pydantic==2.8.2`
  - `python-dotenv==1.0.1`
  - `pandas==2.2.2`
  - `numpy==1.26.4`
  - `scikit-learn==1.5.0`
  - `xgboost==2.0.3`
  - `networkx==3.3`
  - `pytest==9.1.1`

### Node.js / Frontend Environment
- **Node.js:** v24.15.0 (at `C:\Program Files\nodejs\node.exe`)
- **npm:** 11.12.1
- **React Frontend Dependencies (`frontend-react/`):** React 18.3.1, Cytoscape 3.30.4, Lucide React 0.475.0, Vite 6.1.0/6.4.4. All modules installed in `frontend-react/node_modules`.

### Environment Configurations
- **Backend Root `.env`:** Configured with `GROQ_API_KEY` (redacted in public documentation) and `MODEL_THRESHOLD=0.85`.
- **Frontend `.env` (`frontend-react/.env`):** Configured with `VITE_API_BASE_URL=http://127.0.0.1:8000`.

---

## 8. Test and Build Results (Actual Rerun vs. Historical)

All verification commands were physically rerun during this inspection. Results are compared side-by-side with historical reported figures:

### 8.1 Backend Pytest Suite

- **Actual Rerun Command:**
  ```powershell
  $env:PYTHONPATH="backend;.venv\Lib\site-packages"
  & "C:\Users\wdrag\AppData\Local\Microsoft\WindowsApps\python.exe" -m pytest tests/
  ```
- **Actual Rerun Output:**
  ```
  ============================= test session starts =============================
  platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
  rootdir: D:\Hackathon\ThreatWeave
  plugins: anyio-4.15.1
  collected 44 items

  tests\test_correlation.py ........                                       [ 18%]
  tests\test_health.py .                                                   [ 20%]
  tests\test_ml.py .....                                                   [ 31%]
  tests\test_phase4.py .....                                               [ 43%]
  tests\test_pipeline.py ......                                            [ 56%]
  tests\test_scenario_explanation.py .......                               [ 72%]
  tests\test_scenarios_phase12e.py ..........                              [ 95%]
  tests\test_schema.py ..                                                  [100%]

  ======================= 44 passed, 2 warnings in 45.76s =======================
  ```
- **Historical Reported (Phase 12F):** `44 passed, 2 warnings in 77.67s`.
- **Status:** **VERIFIED RERUN** ($100\%$ pass rate; all 44 test cases succeeded).

### 8.2 React Frontend Production Build

- **Actual Rerun Command (in `frontend-react`):**
  ```powershell
  npm run build
  ```
- **Actual Rerun Output:**
  ```
  > frontend-react@1.0.0 build
  > tsc && vite build

  vite v6.4.4 building for production...
  transforming...
  ✓ 1606 modules transformed.
  rendering chunks...
  computing gzip size...
  dist/index.html                   0.81 kB │ gzip:   0.45 kB
  dist/assets/index-Dr9efc3C.css    9.39 kB │ gzip:   2.57 kB
  dist/assets/index-DtU-q1Nn.js   719.86 kB │ gzip: 216.31 kB

  ✓ built in 3.78s
  ```
- **Historical Reported (Phase 12F):** `✓ 1606 modules transformed. dist/assets/index-DtU-q1Nn.js (719.86 kB). Built in 25.83s with 0 errors.`
- **Status:** **VERIFIED RERUN** (Zero TypeScript errors, exact asset hash reproduction).

### 8.3 Legacy Frontend Production Build

- **Actual Rerun Command (in `frontend`):**
  ```powershell
  npm run build
  ```
- **Actual Rerun Output:**
  ```
  > frontend@0.0.0 build
  > tsc && vite build

  vite v8.3.4 building client environment for production...
  transforming...
  ✓ 8 modules transformed.
  rendering chunks...
  computing gzip size...
  dist/index.html                   0.70 kB │ gzip:   0.40 kB
  dist/assets/index-Dz0hM0O7.css    4.93 kB │ gzip:   1.47 kB
  dist/assets/index-BN5Brtut.js   449.10 kB │ gzip: 141.32 kB

  ✓ built in 342ms
  ```
- **Historical Reported (Phase 12F):** `✓ 8 modules transformed. dist/assets/index-BN5Brtut.js (449.10 kB). Built in 663ms/696ms with 0 errors.`
- **Status:** **VERIFIED RERUN** (Zero errors, exact asset hash reproduction).

### 8.4 Backend API Endpoint Live Verification

- **Command:** Launched FastAPI with Uvicorn and issued HTTP requests:
  - `GET http://127.0.0.1:8000/health` $\to$ `{"status": "ok", "service": "ThreatWeave"}` (**HTTP 200**)
  - `GET http://127.0.0.1:8000/api/demo/scenarios` $\to$ Returned 10-scenario catalogue (**HTTP 200**)
  - `GET http://127.0.0.1:8000/api/demo/scenario/TC-01` $\to$ Returned Benign Baseline incident payload (**HTTP 200**)
  - `GET http://127.0.0.1:8000/api/demo/scenario/TC-10` $\to$ Returned Multi-Stage APT incident payload (**HTTP 200**)
  - `GET http://127.0.0.1:8000/api/demo/scenario/TC-05` $\to$ Returned `{"detail": "Scenario 'TC-05' is disabled: Autoencoder model weights do not exist on disk for live inference."}` (**HTTP 404**)
- **Status:** **VERIFIED RERUN**.

---

## 9. Discrepancies, Missing Items, and Environment Notes

1. **Host-Specific Python Path in `.venv/pyvenv.cfg`:**
   - *Finding:* `.venv/pyvenv.cfg` contains:
     ```
     home = C:\Users\ADMIN\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0
     executable = C:\Users\ADMIN\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe
     ```
   - *Impact:* Invoking `.\.venv\Scripts\python.exe` directly prints: `No Python at 'C:\Users\ADMIN\...` because on the current machine the user profile is `wdrag`, where Python 3.12.10 is installed at `C:\Users\wdrag\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe`.
   - *Status:* Discrepancy reported. Does not impede execution when system Python 3.12 is invoked with the existing `.venv/Lib/site-packages` in `PYTHONPATH`. Updating `pyvenv.cfg` requires simple text replacement if authorized.

2. **Project Directory Path:**
   - *Finding:* Extracted root is `d:\Hackathon\ThreatWeave`. Handover documents reference `D:\Zephyr\ThreatWeave`.
   - *Impact:* No functional impact since code relies on relative paths.

3. **`py` Command Not on PATH:**
   - *Finding:* Windows `py` launcher is not installed/mapped on PATH.
   - *Impact:* Use `python.exe` or `python3.12.exe` directly.

4. **Git Repository Uninitialized:**
   - *Finding:* `git status` outputs `fatal: not a git repository`.
   - *Impact:* The extracted directory is an unversioned folder.

5. **Legacy Frontend `.env`:**
   - *Finding:* `frontend/` contains `.env.example` but no `.env`.
   - *Impact:* The primary frontend is `frontend-react/`, which has a fully configured `.env`.

---

## 10. Documented vs. Actual Startup Procedures

### Recommended Startup Procedure for Current Machine

#### 1. Backend Service (FastAPI)
From the project root (`d:\Hackathon\ThreatWeave`):
```powershell
$env:PYTHONPATH="backend;.venv\Lib\site-packages"
& "C:\Users\wdrag\AppData\Local\Microsoft\WindowsApps\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
*(Alternatively, if `pyvenv.cfg` is updated to the `wdrag` user path, standard `.\.venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000` is used).*

- **Health Check:** `http://127.0.0.1:8000/health`
- **Scenarios Endpoint:** `http://127.0.0.1:8000/api/demo/scenarios`

#### 2. Primary Frontend (React SOC Dashboard)
From a separate PowerShell terminal:
```powershell
cd d:\Hackathon\ThreatWeave\frontend-react
npm run dev
```
- **Dashboard URL:** `http://localhost:5173`

---

## 11. Statement of File Modifications

> **Explicit Audit Statement:**  
> During this initial inspection and verification kick-start:
> - **ZERO** application code files were modified.
> - **ZERO** model files or weights were modified or retrained.
> - **ZERO** scenario cache files or datasets were altered.
> - **ZERO** packages were installed, updated, or removed.
> - Only this verification report ([`docs/THREATWEAVE_HANDOVER_VERIFICATION.md`](file:///d:/Hackathon/ThreatWeave/docs/THREATWEAVE_HANDOVER_VERIFICATION.md)) was created.

---

## 12. Current Project Status & Safest Next Steps

### Current Status
ThreatWeave is in a **fully operational, frozen, and demonstration-ready state**. All automated tests pass, the React SOC interface builds cleanly with identical artifact hashes, and backend scenario caches serve deterministic incident payloads.

### Safest Next Steps
1. **User Alignment:** Await explicit instruction regarding whether the user wishes to update `pyvenv.cfg` to point to the local `wdrag` user directory for standard virtualenv activation convenience.
2. **Preserve Freeze:** Continue enforcing the zero-code-change policy on model weights, thresholds, and backend contracts.
3. **Rehearsal & Demonstration:** Follow the documented 10-minute presentation guide and 4-minute demonstration sequence (TC-01 $\to$ TC-02 $\to$ TC-10) in [`docs/THREATWEAVE_COMPLETE_HANDOVER.md`](file:///d:/Hackathon/ThreatWeave/docs/THREATWEAVE_COMPLETE_HANDOVER.md).
