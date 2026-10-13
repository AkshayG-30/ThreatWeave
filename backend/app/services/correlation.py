import networkx as nx
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import itertools

class CorrelationEngine:
    def __init__(self, temporal_window: float = 30.0, edge_threshold: float = 1.0):
        self.temporal_window = temporal_window
        self.edge_threshold = edge_threshold
        
        # Evidence Hierarchy Weights
        self.weights = {
            "SAME_SOURCE_IP": 0.4,          # WEAK
            "SAME_DESTINATION_IP": 0.4,     # WEAK
            "SHARED_IP_BIDIR": 0.5,         # MEDIUM
            "SAME_SRC_AND_DST": 0.6,        # MEDIUM
            "SAME_SRC_DST_PORT": 0.3,       # Adds to SRC/DST
            "TEMPORAL": 0.6,                # STRONG when combined
            "DETECTION_AGREEMENT": 0.2      # WEAK bonus
        }

    def correlate(self, events: List[Dict[str, Any]]) -> nx.Graph:
        """
        Builds a NetworkX graph connecting suspicious events using bounded candidate generation
        and an evidence hierarchy threshold.
        """
        G = nx.Graph()
        
        for event in events:
            G.add_node(event["event_id"], **event)
            
        # 1. Bounded Candidate Generation (Avoid O(N^2) on weak attributes)
        # We index by composite keys that imply stronger relationships.
        candidate_pairs = set()
        
        # Index: (Source IP, Destination IP) -> captures SAME_SRC_AND_DST
        src_dst_idx = defaultdict(list)
        # Index: frozenset(IP1, IP2) -> captures SHARED_IP_BIDIR
        bidir_idx = defaultdict(list)
        
        # We also need to capture Temporal. For temporal, we only care about DEMO_REPLAY events.
        demo_events = []
        
        for event in events:
            src = event.get("source_ip")
            dst = event.get("destination_ip")
            if src and dst:
                src_dst_idx[(src, dst)].append(event)
                bidir_idx[frozenset([src, dst])].append(event)
                
            if event.get("timestamp_source") == "DEMO_REPLAY" and event.get("timestamp") is not None:
                demo_events.append(event)
                
        # Generate pairs from indices
        for group in src_dst_idx.values():
            if len(group) < 1000: # Sanity bound to prevent internal explosion if one pair is huge
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        candidate_pairs.add((group[i]["event_id"], group[j]["event_id"]))
                        
        for group in bidir_idx.values():
            if len(group) < 1000:
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        candidate_pairs.add((group[i]["event_id"], group[j]["event_id"]))
                        
        # Generate pairs from Temporal sliding window
        demo_events.sort(key=lambda x: x["timestamp"])
        for i in range(len(demo_events)):
            for j in range(i + 1, len(demo_events)):
                if demo_events[j]["timestamp"] - demo_events[i]["timestamp"] <= self.temporal_window:
                    candidate_pairs.add((demo_events[i]["event_id"], demo_events[j]["event_id"]))
                else:
                    break # Window exceeded
                    
        # 2. Evaluate Candidate Pairs
        for id1, id2 in candidate_pairs:
            e1 = G.nodes[id1]
            e2 = G.nodes[id2]
            
            score, reasons = self._evaluate_pair(e1, e2)
            
            if score >= self.edge_threshold:
                # Determine evidence strength
                strength = "WEAK"
                if score >= 1.5: strength = "STRONG"
                elif score >= 1.0: strength = "MEDIUM"
                
                G.add_edge(id1, id2, weight=score, reasons=reasons, evidence_strength=strength)
                
        return G

    def _evaluate_pair(self, e1: Dict[str, Any], e2: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]]]:
        score = 0.0
        reasons = []
        
        src1, dst1 = e1.get("source_ip"), e1.get("destination_ip")
        src2, dst2 = e2.get("source_ip"), e2.get("destination_ip")
        
        # Entity Relationships
        if src1 and dst1 and src1 == src2 and dst1 == dst2:
            score += self.weights["SAME_SRC_AND_DST"]
            reasons.append({"edge_type": "SAME_SRC_AND_DST", "reason": f"Events share Src->Dst {src1}->{dst1}"})
            
            # Check port overlap
            if e1.get("destination_port") and e1.get("destination_port") == e2.get("destination_port"):
                score += self.weights["SAME_SRC_DST_PORT"]
                reasons.append({"edge_type": "SAME_SRC_DST_PORT", "reason": "Events share destination port"})
                
        elif src1 and dst1 and src1 == dst2 and dst1 == src2:
            score += self.weights["SHARED_IP_BIDIR"]
            reasons.append({"edge_type": "SHARED_IP_BIDIR", "reason": f"Bidirectional flow between {src1} and {dst1}"})
            
        elif src1 and dst1 and (dst1 == src2 or src1 == dst2):
            if dst1 == src2:
                score += 0.4
                reasons.append({"edge_type": "SHARED_IP_PIVOT", "reason": f"Pivot IP {dst1}"})
            elif src1 == dst2:
                score += 0.4
                reasons.append({"edge_type": "SHARED_IP_PIVOT", "reason": f"Pivot IP {src1}"})
                
        elif src1 and src1 == src2:
            score += self.weights["SAME_SOURCE_IP"]
            reasons.append({"edge_type": "SAME_SOURCE_IP", "reason": "Events share source IP only (WEAK)"})
            
        elif dst1 and dst1 == dst2:
            score += self.weights["SAME_DESTINATION_IP"]
            reasons.append({"edge_type": "SAME_DESTINATION_IP", "reason": "Events share destination IP only (WEAK)"})
            
        # Detection Agreement
        if e1.get("detection_source") == e2.get("detection_source") and e1.get("detection_source") not in ["NONE", None]:
            score += self.weights["DETECTION_AGREEMENT"]
            reasons.append({"edge_type": "DETECTION_AGREEMENT", "reason": "Events share same detection mechanism"})
            
        # Temporal
        if e1.get("timestamp_source") == "DEMO_REPLAY" and e2.get("timestamp_source") == "DEMO_REPLAY":
            t1, t2 = e1.get("timestamp"), e2.get("timestamp")
            if t1 is not None and t2 is not None:
                if abs(t1 - t2) <= self.temporal_window:
                    score += self.weights["TEMPORAL"]
                    reasons.append({"edge_type": "TEMPORAL", "reason": f"Events within {self.temporal_window}s window"})
                    
        return score, reasons

    def get_candidate_incidents(self, G: nx.Graph) -> List[Dict[str, Any]]:
        incidents = []
        # Filter out nodes with NO incident edges (degree 0)
        # Single nodes are just isolated contextual events, not multi-stage candidate incidents
        valid_nodes = [n for n, d in G.degree() if d > 0]
        subgraph_G = G.subgraph(valid_nodes)
        
        components = list(nx.connected_components(subgraph_G))
        
        for idx, comp in enumerate(components):
            subgraph = G.subgraph(comp)
            nodes_data = [data for _, data in subgraph.nodes(data=True)]
            
            src_ips = set(n.get("source_ip") for n in nodes_data if n.get("source_ip"))
            dst_ips = set(n.get("destination_ip") for n in nodes_data if n.get("destination_ip"))
            
            is_demo = all(n.get("timestamp_source") == "DEMO_REPLAY" for n in nodes_data)
            if is_demo:
                nodes_data.sort(key=lambda x: x.get("timestamp", 0))
                
            incident = {
                "incident_id": f"INC_{idx+1}",
                "event_count": len(comp),
                "edge_count": subgraph.number_of_edges(),
                "source_ips": list(src_ips),
                "destination_ips": list(dst_ips),
                "ordered_events": [n.get("event_id") for n in nodes_data] if is_demo else []
            }
            incidents.append(incident)
            
        return incidents
