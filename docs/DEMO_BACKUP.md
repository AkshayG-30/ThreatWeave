# Demo Backup / Recovery Guide

If you encounter technical issues during the live demonstration, use these recovery procedures. **Do not fabricate results or use fake endpoints under any circumstances.**

## 1. Backend Fails
- **Symptom:** UI displays "Service Offline" or API requests 500/502.
- **Action:** 
  1. Halt the process in terminal (`Ctrl+C`).
  2. Verify virtual environment is active (`.\.venv\Scripts\Activate.ps1`).
  3. Verify `PYTHONPATH` is strictly set (`$env:PYTHONPATH="backend"`).
  4. Restart: `uvicorn app.main:app --host 127.0.0.1 --port 8000`.

## 2. Frontend Fails / Cannot Connect to Backend
- **Symptom:** White screen, missing graph, or CORS errors.
- **Action:**
  1. Press `F12` to check browser console for exact errors.
  2. Ensure the backend is correctly running on `127.0.0.1:8000` (Vite's proxy requires this exact port).
  3. Ensure `npm run dev` is running. 
  4. Refresh the browser using `Ctrl+F5` (hard refresh).

## 3. Groq Fails / Internet is Unavailable
- **Symptom:** API timeouts, rate-limit failures (HTTP 429), or missing `GROQ_API_KEY`.
- **Action:** Do absolutely nothing! ThreatWeave is intentionally designed with an autonomous, offline-first fallback. If the Groq client is unreachable or errors out, the pipeline deterministically injects a rule-based explanation utilizing the existing MITRE data and incident graphs. The demo will continue functionally without interruption. State clearly to the judges: "Our external LLM provider experienced an interruption, and our deterministic offline safety fallback successfully caught the failure to preserve SOC visibility."
