# SAGA Dataset Audit

## Availability
- **Local Availability**: NOT AVAILABLE LOCALLY.
- **Official Source**: Academic / Open-source repositories (e.g., GitHub).
- **Format**: Synthetic audit logs combining benign and APT activities.
- **Approximate Size**: Configurable/Generative (can be massively scaled).
- **Practical Obtainability**: Not immediately obtainable in the current frozen environment without substantial download, setup of the generation framework, and validation.

## Schema Characteristics
- **Files**: JSON/CSV formatted audit logs.
- **Timestamps**: Natively supported through sequential audit log generation.
- **Event Identifiers**: Unique system/process/network events.
- **Entities**: Primarily host-level (users, files, processes).
- **Campaign/Attack Ground Truth**: Modeled against known APT campaigns (e.g., APT28, FIN7, CobaltGroup) and fully mapped to MITRE ATT&CK TTPs.
- **Sequence/Order**: High-fidelity temporal sequences representing the lifecycle of an APT.

## ThreatWeave Compatibility
SAGA (Synthetic Audit Log Generation for APT Campaigns) provides high-quality sequential ground truth specifically constructed around MITRE ATT&CK. 

Because it primarily generates audit/host logs rather than raw network flow statistics, it is **incompatible** with our frozen 41-feature XGBoost detector (which operates strictly on NF-UNSW network flows). 

However, SAGA is highly suitable as an **ATTACK-CHAIN VALIDATION DATASET**. By parsing SAGA logs directly into ThreatWeave's `StructuredIncident` format, we can natively evaluate ThreatWeave's deterministic correlation rules, temporal bounds, and Graph/NetworkX reconstruction against complex, composite APT campaigns. 

Crucially, SAGA contains genuine chronological ordering information, fully supporting future GRU temporal experiments and deterministic temporal correlation logic.

## Verdict
READY FOR REAL VALIDATION (Requires Adapter for parsing audit logs into ThreatWeave correlation schemas).
