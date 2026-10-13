# ThreatWeave Architecture MVP

## Components
1. **Frontend**: React application for visualizations (Dashboard).
2. **Backend**: FastAPI for handling REST API requests and invoking models.
3. **ML Pipeline**: 
    - Loads Network Flow datasets.
    - Standardizes schema to `CanonicalEvent`.
    - Routes to `SupervisedModel` and `AnomalyDetector`.
4. **Correlation Engine (Future)**: Will use NetworkX for campaign graph clustering.
5. **LLM Explainer (Future)**: Will query Groq API with correlated events for incident summary.

## Data Flow
`Raw Dataset -> DataPipeline (Preprocess) -> CanonicalEvent -> ML Models -> DetectorOutput -> Correlation Engine -> UI`
