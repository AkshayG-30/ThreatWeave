# ThreatWeave Correlation Data Model

## Purpose
The Correlation Engine is responsible for grouping individual suspicious events into broader candidate incidents (attack chains). It avoids false-positive clustering by enforcing a strict Evidence Hierarchy and scoring threshold.

## Data Sources
- **Integrated Events**: Sourced from the detector layer containing both Supervised (XGBoost) and Anomaly (Isolation Forest) scores.
- **Entities**: IP addresses (Source/Destination) preserved specifically for this phase.
- **Timestamps**: Due to constraints in the `NF-UNSW-NB15-v2` dataset (no timestamps), all temporal fields for the real dataset are strictly `NULL`.

## Candidate Generation Strategy
To avoid O(N²) memory explosions when processing thousands of events that happen to share a common entity (like a single Source IP in a lab environment), the engine uses **Bounded Candidate Generation**. Events are indexed by composite, high-confidence attributes (e.g. `(Source IP, Destination IP)`) or sorted temporally if timestamps exist. Pairwise correlation is only performed *within* these bounded groups.

## Evidence Hierarchy
Every potential relationship is scored according to a weighted evidence hierarchy:
- `SAME_SRC_AND_DST`: 0.6 (MEDIUM)
- `SHARED_IP_BIDIR`: 0.5 (MEDIUM)
- `TEMPORAL`: 0.6 (STRONG when combined with entity data)
- `SAME_SRC_DST_PORT`: 0.3 (Bonus modifier)
- `SAME_SOURCE_IP`: 0.2 (WEAK contextual indicator)
- `SAME_DESTINATION_IP`: 0.2 (WEAK contextual indicator)
- `DETECTION_AGREEMENT`: 0.2 (Bonus modifier)

## Correlation Threshold
- **Threshold**: `>= 1.0`
- Relationships below this threshold do NOT form an edge. This prevents weak indicators (e.g. sharing only a Source IP = 0.2) from falsely linking unrelated events into a giant incident graph.
- When an edge meets the threshold, its evidence strength is explicitly recorded as WEAK, MEDIUM, or STRONG.

## Contextual Clusters vs. Candidate Incidents
- **Contextual Clusters**: Events that share weak attributes (e.g., `SAME_SOURCE_IP`). These are not grouped into a candidate incident. 
- **Candidate Incidents**: Connected components in the graph where nodes have at least one edge meeting the `1.0` threshold. Single isolated events (even if highly anomalous) are not considered multi-stage candidate incidents.

## Synthetic Demo Replay
Because the real dataset lacks timestamps, the temporal rules (`TEMPORAL: 0.6` within 30 seconds) can only be demonstrated on synthetic replays.
- **Flag**: Demo events are strictly isolated using `timestamp_source = "DEMO_REPLAY"`.
- **Integrity**: Real data remains unaffected by temporal sliding-window logic.
