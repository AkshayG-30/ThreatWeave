# Phase 4 MITRE Mapping and Explanation

## Reconstructed Chain
1. Reconnaissance: EV_01_RECON and EV_02_RECON show TCP connections from 10.0.0.5 to web servers (port 80). 2. Scanning: EV_03_SCAN adds a TCP connection to port 445, indicating network service scanning. 3. Exploitation: EV_04_EXPLOIT (high supervised score) indicates exploitation of the remote SMB service on 192.168.1.12. 4. Command & Control: EV_05_C2 and EV_06_C2 are anomalous outbound TCP flows from the compromised host to external IP 185.15.2.1. 5. Exfiltration: EV_07_EXFIL (detected by both models) shows data transfer over the same C2 channel. 6. Lateral Movement: EV_08_LATERAL (high supervised score) shows a new SMB connection from the compromised host to another internal host (192.168.1.15).

## Evidence Grounding
[{'evidence_id': 'EVID_01', 'type': 'CORRELATION', 'description': 'Events share a strong multi‑signal relationship (temporal proximity and shared source/destination IPs).', 'strength': 'STRONG'}, {'evidence_id': 'EVID_02', 'type': 'DETECTION', 'description': 'Events flagged by both Supervised and Anomaly detectors.', 'source_event_ids': ['EV_03_SCAN', 'EV_07_EXFIL'], 'strength': 'HIGH'}]

## MITRE Techniques
[{'technique_id': 'T1046', 'technique_name': 'Network Service Scanning', 'tactic': 'Discovery', 'confidence': 'HIGH', 'source_event_ids': ['EV_01_RECON', 'EV_02_RECON', 'EV_03_SCAN']}, {'technique_id': 'T1210', 'technique_name': 'Exploitation of Remote Services', 'tactic': 'Lateral Movement', 'confidence': 'MEDIUM', 'source_event_ids': ['EV_04_EXPLOIT']}, {'technique_id': 'T1071', 'technique_name': 'Application Layer Protocol', 'tactic': 'Command and Control', 'confidence': 'HIGH', 'source_event_ids': ['EV_05_C2', 'EV_06_C2']}, {'technique_id': 'T1041', 'technique_name': 'Exfiltration Over C2 Channel', 'tactic': 'Exfiltration', 'confidence': 'MEDIUM', 'source_event_ids': ['EV_07_EXFIL']}]

## Confidence
HIGH

## Limitations
['Timestamps are synthetic replay only', 'No deep payload parsing']

## Raw Output
```json
{
    "summary": "A hostile actor from IP 10.0.0.5 performed reconnaissance and service scanning of internal hosts, exploited SMB on 192.168.1.12, established command‑and‑control communications to external IP 185.15.2.1, exfiltrated data over that channel, and later attempted lateral movement to another internal host.",
    "attack_chain": "1. Reconnaissance: EV_01_RECON and EV_02_RECON show TCP connections from 10.0.0.5 to web servers (port 80). 2. Scanning: EV_03_SCAN adds a TCP connection to port 445, indicating network service scanning. 3. Exploitation: EV_04_EXPLOIT (high supervised score) indicates exploitation of the remote SMB service on 192.168.1.12. 4. Command & Control: EV_05_C2 and EV_06_C2 are anomalous outbound TCP flows from the compromised host to external IP 185.15.2.1. 5. Exfiltration: EV_07_EXFIL (detected by both models) shows data transfer over the same C2 channel. 6. Lateral Movement: EV_08_LATERAL (high supervised score) shows a new SMB connection from the compromised host to another internal host (192.168.1.15).",
    "evidence": "[{'evidence_id': 'EVID_01', 'type': 'CORRELATION', 'description': 'Events share a strong multi‑signal relationship (temporal proximity and shared source/destination IPs).', 'strength': 'STRONG'}, {'evidence_id': 'EVID_02', 'type': 'DETECTION', 'description': 'Events flagged by both Supervised and Anomaly detectors.', 'source_event_ids': ['EV_03_SCAN', 'EV_07_EXFIL'], 'strength': 'HIGH'}]",
    "mitre_techniques": "[{'technique_id': 'T1046', 'technique_name': 'Network Service Scanning', 'tactic': 'Discovery', 'confidence': 'HIGH', 'source_event_ids': ['EV_01_RECON', 'EV_02_RECON', 'EV_03_SCAN']}, {'technique_id': 'T1210', 'technique_name': 'Exploitation of Remote Services', 'tactic': 'Lateral Movement', 'confidence': 'MEDIUM', 'source_event_ids': ['EV_04_EXPLOIT']}, {'technique_id': 'T1071', 'technique_name': 'Application Layer Protocol', 'tactic': 'Command and Control', 'confidence': 'HIGH', 'source_event_ids': ['EV_05_C2', 'EV_06_C2']}, {'technique_id': 'T1041', 'technique_name': 'Exfiltration Over C2 Channel', 'tactic': 'Exfiltration', 'confidence': 'MEDIUM', 'source_event_ids': ['EV_07_EXFIL']}]",
    "confidence": "HIGH",
    "limitations": "['Timestamps are synthetic replay only', 'No deep payload parsing']",
    "investigation_recommendations": "['Correlate these flows with host‑level logs on 192.168.1.12 and 192.168.1.15 to confirm compromise.', 'Inspect SMB traffic for exploit payloads and identify the vulnerability used.', 'Perform deep packet inspection on the C2 connections to 185.15.2.1 to determine command sets and data exfiltrated.', 'Check for persistence mechanisms on the compromised hosts.', 'Monitor for additional lateral movement attempts to other internal assets.', 'Enrich external IP 185.15.2.1 with threat intelligence to assess its reputation.']"
}
```
