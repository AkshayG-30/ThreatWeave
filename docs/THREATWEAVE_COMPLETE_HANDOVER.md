# ThreatWeave: Complete Project Handover and Continuation Document

**Project:** ThreatWeave  
**Hackathon:** Zéphyr 2026 AI Hackathon  
**Problem Statement:** PS-9 — Mitigating Advanced Digital Threats and Securing Distributed Infrastructure  
**Team:** FANTASTIC 4  
**Team ID:** MS-2026-0187  
**Project Root:** `D:\Zephyr\ThreatWeave`  
**Primary Frontend:** `frontend-react/` (React 18 + TypeScript + Vite)  
**Backend:** `backend/` (FastAPI + Python 3.12)  
**Primary Dataset:** NF-UNSW-NB15-v2  
**Production Supervised Detector:** XGBoost (`models/xgboost_detector.json`)  
**Production Anomaly Detector:** Isolation Forest (`models/isolation_forest.joblib`)  
**Document Generated / Updated:** October 13, 2026  
**Document Status:** **FINAL & COMPREHENSIVE HANDOVER**  

---

## Table of Contents

1. [Section A: Project Overview](#section-a-project-overview)
2. [Section B: Complete Architecture & Data Flow](#section-b-complete-architecture--data-flow)
3. [Section C: Model Inventory & Scientific Provenance](#section-c-model-inventory--scientific-provenance)
4. [Section D: Critical Execution Reality — Cached Scenarios vs. Live Inference](#section-d-critical-execution-reality--cached-scenarios-vs-live-inference)
5. [Section E: Demonstration Scenario Catalogue (TC-01 through TC-10)](#section-e-demonstration-scenario-catalogue-tc-01-through-tc-10)
6. [Section F: Dataset & Empirical Evaluation Results](#section-f-dataset--empirical-evaluation-results)
7. [Section G: Attack Graph Assembly & MITRE ATT&CK Attribution](#section-g-attack-graph-assembly--mitre-attck-attribution)
8. [Section H: Backend, Frontend & Security Engineering](#section-h-backend-frontend--security-engineering)
9. [Section I: Validation History & Current System Status](#section-i-validation-history--current-system-status)
10. [Section J: Hackathon Presentation & Live-Demo Strategy](#section-j-hackathon-presentation--live-demo-strategy)
11. [Section K: Workstream Allocations & Team Responsibilities](#section-k-workstream-allocations--team-responsibilities)
12. [Section L: Engineering Decision History & Rationale](#section-l-engineering-decision-history--rationale)
13. [Section M: Final Freeze Rules & Immediate Checklist](#section-m-final-freeze-rules--immediate-checklist)
14. [Section N: Local Evidence & Artifact Index](#section-n-local-evidence--artifact-index)

---

## Section A: Project Overview

### 1. Problem Statement & Motivation
Modern Security Operations Centers (SOCs) face an overwhelming volume of disconnected network telemetry. Contemporary intrusion detection systems (IDS) suffer from fundamental architectural bottlenecks:
1. **Supervised Point Blindness:** Supervised machine learning models (XGBoost, Random Forest) achieve near-perfect classification on known attack signatures but exhibit catastrophic recall degradation when encountering zero-day variations or novel attack families.
2. **Unsupervised False Positive Floods:** Standalone unsupervised anomaly detectors (Isolation Forest, Autoencoders) trigger excessive false alarms on benign enterprise variance (often exceeding 5–10% False Positive Rate), causing analyst alert fatigue.
3. **Lack of Causal Reconstruction:** Typical tools report isolated flows without topological or temporal context, leaving analysts to manually stitch multi-stage campaigns together.
4. **LLM Hallucination Risk:** Off-the-shelf generative AI security assistants frequently hallucinate attack steps, IP addresses, and CVEs that are not grounded in actual network evidence.

### 2. What ThreatWeave Does
ThreatWeave is a multi-tier cyber-threat triage platform that bridges the gap between high-speed point detection and automated multi-stage incident explanation:
- **Dual-Engine Detection:** Evaluates incoming NetFlow v2 telemetry simultaneously through a high-precision supervised classifier (XGBoost) and a behavioral outlier detector (Isolation Forest).
- **Consensus & Divergence Fusion:** Identifies whether detections represent known signatures, behavioral anomalies, or detector agreement.
- **Bounded Graph Reconstruction:** Applies deterministic entity-sharing and sliding-window temporal heuristics ($\Delta t \le 30\text{s}$) to assemble causally connected attack graphs while pruning uncorrelated noise.
- **MITRE ATT&CK Attribution:** Maps correlated clusters directly to standardized MITRE tactics and techniques using deterministic rules.
- **Evidence-Grounded AI Explanation:** Synthesizes structured, human-readable SOC briefing narratives via a temperature-constrained LLM (Groq / Llama 3) restricted strictly to verified graph facts, backed by a deterministic rule-based fallback.

### 3. Target Users & Intended Workflow
- **Target Users:** Tier 1 and Tier 2 SOC analysts, threat hunters, and incident responders.
- **Operational Workflow:**
  1. *Stream Ingestion:* Network flows are captured and normalized to standard NetFlow v2 schema.
  2. *Hybrid Classification:* Point detection flags attack probabilities and outlier scores.
  3. *Triage Bounding:* Correlated flows are clustered into candidate incidents; benign noise is isolated.
  4. *Topological Investigation:* The analyst inspects the interactive Cytoscape attack graph.
  5. *Attribution & Reporting:* The system maps MITRE techniques and compiles an exportable Markdown compliance briefing.

### 4. Key Capabilities, Limitations, and Current Maturity
- **Key Capabilities:**
  - Near-zero false alarms on benign baselines ($<0.4\%$ FPR).
  - High-confidence known attack detection ($99.88\%$ recall on test split).
  - Verified zero-shot holdout generalization ($68.64\%$ recall on Fuzzers, $100\%$ on Reconnaissance).
  - Deterministic sub-10ms scenario replay for SOC demonstrations.
  - Complete air-gapped deterministic fallback if external LLM APIs fail.
- **Known Limitations:**
  - Tabular NetFlow records do not contain true multi-hop enterprise kill-chains; multi-stage evaluation relies on a controlled 8-event benchmark fixture (TC-10).
  - Severe domain shift when tested cross-dataset on external enterprise telemetry (NF-ToN-IoT accuracy drops to $52.05\%$).
  - GNN and GRU architectures were abandoned due to small graph topology and missing chronological ground truth.
- **Current Maturity:** **Phase 12F Demonstration-Ready Prototype**. Core detection pipelines, scenario caches, REST APIs, and React SOC interfaces are fully implemented, verified, and frozen.

### 5. Concise Technical Summary for Continuity
> **ThreatWeave** is a hybrid cyber-triage platform for NetFlow v2 data that pairs supervised XGBoost ($99.88\%$ recall) and unsupervised Isolation Forest ($55.08\%$ recall) with NetworkX graph reconstruction and evidence-grounded LLM narrative generation. The operational demo serves 10 verified scenarios (TC-01 through TC-10) with sub-10ms deterministic response times from audited offline caches, backed by an on-demand Groq explainer and interactive Cytoscape visualization.

---

## Section B: Complete Architecture & Data Flow

ThreatWeave processes telemetry through a nine-stage conceptual and operational pipeline:

```
[Raw Network Flows] 
        │
        ▼  Stage 1: NetFlow v2 Ingestion
[Standardized Records (41 Features)]
        │
        ▼  Stage 2: Preprocessing & Normalization
[Feature Vectors & Scaled Tensors]
   ┌────┴──────────────────────────┐
   ▼                               ▼
Stage 3: Supervised XGBoost   Stage 4: Isolation Forest
(Known Signatures: p >= 0.51)   (Behavioral Outliers: s > 0.0094)
   └────┬──────────────────────────┘
        ▼  Stage 5: Bounded Correlation Engine
[Correlated Evidence Clusters (Entity & Temporal Window Δt <= 30s)]
        │
        ▼  Stage 6: NetworkX Graph Assembly
[Directed Attack Graph Topology (Nodes = Events, Edges = Evidence)]
        │
        ▼  Stage 7: MITRE ATT&CK Attribution
[Deterministic Technique Mappings (T1046, T1210, T1071, T1499, etc.)]
        │
        ▼  Stage 8: Evidence-Grounded AI Explanation
[Groq LLM / Deterministic Rule Fallback Narrative]
        │
        ▼  Stage 9: Analyst Command Center
[Interactive Cytoscape Visualizer, HUD & Downloadable Markdown Report]
```

### Stage-by-Stage Implementation Matrix

| Stage | Implementation Status | Physical Files & Functions | Data Artifacts | Operational Reality |
| :--- | :--- | :--- | :--- | :--- |
| **1. Data Ingestion** | **IMPLEMENTED** | `scripts/download_dataset.py`<br>`backend/app/services/pipeline.py:DataPipeline.load_data` | `data/processed/nf_unsw_nb15_v2_sample_150k.csv` | Reads 41-feature NetFlow v2 CSV records into memory. |
| **2. Preprocessing** | **IMPLEMENTED** | `backend/app/services/pipeline.py:DataPipeline.normalize` | `models/feature_columns.json` | StandardScaler feature scaling, categorical encoding, NaN elimination. |
| **3. Supervised Detection** | **IMPLEMENTED & FROZEN** | `scripts/train_supervised.py`<br>`models/xgboost_detector.json` | `experiments/detection_benchmark/comparison.json` | XGBoost binary classifier ($p \ge 0.51$). Evaluated offline and cached for demo. |
| **4. Anomaly Detection** | **IMPLEMENTED & FROZEN** | `scripts/train_anomaly.py`<br>`models/isolation_forest.joblib` | `experiments/anomaly_benchmark/comparison.json` | Scikit-learn Isolation Forest ($s > 0.0094$). Fitted on benign flows. |
| **5. Bounded Correlation** | **IMPLEMENTED** | `backend/app/services/correlation.py:CorrelationEngine.correlate_events` | `backend/app/schemas/incident.py` | Pairs events by shared IP and sliding time window ($\Delta t \le 30\text{s}$). |
| **6. Graph Assembly** | **IMPLEMENTED** | `backend/app/services/correlation.py`<br>`frontend-react/src/pages/AttackGraph.tsx` | `experiments/phase4/synthetic_incident.json` | NetworkX directed graph builder in Python; Cytoscape.js rendering in React. |
| **7. MITRE Mapping** | **IMPLEMENTED** | `backend/app/services/mitre_mapper.py:MitreMapper.map_event` | `backend/app/schemas/incident.py:MitreMapping` | Deterministic signature and destination-port heuristic lookups. |
| **8. AI Explanation** | **IMPLEMENTED** | `backend/app/services/llm_explainer.py:LLMExplainer.explain` | `backend/app/schemas/incident.py:LLMExplanation` | Groq API (`openai/gpt-oss-120b` or `llama-3.3-70b-versatile`) with deterministic rule fallback. |
| **9. Analyst Reporting** | **IMPLEMENTED** | `frontend-react/src/pages/AiExplanation.tsx:handleDownload` | Markdown client export (`ThreatWeave_{ID}_Report.md`) | Client-side dynamic markdown compilation and browser download. |

---

## Section C: Model Inventory & Scientific Provenance

All model artifacts in ThreatWeave are strictly versioned, frozen, and immutable:

```
models/
├── feature_columns.json           (822 bytes, 41 standardized feature names)
├── isolation_forest.joblib        (2,089,821 bytes, production anomaly detector)
├── random_forest_baseline.joblib  (6,375,113 bytes, baseline comparative model)
└── xgboost_detector.json          (321,463 bytes, production supervised detector)
```

### Detailed Model Inventory

#### 1. Production Supervised Detector — XGBoost
- **Algorithm:** Gradient Boosted Decision Trees (XGBoost 2.1+)
- **Physical Artifact:** `models/xgboost_detector.json` (321,463 bytes)
- **Saved Weights Exist:** **YES**
- **Operational Scenario Usage:** **YES** (Source of pre-computed scores in TC-01, TC-02, TC-03, TC-06, TC-07)
- **Training Provenance:** Fitted on 85% training split (127,500 flows) of `NF-UNSW-NB15-v2`.
- **Verified Benchmark Metrics:**
  - *Accuracy:* $99.631\%$
  - *Precision:* $91.598\%$
  - *Recall:* $99.888\%$ ($894 / 895$ test attack flows)
  - *F1-Score:* $95.564\%$
  - *False Positive Rate (FPR):* $0.380\%$ ($82 / 21,605$ benign flows)
  - *Training Latency:* $1.95\text{s}$
- **Source Artifact:** `experiments/detection_benchmark/comparison.json`

#### 2. Production Anomaly Detector — Isolation Forest
- **Algorithm:** Unsupervised Tree Isolation (scikit-learn `IsolationForest`)
- **Physical Artifact:** `models/isolation_forest.joblib` (2,089,821 bytes)
- **Saved Weights Exist:** **YES**
- **Operational Scenario Usage:** **YES** (Source of pre-computed outlier scores in TC-01, TC-04, TC-06, TC-07)
- **Training Provenance:** Fitted exclusively on benign training samples ($119,793$ benign flows) using 41 normalized features. Outlier threshold set at $0.0094$.
- **Verified Benchmark Metrics:**
  - *Precision:* $24.96\%$
  - *Recall:* $55.08\%$
  - *F1-Score:* $34.36\%$
  - *False Positive Rate (FPR):* $6.86\%$
- **Source Artifact:** `experiments/anomaly_benchmark/comparison.json`

#### 3. Supervised Baseline — Random Forest
- **Algorithm:** Random Forest Classifier (scikit-learn, 100 estimators)
- **Physical Artifact:** `models/random_forest_baseline.joblib` (6,375,113 bytes)
- **Saved Weights Exist:** **YES**
- **Operational Scenario Usage:** **NO** (Retained strictly as comparative benchmark baseline)
- **Verified Benchmark Metrics:**
  - *Accuracy:* $99.676\%$
  - *Precision:* $94.967\%$
  - *Recall:* $96.983\%$ ($868 / 895$ test attack flows)
  - *F1-Score:* $95.965\%$
  - *False Positive Rate (FPR):* $0.213\%$
  - *Training Latency:* $2.89\text{s}$
- **Source Artifact:** `experiments/detection_benchmark/comparison.json`

#### 4. Supervised Baseline — LightGBM
- **Algorithm:** LightGBM Booster
- **Physical Artifact:** `experiments/detection_benchmark/lightgbm_model.txt` (341,743 bytes)
- **Saved Weights Exist:** **YES**
- **Operational Scenario Usage:** **NO** (Benchmark comparison only)
- **Verified Benchmark Metrics:**
  - *Accuracy:* $99.622\%$
  - *Precision:* $91.667\%$
  - *Recall:* $99.553\%$ ($891 / 895$ test attack flows)
  - *F1-Score:* $95.447\%$
  - *False Positive Rate (FPR):* $0.375\%$
  - *Training Latency:* $1.18\text{s}$
- **Source Artifact:** `experiments/detection_benchmark/comparison.json`

#### 5. Experimental Anomaly Benchmark — Neural Autoencoder
- **Algorithm:** Deep MLP Autoencoder ($41 \to 32 \to 16 \to 8 \to 16 \to 32 \to 41$) with MSE reconstruction loss
- **Physical Artifact:** Script only (`scripts/run_autoencoder_anomaly.py`)
- **Saved Weights Exist:** **NO** (Model was evaluated in-memory during script execution; weights not serialized)
- **Operational Scenario Usage:** **NO (DISABLED as TC-05)**
- **Verified Benchmark Metrics:**
  - *Precision:* $39.01\%$
  - *Recall:* $53.74\%$
  - *F1-Score:* $45.21\%$
  - *False Positive Rate (FPR):* $3.48\%$
- **Source Artifact:** `experiments/anomaly_benchmark/comparison.json` and `report.md`

#### 6. Zero-Shot Generalization Model — Held-Out Fuzzers
- **Algorithm:** XGBoost trained with 100% of Fuzzers attack flows withheld
- **Physical Artifact:** `experiments/unseen_attack/models/xgb_holdout_Fuzzers.json` (303,334 bytes)
- **Saved Weights Exist:** **YES**
- **Operational Scenario Usage:** **YES** (Source of TC-08 recorded evaluation)
- **Verified Benchmark Metrics:**
  - *Zero-Shot Recall:* $68.64\%$ ($961 / 1,400$ unseen Fuzzers flows detected)
  - *Precision:* $93.12\%$
  - *F1-Score:* $79.03\%$
  - *FPR:* $0.246\%$
- **Source Artifact:** `experiments/unseen_attack/results.json`

#### 7. Zero-Shot Generalization Model — Held-Out Reconnaissance
- **Algorithm:** XGBoost trained with 100% of Reconnaissance flows withheld
- **Physical Artifact:** `experiments/unseen_attack/models/xgb_holdout_Reconnaissance.json` (314,604 bytes)
- **Saved Weights Exist:** **YES**
- **Operational Scenario Usage:** **YES** (Source of TC-09 recorded evaluation)
- **Verified Benchmark Metrics:**
  - *Zero-Shot Recall:* $100.0\%$ ($802 / 802$ unseen Reconnaissance flows detected)
  - *Precision:* $87.46\%$
  - *F1-Score:* $93.31\%$
  - *FPR:* $0.399\%$
- **Source Artifact:** `experiments/unseen_attack/results.json`

---

## Section D: Critical Execution Reality — Cached Scenarios vs. Live Inference

### 1. The Core Scientific Finding
> **CLICKING "EXECUTE SCENARIO" DOES NOT INVOKE XGBOOST OR ISOLATION FOREST ON THE BACKEND AT THAT MOMENT.**  
> The backend does not load `models/xgboost_detector.json` or `models/isolation_forest.joblib` into memory when a scenario button is clicked. The API returns pre-computed, verified incident payloads stored in `backend/app/cache/TC-XX.json`.

### 2. Why Scores Are Genuine (Not Fabricated)
While delivered via pre-computed caches, **the flow scores in TC-01, TC-02, TC-03, TC-04, TC-06, and TC-07 are NOT fabricated or hardcoded by hand**.
- They were generated by executing `scripts/generate_verified_scenarios.py` offline against the frozen production models on genuine test flows sampled from the untouched 15% evaluation split of `NF-UNSW-NB15-v2`.
- Caching was implemented to eliminate disk I/O, tabular serialization, and runtime model evaluation latency, guaranteeing deterministic sub-10ms response times during live hackathon judging.

### 3. Verified End-to-End Call Chain
```
[User Clicks "Execute Scenario" in UI]
  │
  ▼
frontend-react/src/pages/ScenarioLab.tsx::handleExecute(scenarioId)
  │
  ▼
frontend-react/src/context/IncidentContext.tsx::executeScenarioReplay(scenarioId)
  ├─ Sequentially advances UI stage stepper (Stages 1–9) using 200ms setTimeout intervals
  └─ Calls loadScenarioData(scenarioId)
        │
        ▼
frontend-react/src/services/api.ts::ApiService.getScenarioIncident(scenarioId)
  │ (HTTP GET http://127.0.0.1:8000/api/demo/scenario/TC-XX)
  ▼
backend/app/main.py::get_scenario(scenario_id: str)
  │
  ▼
backend/app/services/demo_scenario_service.py::DemoScenarioService.get_scenario_incident(scenario_id)
  │
  ▼ Reads and deserializes: backend/app/cache/{scenario_id}.json
  ▼ Returns Pydantic StructuredIncident model (HTTP 200 JSON)
```

### 4. UI Animation vs. Backend Reality
The 9-stage pipeline animation displayed in the React Command Center is driven by client-side JavaScript timers (`setTimeout(..., 200)`). It visually illustrates the conceptual progression (Ingestion $\to$ Preprocessing $\to$ Supervised $\to$ Anomaly $\to$ Correlation $\to$ Graph $\to$ MITRE $\to$ AI $\to$ Report), but **the backend does not execute these nine stages independently on button click**.

### 5. Status of the Ad-Hoc `POST /api/detect` Endpoint
- **Current Status:** **NOT IMPLEMENTED**.
- **Investigation Finding:** While referenced in earlier design notes and formally specified by the contract schema `IntegratedDetectorOutput` in [`backend/app/schemas/detector.py`](file:///d:/Zephyr/ThreatWeave/backend/app/schemas/detector.py) and placeholder classes in [`backend/app/services/ml_models.py`](file:///d:/Zephyr/ThreatWeave/backend/app/services/ml_models.py), no `POST /api/detect` route exists in [`backend/app/main.py`](file:///d:/Zephyr/ThreatWeave/backend/app/main.py).
- **Active Backend Routes:** The live FastAPI application exposes exclusively:
  - `GET /health`
  - `GET /api/demo/incident`
  - `GET /api/demo/explanation`
  - `GET /api/demo/scenarios`
  - `GET /api/demo/scenario/{scenario_id}`

---

## Section E: Demonstration Scenario Catalogue (TC-01 through TC-10)

| Scenario ID & Name | Purpose | Execution Mode | Input Data Source | Click-Time Inference? | Score Provenance | Graph & MITRE Provenance | Actual Limitations | Primary Source Files |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **TC-01**<br>Benign Traffic Baseline | Validate detector specificity and zero false alarms | `LIVE_INFERENCE` *(UI label)* | 5 Benign flows from untouched test split (`NF-UNSW-NB15-v2`) | **No** (Served from cache) | **Genuine offline model inference** ($p \le 0.0001$, anomaly $-0.1255$ to $-0.0282$) | Predefined empty lists (`edges: []`, `mitre: []`) | Shows only 5 flows; does not process a continuous packet stream. | `backend/app/cache/TC-01.json`<br>`scripts/generate_verified_scenarios.py` |
| **TC-02**<br>Known Attack — Exploits | Demonstrate high-confidence supervised exploit recall | `LIVE_INFERENCE` *(UI label)* | 5 Exploit flows from untouched test split (`NF-UNSW-NB15-v2`) | **No** (Served from cache) | **Genuine offline model inference** ($p \in [0.9984, 0.9995]$) | Computed temporal adjacency edges; MITRE T1210 mapped | Point flows; lacks multi-hop network progression. | `backend/app/cache/TC-02.json`<br>`scripts/generate_verified_scenarios.py` |
| **TC-03**<br>Known Attack — Generic / DoS | Volumetric and protocol denial-of-service recall | `LIVE_INFERENCE` *(UI label)* | 6 DoS & Generic attack flows from test split | **No** (Served from cache) | **Genuine offline model inference** ($p \in [0.9959, 0.9999]$) | Target-cluster edges computed; MITRE T1498/T1499 mapped | Single target victim IP; synthetic flow grouping. | `backend/app/cache/TC-03.json`<br>`scripts/generate_verified_scenarios.py` |
| **TC-04**<br>Isolation Forest Anomaly Example | Unsupervised behavioral outlier detection | `LIVE_INFERENCE` *(UI label)* | 5 Outlier flows from test split where supervised $p=0.0$ | **No** (Served from cache) | **Genuine offline model inference** ($s > 0.0818 > 0.0094$ threshold) | Predefined empty edges; MITRE T1071 mapped | Relies on statistical divergence; cannot pinpoint root cause. | `backend/app/cache/TC-04.json`<br>`scripts/generate_verified_scenarios.py` |
| **TC-05**<br>Autoencoder Anomaly Example | Deep neural reconstruction benchmark | `DISABLED` *(Non-executable)* | N/A | **No** (Blocked with HTTP 404) | **N/A** (Offline benchmark in `experiments/anomaly_benchmark/`) | N/A | **Disabled by design**: No serialized neural weights exist on disk. | `backend/app/main.py:get_demo_explanation`<br>`experiments/anomaly_benchmark/comparison.json` |
| **TC-06**<br>Detector Agreement | Consensus scenario where both engines trigger | `LIVE_INFERENCE` *(UI label)* | 6 Dual-positive flows from test split ($533$ consensus flows) | **No** (Served from cache) | **Genuine offline model inference** ($p \ge 0.51$, $s > 0.0094$, `source: BOTH`) | Temporal correlation edges; MITRE T1210 mapped | Point flows extracted from independent test records. | `backend/app/cache/TC-06.json`<br>`scripts/generate_verified_scenarios.py` |
| **TC-07**<br>Detector Disagreement | Model divergence and defense-in-depth complementarity | `LIVE_INFERENCE` *(UI label)* | 3 XGB-only ($p>0.99$) + 3 IF-only ($s>0.039, p=0.0$) flows | **No** (Served from cache) | **Genuine offline model inference** showing detector divergence | Predefined empty edges and techniques | Discrepancy requires human analyst triage. | `backend/app/cache/TC-07.json`<br>`scripts/generate_verified_scenarios.py` |
| **TC-08**<br>Held-Out Fuzzers Evaluation | Zero-shot generalization on completely withheld family | `RECORDED_EVALUATION` | 5 Fuzzers flows from test split + aggregate holdout metrics | **No** (Served from cache) | **Genuine offline model inference** on `xgb_holdout_Fuzzers.json` ($68.64\%$ recall) | Predefined empty edges; MITRE T1046 mapped | Fuzzers recall is $68.64\%$; misses $31.36\%$ of novel variants. | `backend/app/cache/TC-08.json`<br>`experiments/unseen_attack/models/xgb_holdout_Fuzzers.json` |
| **TC-09**<br>Held-Out Reconnaissance | Zero-shot generalization on withheld scan family | `RECORDED_EVALUATION` | 5 Recon flows from test split + aggregate holdout metrics | **No** (Served from cache) | **Genuine offline model inference** on `xgb_holdout_Reconnaissance.json` ($100\%$ recall) | Predefined empty edges; MITRE T1046 mapped | Evaluates network probes; benign port scans could cause FPs. | `backend/app/cache/TC-09.json`<br>`experiments/unseen_attack/models/xgb_holdout_Reconnaissance.json` |
| **TC-10**<br>Controlled Multi-Stage APT Replay | End-to-end incident reconstruction, graph & LLM | `CONTROLLED_REPLAY` | Synthetic multi-stage APT benchmark fixture (Phase 4) | **No** (Served from cache) | **ILLUSTRATIVE FIXTURE VALUES** ($0.10$ to $0.99$; not sampled from UNSW CSV) | **Pre-constructed fixture** ($20$ edges, $8$ attack events, $1$ isolated noise, $4$ MITRE tactics) | Controlled fixture; NetFlow lacks true multi-stage kill-chains. | `backend/app/cache/TC-10.json`<br>`experiments/phase4/synthetic_incident.json` |

---

## Section F: Dataset & Empirical Evaluation Results

### 1. Primary Dataset & Sample Construction
- **Dataset:** `NF-UNSW-NB15-v2` (NetFlow format based on UNSW-NB15).
- **Physical Sample:** `data/processed/nf_unsw_nb15_v2_sample_150k.csv` ($150,000$ records, $41$ standardized features).
- **Class Balance:**
  - Benign: $144,034$ flows ($96.02\%$)
  - Attack: $5,966$ flows ($3.98\%$)
- **Data Split:** $85\%$ Training ($127,500$ flows) / $15\%$ Untouched Evaluation Split ($22,500$ flows). Stratified, `random_state=42`.

### 2. In-Distribution Supervised Detection Benchmark
*Source: `experiments/detection_benchmark/comparison.json`*

| Metric | Random Forest Baseline | XGBoost Production | LightGBM Benchmark |
| :--- | :---: | :---: | :---: |
| **Accuracy** | $99.676\%$ | $99.631\%$ | $99.622\%$ |
| **Precision** | $94.967\%$ | $91.598\%$ | $91.667\%$ |
| **Recall (Attack)** | $96.983\%$ ($868/895$) | **$99.888\%$** ($894/895$) | $99.553\%$ ($891/895$) |
| **F1-Score** | $95.965\%$ | $95.564\%$ | $95.447\%$ |
| **Macro-F1** | $97.898\%$ | $97.686\%$ | $97.625\%$ |
| **False Positive Rate (FPR)** | **$0.213\%$** ($46/21,605$) | $0.380\%$ ($82/21,605$) | $0.375\%$ ($81/21,605$) |
| **Specificity (Benign Recall)** | $99.787\%$ | $99.620\%$ | $99.625\%$ |
| **Training Latency** | $2.89\text{s}$ | $1.95\text{s}$ | **$1.18\text{s}$** |

### 3. Anomaly Detection Benchmark (Fitted on Benign Only)
*Source: `experiments/anomaly_benchmark/comparison.json`*

| Metric | Isolation Forest (Production) | Neural Autoencoder (Experimental) |
| :--- | :---: | :---: |
| **Precision** | $24.96\%$ | $39.01\%$ |
| **Recall** | **$55.08\%$** | $53.74\%$ |
| **F1-Score** | $34.36\%$ | $45.21\%$ |
| **False Positive Rate (FPR)** | $6.86\%$ | $3.48\%$ |

### 4. Zero-Shot Holdout Family Generalization
*Source: `experiments/unseen_attack/results.json`*

| Holdout Family | Training Set (Zero Family Samples) | Test Support | True Positives | False Positives | Zero-Shot Recall | Precision | F1-Score | FPR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Fuzzers** | $119,793$ | $1,400$ | $961$ | $71$ | **$68.64\%$** | $93.12\%$ | $79.03\%$ | $0.246\%$ |
| **Reconnaissance** | $120,391$ | $802$ | $802$ | $115$ | **$100.0\%$** | $87.46\%$ | $93.31\%$ | $0.399\%$ |

### 5. Cross-Dataset Generalization Stress Test (Domain Shift)
*Source: `experiments/cross_dataset_real/metrics.json`*
- **Target Dataset:** NF-ToN-IoT ($17,129,715$ real enterprise/IoT flows).
- **Model Evaluated:** Production XGBoost trained on NF-UNSW-NB15-v2.
- **Results:**
  - *Accuracy:* $52.05\%$
  - *Precision:* $1.30\%$
  - *Recall:* $4.06\%$ ($82,262 / 2,028,030$ attack flows detected)
  - *F1-Score:* $1.96\%$
  - *False Positive Rate (FPR):* **$41.50\%$** ($6,267,796$ false alarms)
- **Scientific Conclusion:** Flawless in-distribution performance does not transfer across disparate network topologies. Flow-level point detectors experience catastrophic domain shift, proving the necessity of bounded graph correlation.

### 6. Abandoned and Deferred Approaches
*Source: `experiments/gnn_graph/report.md`, `experiments/gru_temporal/report.md`, `experiments/campaign_dataset_audit/`*
- **Graph Neural Networks (GNN):** Deferred. Training a parameterized GNN on an 8-node incident topology causes severe overfitting. Deterministic NetworkX rules provide $100\%$ precision on the candidate incident without deep learning overhead.
- **Recurrent Temporal Models (GRU):** Deferred. Tabular NetFlow lacks verified microsecond chronological ordering across disparate hosts. Training a sequential RNN on unordered tabular rows violates scientific integrity.
- **UNRAVELED & SAGA Datasets:** Audited and rejected for the hackathon MVP due to incompatible feature schemas requiring unverified adapter pipelines.

---

## Section G: Attack Graph Assembly & MITRE ATT&CK Attribution

### 1. Graph Topology: Nodes and Edges
- **Nodes ($V$):** Represent individual candidate security events flagged by point detectors.
  - Node attributes: `event_id`, `timestamp`, `source_ip`, `destination_ip`, `destination_port`, `protocol`, `detection_source`, `confidence`.
- **Edges ($E$):** Directed relationships established by the Bounded Correlation Engine.
  - Edge types:
    - `TEMPORAL_PROXIMITY`: Events occurring within $\Delta t \le 30\text{s}$.
    - `SHARED_SRC_IP`: Same attacking host pivoting to new destinations.
    - `SHARED_DST_IP`: Multiple events converging on a common victim asset.
    - `DETECTION_AGREEMENT`: Co-occurring events confirmed by both detection mechanisms.

### 2. Computed vs. Predefined Graphs
- **Computed Scenarios (TC-02, TC-03, TC-06):** Edge lists were computed during scenario generation (`scripts/generate_verified_scenarios.py`) by applying pairwise temporal and IP-matching heuristics across the selected test flows.
- **Controlled Replay Fixture (TC-10):** A 9-node, 20-edge topology originating from Phase 4 benchmark research (`experiments/phase4/synthetic_incident.json`).
  - Contains $8$ correlated attack events spanning Reconnaissance $\to$ Scanning $\to$ Exploitation $\to$ C2 $\to$ Lateral Movement $\to$ Exfiltration.
  - Contains $1$ isolated noise event (`EV_NOISE_99` from benign host `172.16.0.99`). The correlation engine isolates this node with zero edges, proving false-positive pruning.

### 3. Deterministic MITRE ATT&CK Mapping
ThreatWeave bypasses probabilistic LLM classification for threat intelligence attribution, using deterministic rule mapping in `backend/app/services/mitre_mapper.py`:

| Technique ID | Technique Name | Attribution Rule | Associated Fixture Event |
| :--- | :--- | :--- | :--- |
| **T1046** | Network Service Scanning | Port scan pattern or destination port 80/443 sweep | `EV_01_RECON`, `EV_02_RECON`, `EV_03_SCAN` |
| **T1210** | Exploitation of Remote Services | SMB (port 445) exploit signature with $p > 0.90$ | `EV_04_EXPLOIT` |
| **T1071** | Application Layer Protocol | Outbound anomalous beaconing on port 8080/443 | `EV_05_C2`, `EV_06_C2` |
| **T1041** | Exfiltration Over C2 Channel | High byte-ratio outbound egress ($s > 0.90$) | `EV_07_EXFIL` |
| **T1021** | Remote Services | Internal lateral movement on port 22/3389 | `EV_08_LATERAL` |

### 4. Graph Visualization vs. Proof of Attack
*Scientific Boundary:* The Cytoscape attack graph visualizes **statistical correlation and shared entity attribution**. It does not constitute mathematical proof of attacker intent or causality. Network telemetry captures packet headers, not endpoint process executions.

---

## Section H: Backend, Frontend & Security Engineering

### 1. Backend Architecture (FastAPI)
- **Entrypoint:** `backend/app/main.py`
- **Application Structure:**
  - `backend/app/schemas/`: Pydantic data contracts (`StructuredIncident`, `LLMExplanation`, `CanonicalEvent`, `IntegratedDetectorOutput`).
  - `backend/app/services/demo_scenario_service.py`: Whitelisted scenario cache loader.
  - `backend/app/services/llm_explainer.py`: Grounded Groq prompt engine and deterministic rule fallback.
  - `backend/app/services/correlation.py`: NetworkX temporal/entity correlation engine.
  - `backend/app/services/mitre_mapper.py`: Deterministic MITRE ATT&CK attribution engine.

### 2. Frontend Architecture (React + TypeScript + Vite)
- **Directory:** `frontend-react/`
- **Design System:** Enterprise SOC Dark Palette (Slate `#0b0f19`, Cyan `#06b6d4`, Purple `#8b5cf6`, Emerald `#10b981`, Amber `#f59e0b`, Red `#ef4444`).
- **State Management:** `frontend-react/src/context/IncidentContext.tsx`
  - Maintains `selectedScenarioId`, `incident`, `explanation`, `explanationSource`, `stages`, and `isReplaying`.
  - Guarantees zero stale-data leakage across scenario switches.
- **Nine Primary Pages:**
  1. `SecurityOverview.tsx`: Master telemetry status, 9-stage stepper, and quick action bar.
  2. `AttackGraph.tsx`: Interactive Cytoscape.js canvas with node inspection HUD.
  3. `MitreMatrix.tsx`: ATT&CK technique matrix linked dynamically to active incident.
  4. `AiExplanation.tsx`: Evidence-grounded narrative briefing with on-demand Groq trigger.
  5. `ScenarioLab.tsx`: Interactive catalogue of TC-01 through TC-10 with replay triggers.
  6. `ModelEvaluation.tsx`: Frozen confusion matrices, ROC-AUC curves, and benchmark tables.
  7. `LiveMonitor.tsx`: Stream inspection view.
  8. `Methodology.tsx`: Architectural documentation and ablation metrics.
  9. `SystemHealth.tsx`: Diagnostic latency meters and service health.

### 3. On-Demand Groq LLM Triggering
To prevent automatic quota depletion and unintended external API calls:
- **No Groq Calls on Startup:** On initial load, the app initializes the deterministic offline narrative without contacting Groq.
- **No Groq Calls on Browsing:** Selecting scenarios in the UI does not trigger external requests.
- **Explicit Button Invocations Only:**
  - Clicking **"Execute Scenario"** in Scenario Lab triggers Groq for that scenario during replay.
  - Clicking **"Generate AI Explanation (Groq)"** on the AI Explanation page invokes Groq on demand.
- **Deterministic Rule Fallback:** If `GROQ_API_KEY` is missing, unconfigured, or rate-limited, `LLMExplainer._deterministic_fallback` immediately constructs an air-gapped narrative from structured graph facts.

### 4. Security & Secret Handling
- **Path Traversal Protection:** Scenario IDs are strictly validated using regex: `^[A-Za-z0-9_-]+$`. Attempts to supply `../../` return HTTP 400.
- **Secret Isolation:** `GROQ_API_KEY` is maintained exclusively on the backend in `.env`. It is never returned in API responses or serialized to client bundles.

---

## Section I: Validation History & Current System Status

### 1. Independent Verification Executed for this Handover (October 13, 2026)

#### A. Full Backend Pytest Suite
- **Command:** `$env:PYTHONPATH="backend"; .venv\Scripts\python -m pytest`
- **Output:** `44 passed, 2 warnings in 18.68s` ($100\%$ pass rate)
- **Coverage:** Schema validation (2), Health check (1), Point detection (5), Phase 4 graph (5), Pipeline (6), Correlation engine (8), Scenario explanations (7), Phase 12E scenarios (10).

#### B. React Frontend Production Build
- **Command:** `npm run build` inside `frontend-react/`
- **Output:** `✓ 1606 modules transformed. dist/assets/index-DtU-q1Nn.js (719.86 kB). Built in 27.24s with 0 errors.`

#### C. Legacy Vanilla Frontend Build
- **Command:** `npm run build` inside `frontend/`
- **Output:** `✓ 8 modules transformed. dist/assets/index-BN5Brtut.js (449.10 kB). Built in 696ms with 0 errors.`

### 2. Prior Phase 12E.1 and Phase 12F Reported Audits
- **Phase 12E.1 Audit (`docs/PHASE_12E1_ACCEPTANCE_AUDIT.md`):** Resolved TC-08 identity as Held-Out Fuzzers (`xgb_holdout_Fuzzers.json`); 17 targeted tests passed.
- **Phase 12F Validation (`docs/PHASE_12F_DEMONSTRATION_VALIDATION_REPORT.md`):** Confirmed 20 of 20 verification checks passed.
- **Critical Defects Previously Fixed:**
  1. *JavaScript `||` Fallback Bug:* Fixed bug where 0 values in `evidence_items.length` fell back to default counts.
  2. *Noise Node Leakage:* Fixed issue where `EV_NOISE_99` was erroneously rendered in unrelated scenarios.
  3. *Unintended Groq Burning:* Fixed re-render loops and automatic startup invocations.

---

## Section J: Hackathon Presentation & Live-Demo Strategy

### 1. Allocation of the 10-Minute Presentation Window
- **Minutes 0:00 – 6:00 (Slide Pitch):**
  - Problem statement: Alert fatigue and zero-day blind spots in modern SOCs.
  - The ThreatWeave approach: Hybrid detection + bounded graph reconstruction + grounded AI.
  - Model benchmarks: Supervised ($99.88\%$ recall), Zero-shot holdouts ($68.6\%$ and $100\%$).
  - Scientific honesty: Explaining the domain-shift stress test on ToN-IoT.
- **Minutes 6:00 – 10:00 (Live Prototype Demonstration):**
  - Execute live sequence below.
- **Post-Presentation (5:00):** Q&A session.

### 2. Planned 4-Minute Demonstration Sequence
1. **TC-01 (Benign Baseline):** Show 0 false alarms on normal traffic.
2. **TC-02 (Known Exploits):** Execute live replay; highlight supervised detection ($p > 0.998$) and T1210 MITRE mapping.
3. **TC-10 (Full Multi-Stage Campaign):**
   - Click "Execute Scenario". Watch the 9-stage pipeline animate.
   - Switch to **Attack Graph**: Inspect the 8-node attack chain and the isolated noise node (`EV_NOISE_99`).
   - Switch to **MITRE Matrix**: Show dynamic technique mapping across 4 tactics.
   - Switch to **AI Explanation**: Highlight grounded Groq synthesis and click **Download Report (.md)**.

### 3. Scientifically Defensible Judge Q&A Answers

#### Q1: "Are these models running live on every button click?"
> *"ThreatWeave implements a bifurcated architecture. For our live SOC demonstration, scenario replays serve pre-computed model predictions generated offline from the untouched 15% evaluation split of NF-UNSW-NB15-v2. This guarantees deterministic sub-10ms response times without live disk I/O bottlenecks. However, all predictions in TC-01 through TC-07 represent genuine inferences from our frozen XGBoost and Isolation Forest models."*

#### Q2: "Why does TC-10 have rounded scores like 0.99 and 0.10?"
> *"TC-10 is a controlled multi-stage APT replay fixture created during Phase 4. NetFlow datasets consist of isolated flow records rather than full multi-hop kill-chains spanning internal subnets. TC-10 was calibrated to test our correlation engine, graph reconstruction, noise pruning, and LLM triage narrative. We explicitly document TC-10 as a controlled fixture rather than misrepresenting it as raw UNSW data."*

#### Q3: "Does this detect zero-day attacks?"
> *"We evaluate zero-day capability through rigorous holdout experiments. When we completely withheld the Fuzzers and Reconnaissance families from training, our models achieved 68.64% zero-shot recall on Fuzzers and 100% on Reconnaissance. Furthermore, our unsupervised Isolation Forest flags abnormal behavioral outliers even when the supervised detector outputs zero probability (as demonstrated in TC-04)."*

#### Q4: "How do you prevent the LLM from hallucinating?"
> *"Our LLM prompt is strictly evidence-bounded: we serialize only verified graph nodes, correlation edges, and MITRE mappings into the prompt with temperature 0.1 and strict negative system constraints. If the LLM API is unavailable, our deterministic fallback engine constructs a verified narrative purely from graph facts."*

---

## Section K: Workstream Allocations & Team Responsibilities

*Note: Proposed team responsibility allocations based on hackathon workstreams.*

| Workstream | Proposed Focus Areas | Primary Artifacts |
| :--- | :--- | :--- |
| **1. Supervised ML & Benchmarking** | XGBoost, Random Forest, LightGBM, Holdout experiments | `models/xgboost_detector.json`<br>`experiments/detection_benchmark/`<br>`experiments/unseen_attack/` |
| **2. Anomaly Detection & Stress Testing** | Isolation Forest, Autoencoder, Cross-dataset ToN-IoT | `models/isolation_forest.joblib`<br>`experiments/anomaly_benchmark/`<br>`experiments/cross_dataset_real/` |
| **3. Backend, Correlation & Threat Intel** | FastAPI API, NetworkX correlation, MITRE mapper | `backend/app/main.py`<br>`backend/app/services/correlation.py`<br>`backend/app/services/mitre_mapper.py` |
| **4. Frontend, AI Explanation & Integration** | React UI, Cytoscape graph, Groq explainer, Handover | `frontend-react/src/`<br>`backend/app/services/llm_explainer.py`<br>`docs/` |

---

## Section L: Engineering Decision History & Rationale

1. **Feature Freeze & Zero Code Changes Rule:** Post-Phase 12E, the team froze all model weights, thresholds, and schemas to eliminate regression risks before judging.
2. **Resolution of TC-08 Provenance:** An errant documentation label previously identified TC-08 as Backdoor. Physical artifact auditing confirmed TC-08 is Held-Out Fuzzers (`xgb_holdout_Fuzzers.json`). The label was corrected without fabricating nonexistent Backdoor models.
3. **Disabling TC-05:** The Neural Autoencoder was an offline research experiment without serialized inference weights. Rather than simulating inference, TC-05 was explicitly disabled with an honest diagnostic banner.
4. **Distinction Between Replay and Fixtures:** Formally differentiated TC-01..TC-04 and TC-06..TC-07 (genuine pre-computed model predictions) from TC-10 (controlled multi-stage fixture).
5. **On-Demand LLM Execution:** Moved Groq API calls from automatic mount-time execution to explicit button clicks, preventing accidental token burn and rate-limit exhaustion.

---

## Section M: Final Freeze Rules & Immediate Checklist

### Strict Pre-Judging Freeze Rules
- **DO NOT retrain models.** All weights in `models/` are frozen.
- **DO NOT modify feature columns or thresholds.** Thresholds ($0.51$ for XGBoost, $0.0094$ for Isolation Forest) are immutable.
- **DO NOT alter scenario caches.** JSON files in `backend/app/cache/` are verified.
- **DO NOT add unverified detection capabilities.**
- **DO NOT redesign UI layouts.**

### Immediate Pre-Judging Checklist
- [x] Verify backend server running: `http://127.0.0.1:8000/health` $\to$ `{"status": "ok"}`
- [x] Verify React frontend running: `http://127.0.0.1:5173`
- [x] Test TC-01 replay in Scenario Lab (verify 0 alerts)
- [x] Test TC-02 replay in Scenario Lab (verify exploit detection)
- [x] Test TC-10 replay in Scenario Lab (verify 8 events, 20 edges)
- [x] Inspect Attack Graph for TC-10 (verify Cytoscape canvas and noise node)
- [x] Check AI Explanation page (verify report download works)
- [x] Rehearse 6-minute slide pitch and 4-minute prototype demo

---

## Section N: Local Evidence & Artifact Index

### Core Documentation
- `docs/THREATWEAVE_COMPLETE_HANDOVER.md` *(This file)*
- [`docs/PHASE_12E1_ACCEPTANCE_AUDIT.md`](file:///d:/Zephyr/ThreatWeave/docs/PHASE_12E1_ACCEPTANCE_AUDIT.md)
- [`docs/PHASE_12F_DEMONSTRATION_VALIDATION_REPORT.md`](file:///d:/Zephyr/ThreatWeave/docs/PHASE_12F_DEMONSTRATION_VALIDATION_REPORT.md)
- [`docs/CLAIMS_AUDIT.md`](file:///d:/Zephyr/ThreatWeave/docs/CLAIMS_AUDIT.md)

### Model Artifacts
- [`models/xgboost_detector.json`](file:///d:/Zephyr/ThreatWeave/models/xgboost_detector.json) (Production XGBoost)
- [`models/isolation_forest.joblib`](file:///d:/Zephyr/ThreatWeave/models/isolation_forest.joblib) (Production Isolation Forest)
- [`models/random_forest_baseline.joblib`](file:///d:/Zephyr/ThreatWeave/models/random_forest_baseline.joblib) (Baseline RF)
- [`models/feature_columns.json`](file:///d:/Zephyr/ThreatWeave/models/feature_columns.json) (41 features)
- [`experiments/unseen_attack/models/xgb_holdout_Fuzzers.json`](file:///d:/Zephyr/ThreatWeave/experiments/unseen_attack/models/xgb_holdout_Fuzzers.json)
- [`experiments/unseen_attack/models/xgb_holdout_Reconnaissance.json`](file:///d:/Zephyr/ThreatWeave/experiments/unseen_attack/models/xgb_holdout_Reconnaissance.json)

### Scripts & Generators
- [`scripts/generate_verified_scenarios.py`](file:///d:/Zephyr/ThreatWeave/scripts/generate_verified_scenarios.py) (Scenario cache generator)
- [`scripts/e2e_scenario_validation.py`](file:///d:/Zephyr/ThreatWeave/scripts/e2e_scenario_validation.py) (E2E validator)
- [`scripts/train_supervised.py`](file:///d:/Zephyr/ThreatWeave/scripts/train_supervised.py)
- [`scripts/train_anomaly.py`](file:///d:/Zephyr/ThreatWeave/scripts/train_anomaly.py)

### Backend Codebase
- [`backend/app/main.py`](file:///d:/Zephyr/ThreatWeave/backend/app/main.py)
- [`backend/app/services/demo_scenario_service.py`](file:///d:/Zephyr/ThreatWeave/backend/app/services/demo_scenario_service.py)
- [`backend/app/services/llm_explainer.py`](file:///d:/Zephyr/ThreatWeave/backend/app/services/llm_explainer.py)
- [`backend/app/services/correlation.py`](file:///d:/Zephyr/ThreatWeave/backend/app/services/correlation.py)
- [`backend/app/services/mitre_mapper.py`](file:///d:/Zephyr/ThreatWeave/backend/app/services/mitre_mapper.py)
- [`backend/app/schemas/incident.py`](file:///d:/Zephyr/ThreatWeave/backend/app/schemas/incident.py)
- [`backend/app/cache/`](file:///d:/Zephyr/ThreatWeave/backend/app/cache) (`TC-01.json` through `TC-10.json`)

### Frontend Codebase
- [`frontend-react/src/context/IncidentContext.tsx`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/context/IncidentContext.tsx)
- [`frontend-react/src/types/scenario.ts`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/types/scenario.ts)
- [`frontend-react/src/services/api.ts`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/services/api.ts)
- [`frontend-react/src/pages/ScenarioLab.tsx`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/pages/ScenarioLab.tsx)
- [`frontend-react/src/pages/AttackGraph.tsx`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/pages/AttackGraph.tsx)
- [`frontend-react/src/pages/AiExplanation.tsx`](file:///d:/Zephyr/ThreatWeave/frontend-react/src/pages/AiExplanation.tsx)

---
*End of Complete Project Handover Document.*
