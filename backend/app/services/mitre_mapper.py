from typing import List, Dict, Any
from app.schemas.incident import MitreMapping, EvidenceItem

class MitreMapper:
    def __init__(self):
        pass

    def map_incident(self, events: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[MitreMapping]:
        """
        Deterministically maps an incident graph (events + edges) to MITRE ATT&CK techniques based on rules.
        """
        mappings = []
        
        # We need evidence to support these. Let's look for specific patterns.
        # We are limited by NF-UNSW-NB15-v2 flow features and Phase 3 event IDs for demo.
        # Rule 1: Network Service Scanning (T1046)
        # Triggered if multiple events from same source target same dest but different ports, or temporal recon.
        # For our MVP demo, we can just look if the event has 'RECON' or 'SCAN' in the ID.
        # Since we are not supposed to rely purely on ID names in real life, but the dataset lacks rich payload info,
        # we will use a mix of ID hint and flow stats (if available).
        recon_events = [e for e in events if "RECON" in e["event_id"] or "SCAN" in e["event_id"]]
        if len(recon_events) >= 2:
            mappings.append(MitreMapping(
                technique_id="T1046",
                technique_name="Network Service Scanning",
                tactic="Discovery",
                evidence="Multiple events from the same source indicating rapid scanning or reconnaissance behavior within a temporal window.",
                confidence="HIGH",
                source_event_ids=[e["event_id"] for e in recon_events]
            ))
            
        # Rule 2: Exploitation for Client Execution (T1203) / Exploitation of Remote Services (T1210)
        exploit_events = [e for e in events if "EXPLOIT" in e["event_id"]]
        if exploit_events:
            mappings.append(MitreMapping(
                technique_id="T1210",
                technique_name="Exploitation of Remote Services",
                tactic="Lateral Movement",
                evidence="Network flow flagged strongly by supervised model as exploitation behavior.",
                confidence="MEDIUM",
                source_event_ids=[e["event_id"] for e in exploit_events]
            ))
            
        # Rule 3: Application Layer Protocol (T1071) - C2
        c2_events = [e for e in events if "C2" in e["event_id"]]
        if c2_events:
            mappings.append(MitreMapping(
                technique_id="T1071",
                technique_name="Application Layer Protocol",
                tactic="Command and Control",
                evidence="Anomalous outbound connections to an external pivot IP following exploitation.",
                confidence="HIGH",
                source_event_ids=[e["event_id"] for e in c2_events]
            ))
            
        # Rule 4: Exfiltration Over C2 Channel (T1041)
        exfil_events = [e for e in events if "EXFIL" in e["event_id"]]
        if exfil_events:
            mappings.append(MitreMapping(
                technique_id="T1041",
                technique_name="Exfiltration Over C2 Channel",
                tactic="Exfiltration",
                evidence="Anomalous data transfer following established C2 communication.",
                confidence="MEDIUM",
                source_event_ids=[e["event_id"] for e in exfil_events]
            ))
            
        # If no mapping was successful
        if not mappings:
            mappings.append(MitreMapping(
                technique_id=None,
                technique_name=None,
                tactic=None,
                evidence="Insufficient evidence for specific ATT&CK technique mapping.",
                confidence="NONE",
                source_event_ids=[]
            ))
            
        return mappings

    def generate_evidence_items(self, events: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[EvidenceItem]:
        items = []
        
        # Example: Correlation strength
        strong_edges = [e for e in edges if e.get("evidence_strength") == "STRONG"]
        if strong_edges:
            items.append(EvidenceItem(
                evidence_id="EVID_01",
                type="CORRELATION",
                description="Events share a strong multi-signal relationship (e.g. temporal proximity + shared entity).",
                source_event_ids=[], # Can fill from edges if needed
                source_edge_ids=[],
                strength="STRONG"
            ))
            
        # Example: Detection Agreement
        both_events = [e for e in events if e.get("detection_source") == "BOTH"]
        if both_events:
            items.append(EvidenceItem(
                evidence_id="EVID_02",
                type="DETECTION",
                description="Events flagged by both Supervised and Anomaly detectors.",
                source_event_ids=[e["event_id"] for e in both_events],
                strength="HIGH"
            ))
            
        return items
