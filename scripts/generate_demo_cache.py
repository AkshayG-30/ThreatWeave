import os
import json
from pathlib import Path

def main():
    print("Generating deterministic demo cache from existing models...")
    cache_dir = Path("backend/app/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # We will copy the synthetic incident as TC-10
    with open("experiments/phase4/synthetic_incident.json", "r") as f:
        synthetic = json.load(f)
        
    with open(cache_dir / "TC-10.json", "w") as f:
        json.dump(synthetic, f, indent=4)
        
    scenarios = [
        {
            "id": "TC-10",
            "name": "Full Multi-Stage APT Replay",
            "description": "Controlled multi-stage incident demonstrating correlation, graph reconstruction, MITRE mapping and evidence-grounded explanation.",
            "source": "CONTROLLED_REPLAY",
            "primary_capability": "END_TO_END",
            "stages": ["DETECTION", "ANOMALY", "CORRELATION", "GRAPH", "MITRE", "AI"]
        }
    ]
    
    with open(cache_dir / "scenarios.json", "w") as f:
        json.dump(scenarios, f, indent=4)
        
    print("Demo cache generated safely without modifying production models.")

if __name__ == "__main__":
    main()
