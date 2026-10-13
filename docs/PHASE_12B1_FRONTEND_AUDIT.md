# ThreatWeave — Phase 12B.1 Frontend Audit & Verification Document

**Document Path:** `docs/PHASE_12B1_FRONTEND_AUDIT.md`  
**Audit Date:** 2026-10-09  
**Target Applications:** 
- Frontend React: `D:\Zephyr\ThreatWeave\frontend-react`
- Existing Vanilla Frontend: `D:\Zephyr\ThreatWeave\frontend` (Untouched & runnable)
- Backend: `D:\Zephyr\ThreatWeave\backend` (Untouched, verified API)

---

## 1. Findings Before Changes

Following the initial scaffolding and user browser review, a thorough inspection revealed:
1. **Navigation Horizontal Clipping:** At desktop viewports around 1365px, having nine wide pill navigation buttons with long labels forced horizontal overflow and clipping on the right edge.
2. **Security Overview Pipeline Disconnect:** The command center displayed static status cards without a truthful representation of the nine-stage defensive pipeline, risking confusion between live network taps and controlled replays.
3. **Attack Graph Empty Placeholder:** The graph view rendered an uninitialized container rather than mounting the actual Cytoscape graph nodes and relationships.
4. **Isolated Noise Event Discrepancy:** Earlier summaries mentioned both "8 attack events" and "9 events with 1 noise event". Physical investigation revealed `backend/app/cache/TC-10.json` contains the 8 connected candidate incident events (`EV_01_RECON` through `EV_08_LATERAL`), whereas the Phase 3 replay experiment (`experiments/phase3/synthetic_replay_results.json`) demonstrated that `EV_09_NOISE` was tested and 100% isolated by the correlation engine.
5. **Scenario Selection Isolation:** TC-10 execution did not synchronize state with the Overview, MITRE, or Report views.
6. **Explanation Backend Route Constraints:** `GET /api/demo/explanation` hardcodes `experiments/phase4/synthetic_incident.json` and does not accept scenario identifiers; however, because `TC-10.json` is identical to `synthetic_incident.json`, TC-10 explanation is 100% physically aligned.
7. **Discrepancy in Handover LightGBM Claims:** Handover docs stated LightGBM had 99.84% accuracy, 97.78% F1, and 0.09% FPR. The actual physical artifact (`experiments/detection_benchmark/comparison.json`) proves the true values are **99.62% accuracy, 95.45% F1, 0.38% FPR, and 1.18s training time**.

---

## 2. Verified TC-10 Schema and Topology

Physical verification of [backend/app/cache/TC-10.json](file:///D:/Zephyr/ThreatWeave/backend/app/cache/TC-10.json) and [experiments/phase3/synthetic_replay_results.json](file:///D:/Zephyr/ThreatWeave/experiments/phase3/synthetic_replay_results.json):

### A. Candidate Incident Event Inventory (`INC_1`):
- **Total Correlated Events:** Exactly 8
- **Event List & Attributes:**
  1. `EV_01_RECON`: `10.0.0.5:1234 -> 192.168.1.10:80` (TCP, Anomaly p=0.8, Supervised p=0.1)
  2. `EV_02_RECON`: `10.0.0.5:1235 -> 192.168.1.11:80` (TCP, Anomaly p=0.8, Supervised p=0.1)
  3. `EV_03_SCAN`: `10.0.0.5:1236 -> 192.168.1.12:445` (TCP, Dual Consensus p=0.9, Supervised p=0.9)
  4. `EV_04_EXPLOIT`: `10.0.0.5:1237 -> 192.168.1.12:445` (TCP, Supervised p=0.99, Anomaly p=0.1)
  5. `EV_05_C2`: `192.168.1.12:4444 -> 185.15.2.1:8080` (TCP, Anomaly p=0.85, Supervised p=0.1)
  6. `EV_06_C2`: `192.168.1.12:4445 -> 185.15.2.1:8080` (TCP, Anomaly p=0.85, Supervised p=0.1)
  7. `EV_07_EXFIL`: `192.168.1.12:4446 -> 185.15.2.1:8080` (TCP, Dual Consensus p=0.9, Supervised p=0.9)
  8. `EV_08_LATERAL`: `192.168.1.12:5000 -> 192.168.1.15:445` (TCP, Supervised p=0.9, Anomaly p=0.2)
- **Isolated Noise Event (`EV_09_NOISE`):**
  - Origin: `8.8.8.8:123 -> 192.168.1.50:53` (UDP, Anomaly p=0.7)
  - Topology Status: Disconnected from candidate cluster; 0 edges; proves 100% noise isolation.

### B. Topology Edge Relationships:
- **Total Edges in `TC-10.json`:** Exactly 20 directed relationships
- **Edge Weight Range:** 1.00 to 1.70
- **Evidence Breakdown:**
  - `SAME_SOURCE_IP`: 8 edges
  - `SHARED_IP_PIVOT`: 8 edges
  - `SAME_SRC_AND_DST`: 4 edges
  - `DETECTION_AGREEMENT`: 4 edges
  - `TEMPORAL`: 20 edges (all edges bounded by 30.0s window)
- **Strength Classifications:** 16 Medium, 4 Strong

### C. Deterministic MITRE ATT&CK Mappings:
1. `T1046` (**Network Service Scanning**, Discovery): Mapped to `EV_01_RECON`, `EV_02_RECON`, `EV_03_SCAN` (High Confidence).
2. `T1210` (**Exploitation of Remote Services**, Lateral Movement): Mapped to `EV_04_EXPLOIT` (Medium Confidence).
3. `T1071` (**Application Layer Protocol**, Command & Control): Mapped to `EV_05_C2`, `EV_06_C2` (High Confidence).
4. `T1041` (**Exfiltration Over C2 Channel**, Exfiltration): Mapped to `EV_07_EXFIL` (Medium Confidence).

---

## 3. Metric and Claim Discrepancies Audited

| Experiment / Metric | Handover Document Claim | Physical Source File | Actual Verified Truth | Correction in Phase 12B.1 |
| :--- | :--- | :--- | :--- | :--- |
| **LightGBM Benchmark** | F1: 97.78%, FPR: 0.09%, Time: 0.47s | `experiments/detection_benchmark/comparison.json` | F1: 95.45%, FPR: 0.38%, Time: 1.18s | Updated UI to physical artifact truth. |
| **Test Set Support Sums** | Implied various counts | `experiments/phase2b/results.json` | 21,523 TN + 82 FP + 1 FN + 894 TP = **22,500** | Explicit confusion matrix table displays exact sum. |
| **Isolation Forest Confusion Sum** | Implied various counts | `experiments/phase2c/results.json` | 20,123 TN + 1,482 FP + 402 FN + 493 TP = **22,500** | Explicit confusion matrix table displays exact sum. |
| **Fuzzers Holdout Test Sum** | Stated 30k | `experiments/unseen_attack/results.json` | 28,736 TN + 71 FP + 439 FN + 961 TP = **30,207** | Documented exact holdout split sums. |
| **Reconnaissance Holdout Test Sum** | Stated 29k | `experiments/unseen_attack/results.json` | 28,692 TN + 115 FP + 0 FN + 802 TP = **29,609** | Documented exact holdout split sums. |
| **Real Cross-Dataset Test Sum** | Stated 17.1M | `experiments/cross_dataset_real/metrics.json` | 8,833,889 TN + 6,267,796 FP + 1,945,768 FN + 82,262 TP = **17,129,715** | Documented exact real dataset sums. |
| **Autoencoder Model Weights** | Stated model saved | `experiments/anomaly_benchmark/` | Weights NOT saved to disk; benchmark JSONs only. | UI labels AE as offline benchmark artifact; live inference disabled. |

---

## 4. Files Changed and Why

### Frontend (`frontend-react/`):
- `src/types/navigation.ts`: Shortened navigation labels to eliminate desktop horizontal clipping at ~1365px.
- `src/layouts/AppLayout.tsx`: Added active scenario pill (`Active: TC-10 [REPLAY]`), responsive tablet/mobile menu drawer, and backend health status.
- `src/styles/index.css`: Added responsive navbar media queries, 9-stage pipeline stepper layout, and compact card densities.
- `src/context/IncidentContext.tsx`: Built centralized incident state manager binding TC-10 telemetry, 9-stage pipeline simulation, explanation caching, and download generation.
- `src/data/tc10_fixture.json`: Direct local copy of `backend/app/cache/TC-10.json` ensuring seamless zero-latency fallback if API is offline.
- `src/pages/SecurityOverview.tsx`: Implemented 9-stage pipeline tracker with real stage outputs, honest replay labeling, and navigation to incident artifacts.
- `src/pages/ScenarioLab.tsx`: Bound active TC-10 execution with synchronized incident state; detailed prerequisite cards and honest disabled statuses for TC-01..TC-09.
- `src/pages/AttackGraph.tsx`: Built fully interactive Cytoscape graph canvas rendering the 8 attack chain nodes, 20 edges, isolated noise toggle (`EV_09_NOISE`), layout switcher, zoom/fit/reset controls, and node/edge inspection drawers.
- `src/pages/MitreMapping.tsx`: Dynamically populated from active incident `mitre_mappings` and `evidence_items`.
- `src/pages/AiExplanation.tsx`: Connected real explanation API with deterministic fallback detection, Groq indicators, and a one-click Markdown report generator (`.md` download).
- `src/pages/ModelEvaluation.tsx`: Replaced text summaries with tabbed comparisons, verified confusion matrices summing to 22,500, per-category recalls, and LightGBM correction.
- `src/pages/CrossDataset.tsx`: Documented the 17.1M flow evaluation, confusion matrix, 14-category detection breakdown, and ToN-IoT structural audit.
- `src/pages/UnseenAttack.tsx`: Added full confusion matrices and exact holdout split sums for Fuzzers and Reconnaissance.
- `src/pages/Methodology.tsx`: Embedded complete 5-stage ablation study table (Stages A through E) and supported vs unsupported claims audit.
- `src/App.tsx`: Wrapped application in `IncidentProvider`.

---

## 5. Functional Improvements Completed

1. **Zero Horizontal Clipping:** Tested at 1365px, 1280px, and 1024px; top command bar neatly fits all 9 routes and active scenario telemetry.
2. **Interactive TC-10 Execution:** Clicking "Execute Scenario" in Scenario Lab runs the 9-stage state machine and synchronizes incident data across Overview, Graph, MITRE, and Report.
3. **Live Cytoscape Attack Graph:**
   - Visualizes all 8 attack nodes with colors by detector type (`SUPERVISED`, `ANOMALY`, `BOTH`).
   - Visualizes all 20 evidence edges with directional arrows and line weights by confidence (`STRONG` vs `MEDIUM`).
   - Toggle to inspect `EV_09_NOISE` proving 100% noise isolation.
   - Node and edge selection drawers exposing raw ports, IPs, timestamps, and multi-signal reasons.
   - Zoom in, Zoom out, Fit View, and Reset Layout fully functional.
4. **Deterministic MITRE Anchoring:** T-codes (T1046, T1210, T1071, T1041) linked to raw event IDs.
5. **Report Download:** Generates formatted markdown file (`ThreatWeave_TC-10_Incident_INC_1_Report.md`) with complete executive summary, MITRE classifications, flow telemetry table, and limitations.

---

## 6. Tests Run and Exact Results

### 1. `frontend-react` Production Build (`tsc && vite build`)
```powershell
> frontend-react@1.0.0 build
> tsc && vite build

vite v6.2.1 building for production...
transforming...
✓ 40 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.82 kB │ gzip:   0.45 kB
dist/assets/index-B7jGf31j.css    9.14 kB │ gzip:   2.36 kB
dist/assets/index-BL8V3Vl6.js   464.71 kB │ gzip: 147.21 kB
✓ built in 709ms
```
**Result:** **PASSED (Exit Code: 0)**

### 2. Existing Vanilla Frontend Production Build (`frontend/`)
```powershell
> frontend@0.0.0 build
> tsc && vite build

vite v8.3.4 building client environment for production...
transforming...
✓ 8 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.70 kB │ gzip:   0.40 kB
dist/assets/index-Dz0hM0O7.css    4.93 kB │ gzip:   1.47 kB
dist/assets/index-BHOUDNJS.js   449.09 kB │ gzip: 141.32 kB
✓ built in 339ms
```
**Result:** **PASSED (Exit Code: 0, completely untouched)**

### 3. Backend Pytest Suite
```powershell
$env:PYTHONPATH="backend"; .\.venv\Scripts\pytest -q
...........................                                              [100%]
27 passed, 2 warnings in 4.32s
```
**Result:** **PASSED (27 passed, 0 failed)**

### 4. HTTP API Endpoint Verification
- `GET http://127.0.0.1:8000/health`: HTTP 200 `{"status": "ok", "service": "ThreatWeave"}`
- `GET http://127.0.0.1:8000/api/demo/scenario/TC-10`: HTTP 200 `incident_id: INC_1`, `event_count: 8`
- `GET http://127.0.0.1:8000/api/demo/explanation`: HTTP 200 `summary`: "Candidate incident contains 8 correlated events..."

---

## 7. Known Remaining Gaps

1. **Scenarios TC-01 through TC-09 Live Execution:** Scenarios TC-01 through TC-09 remain visibly disabled in the Scenario Lab. They require dedicated JSON cache fixtures or inference pipeline scripts to be created in a subsequent phase before they can be marked executable.
2. **Autoencoder Live Inference:** Weights were not persisted during Phase 2C; live inference remains disabled, presenting static verified benchmark metrics only.
3. **External LLM Quota:** The Groq explainer gracefully defaults to the verified deterministic offline fallback engine when API rate limits or network limits are hit.

---

## 8. Recommendation

**Status:** **READY FOR PHASE 12C**

The React application now possesses a verified, truthful, and fully functional TC-10 demonstration, an interactive Cytoscape attack graph, synchronized incident context, honest scenario catalogues, and verified metric claims. All 27 backend tests pass and both frontend production builds succeed cleanly.
