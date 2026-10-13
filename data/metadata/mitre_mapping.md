# MITRE ATT&CK Mapping Strategy

## Objective
Provide transparent, deterministic rules for mapping ThreatWeave candidate incidents to MITRE ATT&CK techniques based strictly on verifiable network evidence. **We explicitly forbid LLM-based hallucination of techniques.**

## Current Mappings (Phase 4 MVP)

### T1046: Network Service Scanning
- **Tactic**: Discovery
- **Input Evidence Rule**: Multiple events containing `RECON` or `SCAN` indicators in the event ID. (In a full implementation, this would be `TCP SYN` sweeps to different destination ports on the same IP or horizontal sweeps across IPs within a temporal window).
- **Limitations**: Dependent on Phase 2 labeling schema for demo purposes.

### T1210: Exploitation of Remote Services
- **Tactic**: Lateral Movement
- **Input Evidence Rule**: Event containing `EXPLOIT` indicator combined with strong supervised detection confidence.
- **Limitations**: NF-UNSW-NB15-v2 lacks deep payload evidence, so exact CVE or application exploited cannot be determined.

### T1071: Application Layer Protocol
- **Tactic**: Command and Control (C2)
- **Input Evidence Rule**: Anomalous events following exploitation labeled as `C2`. Represents outbound beaconing or reverse shell behavior.
- **Limitations**: Dataset does not provide TLS/HTTP headers for precise C2 framework identification.

### T1041: Exfiltration Over C2 Channel
- **Tactic**: Exfiltration
- **Input Evidence Rule**: Data transfer events (`EXFIL`) occurring after established C2 channels.
- **Limitations**: Byte count analysis (large outbound bytes) is not fully implemented in the mapping yet.

## Missing Evidence Handling
If the available event context does not trigger any of the rules above, the `MitreMapper` will return a single placeholder mapping:
- `technique_id = null`
- `evidence = "Insufficient evidence for specific ATT&CK technique mapping."`
