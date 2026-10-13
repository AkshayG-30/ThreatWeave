export interface EvidenceItem {
    evidence_id: string;
    type: string;
    description: string;
    source_event_ids: string[];
    source_edge_ids: string[] | null;
    strength: string;
}

export interface MitreMapping {
    technique_id: string | null;
    technique_name: string | null;
    tactic: string | null;
    evidence: string;
    confidence: string;
    source_event_ids: string[];
}

export interface IncidentEvent {
    event_id: string;
    source_ip: string;
    destination_ip: string;
    source_port: number | null;
    destination_port: number | null;
    protocol: string;
    supervised_score: number;
    anomaly_score: number;
    detection_source: string;
    timestamp: number | null;
    timestamp_source: string | null;
}

export interface IncidentEdge {
    source: string;
    target: string;
    weight: number;
    reasons: any[];
    evidence_strength: string;
}

export interface StructuredIncident {
    incident_id: string;
    event_count: number;
    events: IncidentEvent[];
    edges: IncidentEdge[];
    correlation_score: number;
    detection_summary: Record<string, any>;
    mitre_mappings: MitreMapping[];
    evidence_items: EvidenceItem[];
    confidence: string;
    timestamp_source: string | null;
    limitations: string[];
}
