import json
import re
from pathlib import Path
from fastapi import HTTPException
from app.schemas.incident import StructuredIncident

class DemoScenarioService:
    def __init__(self):
        self.cache_dir = Path("backend/app/cache")
        
    def get_scenarios(self):
        try:
            with open(self.cache_dir / "scenarios.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
            
    def get_scenario_incident(self, scenario_id: str) -> StructuredIncident:
        if not re.match(r"^[A-Za-z0-9_-]+$", scenario_id):
            raise HTTPException(status_code=400, detail="Invalid scenario identifier format")
            
        if scenario_id == "TC-05":
            raise HTTPException(
                status_code=404, 
                detail="Scenario 'TC-05' is disabled: Autoencoder model weights do not exist on disk for live inference."
            )

        file_path = self.cache_dir / f"{scenario_id}.json"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found or unavailable.")
            
        with open(file_path, "r") as f:
            data = json.load(f)
            return StructuredIncident(**data)
