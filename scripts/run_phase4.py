import sys
import json
import uuid
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

sys.path.append('backend')
from app.services.pipeline import DataPipeline
from app.services.correlation import CorrelationEngine
from app.services.mitre_mapper import MitreMapper
from app.services.llm_explainer import LLMExplainer
from app.schemas.incident import StructuredIncident, IncidentEvent
from xgboost import XGBClassifier
import joblib

def main():
    load_dotenv()
    exp_dir = Path("experiments/phase4")
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    print("Initializing components...")
    pipeline = DataPipeline(random_state=42)
    xgb = XGBClassifier()
    xgb.load_model("models/xgboost_detector.json")
    iso = joblib.load("models/isolation_forest.joblib")
    
    try:
        with open("experiments/phase2c/config.json", "r") as f:
            cfg = json.load(f)
            iso_threshold = cfg["selected_threshold"]
    except:
        iso_threshold = 0.0094
        
    print("Loading data...")
    try:
        df = pd.read_parquet(r"D:\Zephyr\ThreatWeave\data\processed\nf_unsw_nb15_v2_sample_150k.parquet")
    except ImportError:
        df = pd.read_csv(r"D:\Zephyr\ThreatWeave\data\processed\nf_unsw_nb15_v2_sample_150k.csv")
        
    train_df, _, test_df = pipeline.split_data(df, stratify_col='Attack')
    X_train_raw, _, _ = pipeline.select_features(train_df)
    pipeline.normalize(pipeline.numeric_conversion(X_train_raw), is_train=True)
    
    X_test_raw, y_test, attack_test = pipeline.select_features(test_df)
    X_test_num = pipeline.numeric_conversion(X_test_raw)
    X_test = pipeline.normalize(X_test_num, is_train=False)
    
    xgb_preds = xgb.predict(X_test)
    xgb_probs = xgb.predict_proba(X_test)[:, 1]
    iso_scores = -iso.decision_function(X_test)
    iso_preds = (iso_scores > iso_threshold).astype(int)
    
    suspicious_events = []
    X_test_raw = X_test_raw.reset_index(drop=True)
    
    for i in range(len(X_test_raw)):
        is_xgb = (xgb_preds[i] == 1)
        is_iso = (iso_preds[i] == 1)
        
        if is_xgb and is_iso: src = "BOTH"
        elif is_xgb: src = "SUPERVISED"
        elif is_iso: src = "ANOMALY"
        else: continue
            
        row = X_test_raw.iloc[i]
        suspicious_events.append({
            "event_id": str(uuid.uuid4()),
            "timestamp": None,
            "timestamp_source": None,
            "source_ip": str(row.get('IPV4_SRC_ADDR')),
            "destination_ip": str(row.get('IPV4_DST_ADDR')),
            "source_port": int(row.get('L4_SRC_PORT', 0)),
            "destination_port": int(row.get('L4_DST_PORT', 0)),
            "protocol": str(row.get('PROTOCOL', '')),
            "supervised_score": float(xgb_probs[i]),
            "anomaly_score": float(iso_scores[i]),
            "detection_source": src
        })
        
    engine = CorrelationEngine(temporal_window=30.0, edge_threshold=1.0)
    G_real = engine.correlate(suspicious_events)
    incidents_real = engine.get_candidate_incidents(G_real)
    
    real_results = {
        "suspicious_events": len(suspicious_events),
        "candidate_incidents": len(incidents_real),
        "message": "No candidate incident met the correlation evidence threshold." if len(incidents_real) == 0 else f"Found {len(incidents_real)} incidents."
    }
    with open(exp_dir / "real_data_result.json", "w") as f:
        json.dump(real_results, f, indent=4)
        
    print("Running Synthetic Demo Replay...")
    base_time = 1700000000.0
    demo_events = [
        {"event_id": "EV_01_RECON", "timestamp": base_time, "timestamp_source": "DEMO_REPLAY", "source_ip": "10.0.0.5", "destination_ip": "192.168.1.10", "detection_source": "ANOMALY", "supervised_score": 0.1, "anomaly_score": 0.8, "source_port": 1234, "destination_port": 80, "protocol": "TCP"},
        {"event_id": "EV_02_RECON", "timestamp": base_time + 5, "timestamp_source": "DEMO_REPLAY", "source_ip": "10.0.0.5", "destination_ip": "192.168.1.11", "detection_source": "ANOMALY", "supervised_score": 0.1, "anomaly_score": 0.8, "source_port": 1235, "destination_port": 80, "protocol": "TCP"},
        {"event_id": "EV_03_SCAN", "timestamp": base_time + 10, "timestamp_source": "DEMO_REPLAY", "source_ip": "10.0.0.5", "destination_ip": "192.168.1.12", "detection_source": "BOTH", "supervised_score": 0.9, "anomaly_score": 0.9, "source_port": 1236, "destination_port": 445, "protocol": "TCP"},
        {"event_id": "EV_04_EXPLOIT", "timestamp": base_time + 15, "timestamp_source": "DEMO_REPLAY", "source_ip": "10.0.0.5", "destination_ip": "192.168.1.12", "detection_source": "SUPERVISED", "supervised_score": 0.99, "anomaly_score": 0.1, "source_port": 1237, "destination_port": 445, "protocol": "TCP"},
        {"event_id": "EV_05_C2", "timestamp": base_time + 20, "timestamp_source": "DEMO_REPLAY", "source_ip": "192.168.1.12", "destination_ip": "185.15.2.1", "detection_source": "ANOMALY", "supervised_score": 0.1, "anomaly_score": 0.85, "source_port": 4444, "destination_port": 8080, "protocol": "TCP"},
        {"event_id": "EV_06_C2", "timestamp": base_time + 25, "timestamp_source": "DEMO_REPLAY", "source_ip": "192.168.1.12", "destination_ip": "185.15.2.1", "detection_source": "ANOMALY", "supervised_score": 0.1, "anomaly_score": 0.85, "source_port": 4445, "destination_port": 8080, "protocol": "TCP"},
        {"event_id": "EV_07_EXFIL", "timestamp": base_time + 28, "timestamp_source": "DEMO_REPLAY", "source_ip": "192.168.1.12", "destination_ip": "185.15.2.1", "detection_source": "BOTH", "supervised_score": 0.9, "anomaly_score": 0.9, "source_port": 4446, "destination_port": 8080, "protocol": "TCP"},
        {"event_id": "EV_08_LATERAL", "timestamp": base_time + 35, "timestamp_source": "DEMO_REPLAY", "source_ip": "192.168.1.12", "destination_ip": "192.168.1.15", "detection_source": "SUPERVISED", "supervised_score": 0.9, "anomaly_score": 0.2, "source_port": 5000, "destination_port": 445, "protocol": "TCP"},
        {"event_id": "EV_09_NOISE", "timestamp": base_time + 40, "timestamp_source": "DEMO_REPLAY", "source_ip": "8.8.8.8", "destination_ip": "192.168.1.50", "detection_source": "ANOMALY", "supervised_score": 0.1, "anomaly_score": 0.7, "source_port": 123, "destination_port": 53, "protocol": "UDP"},
    ]
    
    G_demo = engine.correlate(demo_events)
    incidents_demo = engine.get_candidate_incidents(G_demo)
    incidents_demo.sort(key=lambda x: x['event_count'], reverse=True)
    best_incident = incidents_demo[0]
    
    # 4. Phase 4 - MITRE and Structure
    mapper = MitreMapper()
    
    # Extract nodes and edges for the subgraph
    subgraph = G_demo.subgraph(best_incident["ordered_events"])
    inc_events = [data for _, data in subgraph.nodes(data=True)]
    
    edges_list = []
    for u, v, data in subgraph.edges(data=True):
        edges_list.append({"source": u, "target": v, **data})
        
    mappings = mapper.map_incident(inc_events, edges_list)
    evidence_items = mapper.generate_evidence_items(inc_events, edges_list)
    
    struct_inc = StructuredIncident(
        incident_id=best_incident["incident_id"],
        event_count=best_incident["event_count"],
        events=[IncidentEvent(**e) for e in inc_events],
        edges=edges_list,
        correlation_score=sum(e['weight'] for e in edges_list),
        detection_summary={"supervised_avg": 0.5, "anomaly_avg": 0.5},
        mitre_mappings=mappings,
        evidence_items=evidence_items,
        confidence="HIGH",
        timestamp_source="DEMO_REPLAY",
        limitations=["Timestamps are synthetic replay only", "No deep payload parsing"]
    )
    
    with open(exp_dir / "synthetic_incident.json", "w") as f:
        f.write(struct_inc.model_dump_json(indent=4))
        
    # 5. Explainer
    explainer = LLMExplainer()
    explanation = explainer.explain(struct_inc)
    
    report = f"""# Phase 4 MITRE Mapping and Explanation

## Reconstructed Chain
{explanation.attack_chain}

## Evidence Grounding
{explanation.evidence}

## MITRE Techniques
{explanation.mitre_techniques}

## Confidence
{explanation.confidence}

## Limitations
{explanation.limitations}

## Raw Output
```json
{explanation.model_dump_json(indent=4)}
```
"""
    with open(exp_dir / "synthetic_incident_report.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print("Phase 4 Complete.")

if __name__ == "__main__":
    main()
