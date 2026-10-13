# ThreatWeave

## 1. What ThreatWeave is
ThreatWeave is an AI-driven cybersecurity framework designed for detecting known and previously unseen attack behaviour. It correlates security events, reconstructs multi-stage attack chains, maps them to MITRE ATT&CK, and generates evidence-grounded incident explanations.

## 2. Problem Being Solved
Modern security operations centers (SOCs) are overwhelmed with isolated alerts. ThreatWeave aims to reduce alert fatigue by contextualizing and correlating network and host events into comprehensive attack campaigns, providing interpretable AI-driven insights.

## 3. Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla TypeScript & Vite
- **Supervised ML**: XGBoost
- **Anomaly Detection**: Isolation Forest
- **Correlation Engine**: Bounded Graph Correlation
- **LLM Integration**: Groq API (openai/gpt-oss-120b or mixtral)

## 4. Project Structure
```
ThreatWeave/
├── backend/       # FastAPI app, Schemas, ML Models, Pipelines
├── frontend/      # Vite/TypeScript SOC dashboard
├── data/          # Raw, processed, metadata, and samples
├── models/        # Saved model binaries
├── notebooks/     # Exploratory Data Analysis
├── scripts/       # Demo & ML Utilities
├── experiments/   # ML experiment tracking & metrics
├── tests/         # Unit and integration tests
└── docs/          # Architecture and design documents
```

## 5. Setup & Environment
1. Ensure Python 3.12+ and Node.js are installed.
2. Clone the repository and install backend dependencies into a virtual environment:
   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r backend/requirements.txt
   ```
3. Set up your `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_key_here
   GROQ_MODEL=openai/gpt-oss-120b
   ```
4. Set up the frontend `.env` file in `frontend/.env`:
   ```env
   VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

## 6. How to Launch the Demo

### Start the Backend
With the virtual environment activated from the root directory (`D:\Zephyr\ThreatWeave`):
```powershell
$env:PYTHONPATH="backend"
.\.venv\Scripts\uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Demo API Endpoints:
- `GET http://127.0.0.1:8000/api/demo/incident`
- `GET http://127.0.0.1:8000/api/demo/explanation`

### Start the Frontend
In a new terminal window:
```powershell
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

## 7. Dashboard Features
- **Attack Chain Graph**: Visualizes the progression from Recon to C2/Exfiltration using Cytoscape.js.
- **Evidence-Grounded AI Analysis**: Uses Groq LLM to explain the attack chain deterministically.
- **MITRE ATT&CK Mapping**: Maps network scanning, remote exploitation, and C2 channels.
- **Threat Level & Metric Cards**: Summarizes incident severity and correlation scores.

## 8. Current Implementation Status
- ✅ **Phase 1**: Python 3.12 Environment & Setup
- ✅ **Phase 2**: Dataset Acquisition & ML Detection (XGBoost, Isolation Forest)
- ✅ **Phase 3**: Bounded Graph Correlation Engine
- ✅ **Phase 4**: MITRE ATT&CK Mapping & LLM Incident Explainer
- ✅ **Phase 5**: SOC Frontend Dashboard & API Integration (Vite + TS)
