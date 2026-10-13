export interface EvidenceItem {
  evidence_id: string;
  type: string;
  description: string;
  source_event_ids: string[];
  source_edge_ids?: string[] | null;
  strength: 'HIGH' | 'MEDIUM' | 'LOW' | string;
}

export interface MitreMapping {
  technique_id: string | null;
  technique_name: string | null;
  tactic: string | null;
  evidence: string;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW' | string;
  source_event_ids: string[];
}

export interface IncidentEvent {
  event_id: string;
  source_ip: string;
  destination_ip: string;
  source_port?: number | null;
  destination_port?: number | null;
  protocol: string;
  supervised_score: number;
  anomaly_score: number;
  detection_source: 'SUPERVISED' | 'ANOMALY' | 'BOTH' | 'NONE' | string;
  timestamp?: number | null;
  timestamp_source?: string | null;
}

export interface StructuredIncident {
  incident_id: string;
  event_count: number;
  events: IncidentEvent[];
  edges: Array<{
    source: string;
    target: string;
    relationship?: string;
    evidence_type?: string;
    [key: string]: unknown;
  }>;
  correlation_score: number;
  detection_summary: {
    supervised_detections?: number;
    anomaly_detections?: number;
    both_detections?: number;
    [key: string]: unknown;
  };
  mitre_mappings: MitreMapping[];
  evidence_items: EvidenceItem[];
  confidence: 'HIGH' | 'MEDIUM' | 'LOW' | string;
  timestamp_source?: string | null;
  limitations: string[];
  scenario_id?: string;
  execution_mode?: 'LIVE_INFERENCE' | 'CONTROLLED_REPLAY' | 'RECORDED_EVALUATION';
  source_dataset?: string;
}
