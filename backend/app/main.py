from fastapi import FastAPI, HTTPException
import json
import os
import re
from typing import Optional
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.incident import StructuredIncident, LLMExplanation
from app.services.llm_explainer import LLMExplainer
from app.services.demo_scenario_service import DemoScenarioService

demo_service = DemoScenarioService()

load_dotenv()

app = FastAPI(title="ThreatWeave API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ThreatWeave"
    }

@app.get("/api/demo/incident", response_model=StructuredIncident)
def get_demo_incident():
    try:
        with open("experiments/phase4/synthetic_incident.json", "r") as f:
            data = json.load(f)
            return StructuredIncident(**data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Synthetic incident not found. Run Phase 4 script first.")

@app.get("/api/demo/explanation", response_model=LLMExplanation)
def get_demo_explanation(scenario_id: Optional[str] = None):
    target_id = scenario_id or "TC-10"
    
    # Path traversal protection: whitelist scenario ID format
    if not re.match(r"^[A-Za-z0-9_-]+$", target_id):
        raise HTTPException(status_code=400, detail="Invalid scenario identifier format")
        
    if target_id == "TC-05":
        raise HTTPException(
            status_code=404, 
            detail="Scenario 'TC-05' is disabled: Autoencoder model weights do not exist on disk for live inference."
        )

    cache_path = os.path.join("backend", "app", "cache", f"{target_id}.json")
    if not os.path.exists(cache_path):
        if target_id == "TC-10" and os.path.exists("experiments/phase4/synthetic_incident.json"):
            cache_path = "experiments/phase4/synthetic_incident.json"
        else:
            raise HTTPException(status_code=404, detail=f"Scenario '{target_id}' not found or unavailable.")
            
    try:
        with open(cache_path, "r") as f:
            data = json.load(f)
            incident = StructuredIncident(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load scenario data: {str(e)}")
        
    explainer = LLMExplainer()
    return explainer.explain(incident, scenario_id=target_id)

@app.get("/api/demo/scenarios")
def get_scenarios():
    return demo_service.get_scenarios()

@app.get("/api/demo/scenario/{scenario_id}", response_model=StructuredIncident)
def get_scenario(scenario_id: str):
    return demo_service.get_scenario_incident(scenario_id)
