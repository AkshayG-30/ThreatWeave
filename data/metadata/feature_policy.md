# Feature Policy for NF-UNSW-NB15-v2

| FEATURE | TYPE | KEEP/DROP (For ML) | REASON | USED FOR |
|---|---|---|---|---|
| `Label` | Target | DROP | This is the binary ground truth target. It causes direct data leakage if included in features. | Supervised binary classification target. |
| `Attack` | Target | DROP | Multiclass ground truth target. Causes direct data leakage. | Extracted for evaluation and stratification. |
| `IPV4_SRC_ADDR` | Identifier | DROP | IP addresses are network-specific identifiers. Training on them leads to the model memorizing specific IPs rather than learning attack behaviors. | Canonical Mapping (`source_ip`). |
| `IPV4_DST_ADDR` | Identifier | DROP | Same reasoning as Source IP. Avoids overfitting to the specific network topology of the lab. | Canonical Mapping (`destination_ip`). |
| `L4_SRC_PORT` | Feature | KEEP | Source ports can indicate ephemeral port behavior or specific tools. | ML Feature & Canonical Mapping (`source_port`). |
| `L4_DST_PORT` | Feature | KEEP | Destination ports indicate targeted services (e.g., 80 for HTTP). | ML Feature & Canonical Mapping (`destination_port`). |
| `PROTOCOL` | Feature | KEEP | Network protocol (TCP/UDP/ICMP) is a fundamental feature of attacks. | ML Feature & Canonical Mapping (`protocol`). |
| *All other numeric features* | Numeric | KEEP | Traffic flow statistics (bytes, packets, flags, TTLs) describe the behavioral patterns of the connections. | ML Features. |

**Note on Missing Fields**: The dataset lacks `timestamp`, `host`, `user`, and `process`. These will be strictly mapped as `None`/`NULL` in the canonical events to avoid fabrication.
