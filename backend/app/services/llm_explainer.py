import os
import json
from typing import Dict, Any, Optional
from groq import Groq
from app.schemas.incident import StructuredIncident, LLMExplanation

class LLMExplainer:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def explain(self, incident: StructuredIncident, scenario_id: Optional[str] = None) -> LLMExplanation:
        """
        Explains an incident using Groq API. Falls back to deterministic logic if unavailable or fails.
        """
        resolved_scenario_id = scenario_id or "TC-10"
        if not self.client:
            return self._deterministic_fallback(incident, scenario_id=resolved_scenario_id)
            
        try:
            # Construct a grounded prompt
            prompt = self._build_prompt(incident)
            model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an incident explanation assistant. You may ONLY use the structured evidence provided. Do not infer or invent events, timestamps, IP addresses, users, processes, techniques, or attack stages that are not explicitly present. Output valid JSON adhering to the provided schema."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model_name,
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            content = chat_completion.choices[0].message.content
            parsed = json.loads(content)
            
            # Map back to Pydantic to ensure schema compliance
            return LLMExplanation(
                summary=str(parsed.get("summary", "")),
                attack_chain=str(parsed.get("attack_chain", "")),
                evidence=str(parsed.get("evidence", "")),
                mitre_techniques=str(parsed.get("mitre_techniques", "")),
                confidence=str(parsed.get("confidence", "HIGH")),
                limitations=str(parsed.get("limitations", "")),
                investigation_recommendations=str(parsed.get("investigation_recommendations", "")),
                scenario_id=resolved_scenario_id,
                incident_id=incident.incident_id,
                provider="groq",
                fallback_used=False,
                model_name=model_name
            )
        except Exception as e:
            print(f"LLM generation failed: {e}. Falling back to deterministic explanation.")
            return self._deterministic_fallback(incident, scenario_id=resolved_scenario_id)

    def _build_prompt(self, incident: StructuredIncident) -> str:
        # We only pass explicit evidence to avoid hallucination
        events_str = json.dumps([e.model_dump() for e in incident.events], indent=2)
        mitre_str = json.dumps([m.model_dump() for m in incident.mitre_mappings], indent=2)
        evidence_str = json.dumps([e.model_dump() for e in incident.evidence_items], indent=2)
        
        return f"""
        STRUCTURED EVIDENCE:
        Events: {events_str}
        MITRE Mappings: {mitre_str}
        Evidence Items: {evidence_str}
        Limitations: {incident.limitations}
        
        TASK:
        Generate a JSON object with the following keys:
        - summary: A short summary of the incident based only on the evidence.
        - attack_chain: An explanation of the sequence of events.
        - evidence: The supporting evidence for this chain.
        - mitre_techniques: A list of techniques identified in the MITRE mappings block.
        - confidence: The overall confidence (e.g. HIGH/MEDIUM/LOW).
        - limitations: Any limitations (e.g., if there are no timestamps or missing host data).
        - investigation_recommendations: What an analyst should look at next.
        """

    def _deterministic_fallback(self, incident: StructuredIncident, scenario_id: Optional[str] = None) -> LLMExplanation:
        """
        A deterministic explanation generated purely via rules if LLM is unavailable.
        """
        mitre_names = [m.technique_name for m in incident.mitre_mappings if m.technique_name]
        mitre_str = ", ".join(mitre_names) if mitre_names else "Insufficient evidence for specific ATT&CK technique mapping."
        event_ids = [e.event_id for e in incident.events]
        attack_chain_str = " -> ".join(event_ids) if event_ids else "No correlated events in incident."
        
        return LLMExplanation(
            summary=f"Candidate incident {incident.incident_id} contains {incident.event_count} correlated events. Events were linked using shared network entities and temporal proximity.",
            attack_chain=attack_chain_str,
            evidence=f"Structured evidence items: {len(incident.evidence_items)} items detected.",
            mitre_techniques=mitre_str,
            confidence=incident.confidence or "MEDIUM",
            limitations="Deterministic fallback explanation due to unavailable or failed LLM inference. Reconstructed strictly from deterministic correlation and detection graph.",
            investigation_recommendations="Review raw packet capture or underlying logs for the identified source and destination IP addresses.",
            scenario_id=scenario_id or "TC-10",
            incident_id=incident.incident_id,
            provider="deterministic",
            fallback_used=True,
            model_name=None
        )
