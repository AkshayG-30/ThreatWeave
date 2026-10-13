# Unraveled Dataset Audit

## Availability
- **Local Availability**: NOT AVAILABLE LOCALLY.
- **Official Source**: Academic repositories / specific researcher portals.
- **Format**: Multi-modal (network flows + host logs, authentication, process execution).
- **Approximate Size**: Varies by campaign (typically gigabytes to terabytes).
- **Practical Obtainability**: Not immediately obtainable in the current frozen environment without substantial download, validation, and parsing overhead.

## Schema Characteristics
- **Files**: Multi-file relational schemas (PCAP/flow logs + Sysmon/auditd logs).
- **Timestamps**: Explicit, high-fidelity chronological timestamps natively supported.
- **Event Identifiers**: Granular connection to specific processes/users/connections.
- **Entities**: Source/destination IPs, hosts, user accounts, and process IDs.
- **Campaign/Attack Ground Truth**: Fully labeled by APT stage (reconnaissance, lateral movement, exfiltration) and aligned with specific MITRE ATT&CK techniques.
- **Sequence/Order**: Strong sequential ground truth inherent to the dataset design.

## ThreatWeave Compatibility
Unraveled provides exactly the type of ground truth required for **multi-stage attack-chain validation** and **graph evaluation**. 

It contains explicit chronological timestamps, allowing for genuine temporal sequence evaluation. Furthermore, the presence of host, user, and process entities provides the exact structured bridges needed for advanced entity-relationship graph correlation. 

However, Unraveled provides significantly richer data than our current 41-feature network-flow pipeline. Therefore, it would enter the ThreatWeave pipeline **NOT** as a drop-in replacement for the XGBoost detection stage, but rather as an **ATTACK-CHAIN VALIDATION DATASET** injected at the correlation and graph reconstruction layers, allowing us to evaluate ThreatWeave's ability to chain discrete events into an APT narrative.

## Verdict
READY FOR REAL VALIDATION (Requires Adapter for injection into the correlation pipeline).
