# Dataset Plan for ThreatWeave MVP

## Candidate Dataset for MVP
**NF-UNSW-NB15-v2** (Network Flow based dataset)

- **Purpose**: Initial supervised model training and anomaly detection baseline testing.
- **Source**: University of New South Wales (UNSW) cybersecurity datasets / NetFlow v2 formats.
- **Format**: CSV (NetFlow features)
- **Approximate Size**: Few hundreds of MBs (manageable for a one-day MVP without distributed processing).
- **Relevant Labels**: Benign vs. Malicious (binary), plus attack families (e.g., Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode, Worms).
- **Intended ThreatWeave Component**: Supervised ML Baseline (Random Forest / XGBoost) & Anomaly Detection (Isolation Forest).
- **MVP Priority**: HIGH - Ideal balance of standard netflow features (easy to parse) and well-documented attack classes.

## Future / Secondary Datasets (Do Not Download Yet)
1. **NF-CSE-CIC-IDS2018-v2**: Will test model generalization.
2. **NF-ToN-IoT-v2**: Will test IoT attack detection.
3. **Unraveled & SAGA**: Attack chain / Audit logs for the correlation engine.
