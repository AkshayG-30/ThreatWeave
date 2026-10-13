# Demo Startup Guide

## Starting Directory
Ensure you are operating in the root directory:
```powershell
cd D:\Zephyr\ThreatWeave
```

## 1. Activate Virtual Environment
Before running any commands, the virtual environment must be active:
```powershell
.\.venv\Scripts\Activate.ps1
```

## 2. Start Backend
The backend utilizes FastAPI running on Uvicorn.
```powershell
$env:PYTHONPATH="backend"
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
**Backend URL**: `http://127.0.0.1:8000`

## 3. Start Frontend
In a new terminal window, navigate to the frontend directory and start the Vite development server.
```powershell
cd frontend
npm run dev
```
**Frontend URL**: `http://localhost:5173`

## Expected Dashboard State
Upon opening `http://localhost:5173`:
- The backend status light should show green (Healthy).
- The threat summary metric cards should display detection data.
- The Cytoscape network map should actively render nodes (EV_01-EV_08 connected, EV_09 isolated).
- AI explanation cards should be visible at the bottom.

## How to Stop Services
- In the backend terminal: Press `Ctrl + C`
- In the frontend terminal: Press `Ctrl + C` or `q` + `Enter`
