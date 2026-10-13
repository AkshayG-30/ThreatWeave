# Campaign Dataset Compatibility Report

## Overview
This report evaluates the compatibility of the Unraveled and SAGA datasets with the existing ThreatWeave pipeline.

### CURRENT PIPELINE
Data → Preprocessing → Detection (XGBoost/Isolation Forest) → Correlation → Graph Reconstruction → MITRE ATT&CK → Explanation

## Injection Point
Neither Unraveled nor SAGA matches the exact 41-feature network flow schema of NF-UNSW-NB15-v2. Therefore, neither dataset is appropriate for evaluating the **Detection** layer directly without destructive imputation or complete retraining.

Instead, both datasets perfectly match the requirements of an **ATTACK-CHAIN VALIDATION DATASET**. 

If implemented, these datasets would bypass the XGBoost detection layer entirely. Their ground-truth labeled events would be fed directly into the **Correlation** and **Graph Reconstruction** layers.

## Temporal Validation (GRU Feasibility)
**Both datasets provide explicit, genuine chronological timestamps and sequential ground truth.** 
Unlike NF-UNSW (which lacks strict chronology), Unraveled and SAGA would legitimately support genuine temporal correlation and provide the thousands of ordered sequences necessary to train a future GRU-based temporal model.

## Graph Validation (NetworkX / GNN Feasibility)
**Both datasets contain rich entity interactions (hosts, users, processes, IPs).**
They provide the necessary ground truth to mathematically evaluate our deterministic NetworkX reconstruction (e.g., calculating edge-matching precision/recall and component completeness). Furthermore, their scale and complexity provide exactly the topological diversity required to support meaningful training and evaluation of a future Graph Neural Network (GNN).

## Conclusion
Both datasets represent the scientifically correct path forward for validating ThreatWeave's higher-order logic (Phases 3-4), offering the multi-stage, chronological APT ground truth that NF-UNSW fundamentally lacks.
