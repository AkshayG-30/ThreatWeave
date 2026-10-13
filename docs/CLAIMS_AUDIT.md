# ThreatWeave Claims Audit

## SUPPORTED CLAIMS
- End-to-end layered cybersecurity detection and reconstruction pipeline
- Supervised known-attack detection
- Random Forest baseline
- XGBoost supervised detection
- LightGBM benchmark
- Isolation Forest anomaly detection
- Autoencoder anomaly detection
- Bounded evidence-based correlation
- Entity relationship correlation
- Graph-based attack reconstruction
- Deterministic MITRE ATT&CK mapping
- Evidence-grounded LLM explanation
- Unseen attack-family evaluation
- Real NF-UNSW → NF-CSE-CIC-IDS2018 cross-dataset evaluation
- Controlled multi-stage attack reconstruction
- Formal ablation study
- Anomaly-method comparison

## CLAIMS WE MUST NOT MAKE
- **Zero-day detection**: Our experiments evaluated hold-out families from an existing taxonomy, not genuine unknown zero-days in the wild.
- **Attacks detected in the wild**: We utilized curated academic benchmarks (NF-UNSW-NB15-v2), not live production tap data.
- **State-of-the-art performance**: This is a hackathon MVP designed for conceptual architecture scaling, not a competitively tuned hyperparameter benchmark against academic SotA.
- **Real Unraveled validation**: Not integrated; we utilized controlled synthetic topological chains.
- **Real SAGA validation**: Not integrated due to scope.
- **Successful NF-ToN-IoT evaluation**: The audit proved the dataset was incompatible with our frozen feature structure due to 31 missing features.
- **GNN-based reasoning**: The controlled graph (9 nodes) is vastly insufficient for generalizable GNN training, risking massive overfitting; currently deferred to future research.
- **GRU-based temporal modelling**: NF-UNSW lacks strict chronological timestamps needed to form sequential data for Recurrent Neural Networks.
- **Complete real-world APT campaign reconstruction**: Our correlation testing utilized a 9-event synthetic baseline sequence, which does not rival the complexities of a true advanced persistent threat sequence.
- **LLM improves detection accuracy**: The LLM operates purely post-detection as a contextual explainer. It possesses zero detection capabilities.
- **Graph improves classification accuracy**: The graph organizes relations and dependencies; it does not compute base binary classification metrics.
- **Correlation quantitatively reduces FPR**: While it functionally orphans noise nodes (reducing the volume of alert fatigue), mathematical classification FPR relies on the base detection layers (Stage A/B).
- **Autoencoder universally outperforms Isolation Forest**: Our experiment observed Autoencoder producing lower FPR and higher F1, but Isolation Forest marginally retained higher recall on this specific split.
- **Every component from the original planned architecture was implemented**: Due to the severe 48-hour time constraint, several systems (GNN, GRU, PostgreSQL) were analytically evaluated as infeasible and consciously deferred to future research.
