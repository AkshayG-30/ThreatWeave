# THREATWEAVE — AUDIT RECORD

## Verification Status

| Claim / Feature | Status | Notes |
| :--- | :--- | :--- |
| **Project Root & Setup** | VERIFIED | `D:\Zephyr\ThreatWeave` exists and contains backend, frontend, scripts, and experiments. |
| **Git Repository** | UNVERIFIED | `git status` returned `fatal: not a git repository`. |
| **Pytest 27/27** | VERIFIED | Passing as of Phase 10D. |
| **Frontend Build** | VERIFIED | Vite production build passing as of Phase 10D. |
| **Production XGBoost** | VERIFIED | Model frozen. Artifacts exist. |
| **LightGBM Benchmark** | VERIFIED | Exists in `experiments/detection_benchmark/`. |
| **Autoencoder vs Isolation Forest** | VERIFIED | Exists in `experiments/anomaly_benchmark/`. |
| **Unraveled / SAGA Validation** | NOT IMPLEMENTED | Feasibility audit proved viable, but adapter not built. |
| **NF-ToN-IoT Integration** | REJECTED | Dataset incompatible (31/41 features missing). |
| **GNN / GRU Models** | NOT IMPLEMENTED | Feasibility tested, but aborted to prevent scientific fabrication. |
| **TC-10 Scenario** | VERIFIED | Present in cache and fully functional in URL-driven frontend. |
| **TC-01 through TC-09 Scenarios** | UNVERIFIED / BLOCKED | Backend cache generation mechanism built, but scenarios unpopulated due to offline processing overhead. |
| **Groq LLM Fallback** | VERIFIED | 401 Unauthorized securely caught and routed to deterministic offline fallback. |
| **No API Keys in Frontend** | VERIFIED | `.env` securely isolated. |

*This audit document serves as the absolute source of truth for the new chat session. Do not override these statuses without explicit physical verification of the codebase.*
