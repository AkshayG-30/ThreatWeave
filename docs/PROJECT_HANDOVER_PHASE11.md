# THREATWEAVE — PROJECT HANDOVER (PHASE 11)

## 1. Project Identity and Environment
- **Project name:** ThreatWeave
- **Hackathon:** Zephyr 2026
- **Problem Statement:** PS-9, “Mitigating Advanced Digital Threats and Securing Distributed Infrastructure”
- **Team Name:** FANTASTIC 4
- **Team ID:** MS-2026-0187
- **Project Root:** `D:\Zephyr\ThreatWeave`
- **Environment:** Windows, CPU-only.
- **Backend:** FastAPI, Python (Uvicorn)
- **Frontend:** Vanilla TypeScript, Vite (Current: `frontend/`), planned React migration (`frontend-react/`).

## 2. Original System Architecture
1. **Dataset Ingestion & Preprocessing:** Data loaded and numerical features normalized.
2. **Supervised Detection:** XGBoost production model identifies known threats.
3. **Anomaly Detection:** Isolation Forest and experimental Autoencoder flag behavioral outliers.
4. **Event Correlation:** Evidence-based correlation (e.g., shared IPs) bounded by time.
5. **Attack Graph Reconstruction:** NetworkX constructs a directed graph of the attack.
6. **MITRE ATT&CK Mapping:** Deterministic mapping of events to MITRE T-codes.
7. **AI Incident Explanation:** `LLMExplainer` uses Groq with a deterministic offline fallback.
8. **Dashboard:** Displays the pipeline output natively in the browser.

## 3. Production Models and Scientific Preservation
- **Production Models:** 
  - `models/xgboost_detector.json` (Frozen Production Supervised)
  - Isolation Forest (Frozen Production Anomaly)
- **Benchmarks (Experimental):**
  - Random Forest
  - LightGBM (`experiments/detection_benchmark/`)
  - Dense Autoencoder (`experiments/anomaly_benchmark/`)

*Critical Rule:* **Do not modify or retrain frozen production models.**

## 4. Datasets and Experimental Results
*Results are audited as recorded in previous phases. (See `PROJECT_HANDOVER_AUDIT.md` for specific validations).*
- **NF-UNSW-NB15-v2:** Primary dataset.
- **XGBoost:** F1 ~95.5%, Recall ~99.8%.
- **Autoencoder vs Isolation Forest:** Confirmed Autoencoder outperformed IF in specific anomaly recalls.
- **Cross-Dataset:** NF-CSE-CIC-IDS2018-v2 evaluated. F1 ~1.96%. Proves dataset shift is a real challenge.
- **Unraveled/SAGA Feasibility:** Audit completed. Real validation NOT implemented (requires adapter logic).
- **NF-ToN-IoT:** Audited and rejected due to missing features.
- **GRU/GNN:** Feasibility aborted due to lack of temporal/structural data. Not implemented.

## 5. Scenario System
- **Backend Service:** `DemoScenarioService` serves scenarios from `backend/app/cache/`.
- **Cache Generator:** `scripts/generate_demo_cache.py` caches real outputs safely.
- **TC-10:** Verified controlled multi-stage attack replay with 8 attack events and 1 noise event.
- **TC-01 through TC-09:** Currently unverified or incomplete due to time constraints in caching. 

## 6. Existing Frontend (Phase 10)
- **Current State:** Monolithic 14KB `Dashboard.ts`. 
- **Implemented:** URL-driven scenario selector (`?scenario=TC-10`), single-page scroll fix, graph edge-label cleanup, and Markdown report download.
- **Skipped:** Deep DOM state changes (React-like lifecycle) were skipped to preserve the functional demo.

## 7. Next Major Task: React Frontend Reconstruction
The user authorized a full frontend reconstruction in `D:\Zephyr\ThreatWeave\frontend-react`.
**Requirements:**
- React, TypeScript, Vite.
- Professional SOC styling (SentinelX-inspired).
- **Live Pipeline Visualization:** Real-time state machine of the 9 stages (Data Loading -> Report Ready).
- **Scenario Lab:** Fully functional TC-01 to TC-10 using cached backend data.
- **Preserve:** Scientific honesty. Do not fabricate scores or progress bars.

## 8. Safety Rules
1. Do not overwrite the current `frontend/` directory.
2. Do not modify production models.
3. Keep `GROQ_API_KEY` out of the frontend and Git.
4. Do not fabricate data.
5. Do not claim unfinished work (GNN, GRU, SAGA) is completed.

## 9. Repository Status
- **Git Status:** Git is not initialized in the project root.
- **Testing:** `pytest` passes 27/27 tests.
- **Frontend Build:** `npm run build` succeeds in `frontend/`.
- **Start Commands:** `uvicorn app.main:app` (Backend), `npm run dev` (Frontend).

## 10. Concrete Next-Phase Plan
1. Audit the repository.
2. Generate verified scenario fixtures for TC-01 through TC-09.
3. Scaffold `frontend-react`.
4. Build the shared layout and routing.
5. Implement the live execution pipeline state machine.
6. Build graph, MITRE, and AI views.
7. Switch demo presentation to the new React app only when fully verified.
