export interface LLMExplanation {
  summary: string;
  attack_chain: string;
  evidence: string;
  mitre_techniques: string;
  confidence: string;
  limitations: string;
  investigation_recommendations: string;
  scenario_id?: string;
  incident_id?: string;
  provider?: 'groq' | 'deterministic';
  fallback_used?: boolean;
  model_name?: string;
}
