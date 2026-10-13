export interface LLMExplanation {
    summary: string;
    attack_chain: string;
    evidence: string;
    mitre_techniques: string;
    confidence: string;
    limitations: string;
    investigation_recommendations: string;
}
