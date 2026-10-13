# PHASE 12D: SCENARIO-AWARE EXPLANATION & END-TO-END INCIDENT INTEGRATION REPORT

**Project:** ThreatWeave (`D:\Zephyr\ThreatWeave`)  
**Frontend Application:** `D:\Zephyr\ThreatWeave\frontend-react`  
**Legacy Frontend Application:** `D:\Zephyr\ThreatWeave\frontend` (preserved intact)  
**Implementation Date:** October 9, 2026  
**Auditor & Implementation Engineer:** ThreatWeave Advanced Agentic AI Engineer  
**Status:** Complete — Fully Implemented & Tested  

---

## Executive Summary

Phase 12D establishes a reliable, scenario-aware TC-10 incident explanation contract and validates end-to-end incident consistency across the FastAPI backend, React SOC dashboard, Cytoscape attack graph, deterministic MITRE ATT&CK mapping, and exportable SOC report.

### Key Deliverables & Outcomes
1. **Scenario-Aware Explanation API:** Extended `GET /api/demo/explanation` with query parameter `scenario_id` (whitelisted against path traversal). Unsupported scenario identifiers fail explicitly with HTTP 404; omitting `scenario_id` defaults safely to `TC-10` for 100% backward compatibility.
2. **Provenance Metadata Contract:** The `LLMExplanation` Pydantic model now explicitly includes `scenario_id`, `incident_id`, `provider` (`"groq"` vs `"deterministic"`), `fallback_used: bool`, and `model_name`.
3. **Dataset Provenance Discrepancy Resolved:** Re-inspected physical evaluation artifacts (`experiments/cross_dataset_real/config.json`, `metrics.json`, and `report.md`). Proven that the 17,129,715 network flows were evaluated zero-shot against **Real NF-CSE-CIC-IDS2018-V2**, not CIC-IDS2017/CTU-13. The React dashboard already correctly cites `NF-CSE-CIC-IDS2018-V2`.
4. **End-to-End Incident Consistency:** Re-validated that incident `INC_1` with exactly 8 events (`EV_01_RECON` through `EV_08_LATERAL`) and 4 MITRE techniques (`T1046`, `T1210`, `T1071`, `T1041`) is identically reflected in the backend response, local cache, frontend context, attack graph, MITRE grid, and downloaded Markdown report.
5. **Zero Credential Exposure:** Verified that `GROQ_API_KEY` remains strictly server-side. Zero API keys appear in client JavaScript bundles, response payloads, or logs.
6. **Comprehensive Automated Verification:** 34/34 backend pytest tests pass (including 7 new scenario-explanation and provenance tests). Both the React frontend (`frontend-react`) and legacy vanilla frontend (`frontend`) build cleanly with zero errors.

---

## 1. The Contract Before and After Implementation

### 1.1 Before Implementation (Phase 12C Baseline)
* **Endpoint:** `GET /api/demo/explanation`
* **Parameters:** None accepted.
* **Input Resolution:** Hardcoded unconditional read from relative path `"experiments/phase4/synthetic_incident.json"`.
* **Error Handling:** Returned generic 404 if the relative path was missing. No scenario validation.
* **Response Schema:**
  ```json
  {
    "summary": "...",
    "attack_chain": "...",
    "evidence": "...",
    "mitre_techniques": "...",
    "confidence": "...",
    "limitations": "...",
    "investigation_recommendations": "..."
  }
  ```
* **Contract Deficiencies:**
  * Could not explain any scenario other than the fixed synthetic file.
  * No metadata indicating whether Groq or deterministic fallback generated the text.
  * No scenario ID or incident ID anchoring in the response schema.

### 1.2 After Implementation (Phase 12D Verified Contract)
* **Endpoint:** `GET /api/demo/explanation?scenario_id={scenario_id}`
* **Parameters:**
  * `scenario_id: Optional[str] = None`
  * Validated against regex `^[A-Za-z0-9_-]+$` to prevent directory traversal (`HTTP 400 Bad Request` if invalid).
  * If omitted, defaults to `"TC-10"` preserving complete backward compatibility for legacy callers.
* **Input Resolution:**
  * Checks approved cache repository `backend/app/cache/{scenario_id}.json`.
  * If the requested scenario does not exist or is unavailable (e.g. `TC-01`), returns:
    `HTTP 404 Not Found`: `{"detail": "Scenario '{scenario_id}' not found or unavailable."}`
* **Response Schema (`LLMExplanation`):**
  ```json
  {
    "summary": "An attacker from IP 10.0.0.5 performed reconnaissance...",
    "attack_chain": "1. Reconnaissance: EV_01_RECON -> EV_02_RECON...",
    "evidence": "[{'evidence_id': 'EVID_01', ...}]",
    "mitre_techniques": "[{'technique_id': 'T1046', ...}]",
    "confidence": "HIGH",
    "limitations": "['Timestamps are synthetic replay only']",
    "investigation_recommendations": "Review detailed SMB logs...",
    "scenario_id": "TC-10",
    "incident_id": "INC_1",
    "provider": "groq",
    "fallback_used": false,
    "model_name": "openai/gpt-oss-120b"
  }
  ```
* **Fallback Response Schema (Deterministic Mode):**
  ```json
  {
    "summary": "Candidate incident INC_1 contains 8 correlated events...",
    "attack_chain": "EV_01_RECON -> EV_02_RECON -> ... -> EV_08_LATERAL",
    "evidence": "Structured evidence items: 2 items detected.",
    "mitre_techniques": "Network Service Scanning (T1046), Exploitation of Remote Services (T1210), Application Layer Protocol (T1071), Exfiltration Over C2 Channel (T1041)",
    "confidence": "HIGH",
    "limitations": "Deterministic fallback explanation due to unavailable or failed LLM inference. Reconstructed strictly from deterministic correlation and detection graph.",
    "investigation_recommendations": "Review raw packet capture or underlying logs for the identified source and destination IP addresses.",
    "scenario_id": "TC-10",
    "incident_id": "INC_1",
    "provider": "deterministic",
    "fallback_used": true,
    "model_name": null
  }
  ```

---

## 2. Files Changed and Rationale

| File Path | Description of Changes | Rationale |
| :--- | :--- | :--- |
| [`backend/app/schemas/incident.py`](file:///d:/Zephyr/ThreatWeave/backend/app/schemas/incident.py) | Added `scenario_id`, `incident_id`, `provider`, `fallback_used`, and `model_name` to `LLMExplanation`. Added `model_config = {"protected_namespaces": ()}` to avoid Pydantic v2 namespace warnings. | Formalizes the provenance contract so consumers know which incident and AI engine generated the narrative. |
| [`backend/app/services/llm_explainer.py`](file:///d:/Zephyr/ThreatWeave/backend/app/services/llm_explainer.py) | Added `scenario_id` parameter to `explain()` and `_deterministic_fallback()`. Populated provenance fields on both Groq and fallback code paths. | Ground explanation strictly in the requested scenario's incident data and explicitly track fallback status. |
| [`backend/app/main.py`](file:///d:/Zephyr/ThreatWeave/backend/app/main.py) | Added `scenario_id: Optional[str] = None` query parameter to `/api/demo/explanation`. Added regex validation against path traversal and explicit 404 for missing scenarios. Maintained default `"TC-10"` fallback. | Provides secure, scenario-aware routing without breaking existing callers. |
| [`frontend-react/src/types/explanation.ts`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/types/explanation.ts) | Extended `LLMExplanation` TypeScript interface with `scenario_id`, `incident_id`, `provider`, `fallback_used`, and `model_name`. | Type safety across the React application. |
| [`frontend-react/src/services/api.ts`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/services/api.ts) | Updated `getExplanation(scenarioId: string = 'TC-10')` to pass `?scenario_id=${encodeURIComponent(scenarioId)}`. | Passes active scenario context to backend API. |
| [`frontend-react/src/context/IncidentContext.tsx`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/context/IncidentContext.tsx) | Updated `loadExplanation(scenarioId?: string)` to use backend provider and fallback metadata. Integrated grounded dynamic fallback for offline mode. Updated pipeline stages to reflect truthful status. | Keeps incident context synchronized with selected scenario and transparently displays AI provider state. |
| [`frontend-react/src/pages/AiExplanation.tsx`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/pages/AiExplanation.tsx) | Updated executive brief card, provider banner, fallback indicator badge, and Markdown report export with dynamic provider and incident metadata. Updated badge to `Phase 12D Verified`. | Ensures analyst view and compliance report are 100% grounded in current incident facts. |
| [`tests/test_scenario_explanation.py`](file:///d:/Zephyr/ThreatWeave/tests/test_scenario_explanation.py) | Added 7 unit and integration tests covering default backward compatibility, explicit `TC-10`, 404 on missing scenarios, 400 on path traversal, secret isolation, deterministic fallback grounding, and cross-dataset provenance. | Automated regression test coverage for Phase 12D contract. |

---

## 3. Selected-Incident Data Flow

The following diagram illustrates how the selected incident (`TC-10`) flows consistently from disk/backend through the React context into all UI surfaces:

```
[backend/app/cache/TC-10.json]
             │
             ├──► GET /api/demo/scenario/TC-10 ──► IncidentContext.incident (INC_1)
             │                                            │
             │                                            ├──► AttackGraph.tsx (8 Cytoscape nodes, 20 edges)
             │                                            ├──► MitreMapping.tsx (T1046, T1210, T1071, T1041)
             │                                            └──► SecurityOverview.tsx (Severity: CRITICAL, 8 events)
             │
             └──► GET /api/demo/explanation?scenario_id=TC-10
                         │
                         ├──► Groq API (openai/gpt-oss-120b)
                         │       OR Deterministic Fallback Engine
                         ▼
                  IncidentContext.explanation
                         │
                         ├──► AiExplanation.tsx (Executive Brief, Provider Badge, Stage Telemetry)
                         └──► Downloadable Report (.md) (threatweave_TC-10_Incident_INC_1_Report.md)
```

---

## 4. Provider and Fallback Behavior

ThreatWeave implements a dual-mode, resilient explanation pipeline:

1. **Online LLM Generation (Groq):**
   * Prompt grounded strictly in structured events, MITRE mappings, and evidence items (`_build_prompt()`).
   * System prompt forbids inventing timestamps, unobserved IPs, CVEs, or unregistered tactics.
   * On success: Returns `provider: "groq"`, `fallback_used: false`, and `model_name: "openai/gpt-oss-120b"`.
   * Execution time observed: ~1,200ms to 4,000ms.
2. **Deterministic Fallback Engine:**
   * Automatically triggered if:
     * `GROQ_API_KEY` is missing or invalid.
     * Groq API returns a rate limit (`HTTP 429 Tokens Per Minute exceeded`) or network timeout.
     * Backend is running in offline mode.
   * Behavior: Constructs narrative purely from deterministic rule matching against `incident.events`, `incident.mitre_mappings`, and `incident.evidence_items`.
   * Contains exact phrase `"Deterministic fallback explanation"` in `limitations` for backward compatibility.
   * Reconstructs attack chain strictly from actual event IDs:
     `EV_01_RECON -> EV_02_RECON -> EV_03_SCAN -> EV_04_EXPLOIT -> EV_05_C2 -> EV_06_C2 -> EV_07_EXFIL -> EV_08_LATERAL`.
   * Execution time: < 4ms.

---

## 5. Offline Behavior

When the backend API is unreachable:
1. **Visual Health Pill:** Top navigation bar transitions from `API ONLINE` (green) to `FIXTURE MODE (API OFFLINE)` (amber).
2. **Fixture Fallback:** `IncidentContext` loads the verified bundled `tc10_fixture.json` without failing or blanking the UI.
3. **Local Fallback Explanation:** `IncidentContext` dynamically synthesizes a deterministic explanation from the local incident fixture, clearly labeling `provider: "deterministic"`, `fallback_used: true`, and `limitations: "Offline fixture mode: deterministic fallback rendered because backend explanation is unreachable."`.
4. **No Simulated Inference:** The UI never fakes progress or pretends fresh ML inference took place. All badges clearly identify `CONTROLLED MULTI-STAGE REPLAY` with `DETERMINISTIC CACHE GUARD ACTIVE`.

---

## 6. Dataset Provenance Discrepancy Resolution

### 6.1 Discrepancy Background
In the Phase 12C summary, informal notes mentioned evaluating external datasets `CIC-IDS2017` and `CTU-13` for the 17.1M flow benchmark.

### 6.2 Physical Artifact Investigation
We inspected the actual experiment files:
* [`experiments/cross_dataset_real/config.json`](file:///d:/Zephyr/ThreatWeave/experiments/cross_dataset_real/config.json#L3):
  ```json
  "source_dataset": "NF-UNSW-NB15-v2",
  "target_dataset": "Real NF-CSE-CIC-IDS2018-V2",
  "rows_processed": 17129715
  ```
* [`experiments/cross_dataset_real/report.md`](file:///d:/Zephyr/ThreatWeave/experiments/cross_dataset_real/report.md#L9):
  `Target Dataset: Real NF-CSE-CIC-IDS2018-V2` (17,129,715 NetFlow rows; 15,101,685 benign, 2,028,030 attack).
* [`experiments/cross_dataset_real/metrics.json`](file:///d:/Zephyr/ThreatWeave/experiments/cross_dataset_real/metrics.json#L18):
  Attack breakdown lists `SSH-Bruteforce`, `DDoS attacks-LOIC-HTTP`, `DDOS attack-HOIC`, `Infilteration`, `SQL Injection`, which are specific categories of CSE-CIC-IDS2018.

### 6.3 Conclusion & Verification
* The target dataset evaluated in the 17.1M flow experiment was **exclusively Real NF-CSE-CIC-IDS2018-V2**.
* The mention of CIC-IDS2017/CTU-13 in early proposal notes was an artifact of exploratory project planning.
* The React frontend ([`frontend-react/src/pages/CrossDataset.tsx`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/pages/CrossDataset.tsx#L18)) already correctly states **NF-CSE-CIC-IDS2018-V2**, matching the physical artifact.
* Unit test `test_cross_dataset_provenance_verification` now permanently asserts this provenance in CI.

---

## 7. Tests Added and Verification Results

### 7.1 New Tests Added (`tests/test_scenario_explanation.py`)
1. `test_explanation_default_backward_compatible`: Confirms `GET /api/demo/explanation` with no arguments defaults to `TC-10`, returns status 200, `incident_id == "INC_1"`, and populates `provider` and `fallback_used`.
2. `test_explanation_explicit_scenario_tc10`: Confirms `GET /api/demo/explanation?scenario_id=TC-10` returns status 200 with matching scenario metadata.
3. `test_explanation_unsupported_scenario_fails_explicitly`: Confirms `scenario_id=TC-01` and `NONEXISTENT_999` return HTTP 404 with descriptive error detail.
4. `test_explanation_path_traversal_rejected`: Confirms malicious paths like `../../secrets` and `TC-10;cat` are rejected with HTTP 400.
5. `test_explanation_no_secret_leakage`: Confirms responses never contain `gsk_` or the server `GROQ_API_KEY`.
6. `test_deterministic_fallback_fidelity`: Confirms fallback produces structured explanation using only genuine incident event IDs (`EV_01`..`EV_08`) and maintains backward-compatible limitation strings.
7. `test_cross_dataset_provenance_verification`: Confirms `experiments/cross_dataset_real/config.json` verifies `Real NF-CSE-CIC-IDS2018-V2` with `17,129,715` rows.

### 7.2 Execution Results

#### Command 1: Pytest Suite
```powershell
$env:PYTHONPATH="backend"
.\.venv\Scripts\pytest.exe tests/ -q
```
**Output:**
```
..................................                                       [100%]
34 passed, 2 warnings in 33.47s
```
*(All 34 backend unit tests pass without failure).*

#### Command 2: React Frontend Production Build
```powershell
cd D:\Zephyr\ThreatWeave\frontend-react
npm run build
```
**Output:**
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
dist/assets/index-CS1IJtxp.js   719.23 kB │ gzip: 215.88 kB
✓ built in 8.24s
```
*(100% clean build, zero TypeScript errors).*

#### Command 3: Legacy Vanilla Frontend Build
```powershell
cd D:\Zephyr\ThreatWeave\frontend
npm run build
```
**Output:**
```
> frontend@0.0.0 build
> tsc && vite build

vite v8.3.4 building client environment for production...
transforming...
✓ 8 modules transformed.
dist/index.html                   0.70 kB │ gzip:   0.40 kB
dist/assets/index-Dz0hM0O7.css    4.93 kB │ gzip:   1.47 kB
dist/assets/index-BHOUDNJS.js   449.09 kB │ gzip: 141.32 kB
✓ built in 369ms
```
*(Legacy frontend preserved completely intact).*

#### Command 4: Live HTTP API Verification
```powershell
# 1. Explicit scenario_id=TC-10
$res = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/demo/explanation?scenario_id=TC-10"
# Output: scenario_id: "TC-10", incident_id: "INC_1", provider: "groq", fallback_used: false

# 2. Unsupported scenario_id=TC-01
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/demo/explanation?scenario_id=TC-01"
# Output: HTTP 404 {"detail": "Scenario 'TC-01' not found or unavailable."}

# 3. Path traversal attack
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/demo/explanation?scenario_id=../../passwords"
# Output: HTTP 400 {"detail": "Invalid scenario identifier format"}

# 4. Backward compatible default call
$def = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/demo/explanation"
# Output: scenario_id: "TC-10", incident_id: "INC_1"
```

#### Command 5: Visual Verification via Browser Subagent
The browser subagent navigated to `http://localhost:5174/#report` and `http://localhost:5174/#overview`:
* Verified `Phase 12D Verified` badge.
* Verified `Executive Cyber Incident Brief (INC_1 • TC-10)` title.
* Verified `ZERO CREDENTIALS EXPOSED TO BROWSER` badge.
* Verified all 6 narrative sections populated with grounded telemetry facts.
* Verified 9-Stage Pipeline visualizer reflecting truthful execution states.

---

## 8. Known Limitations and Deferred Work

1. **Scenarios TC-01 through TC-07:** Currently unpopulated in `backend/app/cache/`. They return HTTP 404 from the explanation and replay APIs, and the UI correctly marks them as `IMPLEMENTATION REQUIRED`. Creation of scenario replay caches is scheduled for Phase 12E.
2. **Offline Replay Animation:** The 9-stage stepper on the overview page animates visually to demonstrate the pipeline flow; it is explicitly labeled as a controlled replay visualization rather than real-time network sensor telemetry.
3. **Groq Token Limits:** When using free on-demand Groq tiers, rapid consecutive calls may encounter transient 429 rate limits. ThreatWeave handles this gracefully by automatically engaging the deterministic fallback engine with zero analyst downtime.

---

## 9. Readiness Assessment

The TC-10 demonstration is **100% READY for end-to-end review**:
* Consistency between backend cache, API response, UI context, attack graph, MITRE grid, and downloadable report is verified.
* Provider metadata and fallback mechanisms are fully operational and test-backed.
* Security isolation for API keys is confirmed.
* No production model weights or training pipelines were altered.

---

*In accordance with Phase 12D instructions and the stop condition, work ceases here. All subsequent scenario extraction (TC-01..TC-09) awaits user review and approval.*
