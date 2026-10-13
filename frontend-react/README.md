# ThreatWeave — Standalone React Frontend (Phase 12)

ThreatWeave enterprise SOC operations and multi-stage cyber attack reconstruction interface. Inspired by modern SOC operations consoles (SentinelX reference design), built with React, TypeScript, and Vite.

## Architecture
- **Framework:** React 18 + TypeScript + Vite
- **Graph Reconstruction:** Cytoscape.js directed topology engine
- **Design System:** Custom Enterprise SOC design tokens (`tokens.css`, `index.css`)
- **Backend API:** FastAPI (`http://127.0.0.1:8000`)
- **Routing:** Hash-based multi-page router covering 9 operational SOC views

## Directory Structure
```
frontend-react/
├── .env                # Backend URL configuration (VITE_API_BASE_URL)
├── .env.example        # Environment variable template
├── index.html          # Shell with Inter & JetBrains Mono typography
├── package.json        # Dependencies (React, Vite, Lucide, Cytoscape)
├── tsconfig.json       # Strict TypeScript configuration
├── vite.config.ts      # Vite configuration (port 5174)
└── src/
    ├── assets/         # Icons and static SVG assets
    ├── components/     # Reusable SOC components (PageHeader, StatusBadge, Cards)
    ├── hooks/          # React hooks
    ├── layouts/        # AppLayout shell with top navbar and navigation pills
    ├── pages/          # 9 required pages
    │   ├── SecurityOverview.tsx
    │   ├── ScenarioLab.tsx
    │   ├── ModelEvaluation.tsx
    │   ├── CrossDataset.tsx
    │   ├── UnseenAttack.tsx
    │   ├── AttackGraph.tsx
    │   ├── MitreMapping.tsx
    │   ├── AiExplanation.tsx
    │   └── Methodology.tsx
    ├── services/       # Typed ApiService client
    ├── styles/         # SOC tokens and stylesheet
    └── types/          # Pydantic-mirrored TypeScript definitions
```

## Startup Commands

### 1. Backend Service (Terminal 1)
```powershell
# From project root: D:\Zephyr\ThreatWeave
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH="backend"
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 2. Frontend Application (Terminal 2)
```powershell
cd D:\Zephyr\ThreatWeave\frontend-react
npm install
npm run dev
```
Open your browser at `http://localhost:5174`.

### 3. Production Build & Validation
```powershell
cd D:\Zephyr\ThreatWeave\frontend-react
npm run build
```
Build output is generated into `dist/`.

## Security Notice
The Groq API key is strictly isolated in the backend environment. The frontend code never possesses or interacts with raw LLM provider tokens.
