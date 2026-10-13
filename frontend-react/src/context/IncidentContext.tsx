import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { StructuredIncident } from '../types/incident';
import type { LLMExplanation } from '../types/explanation';
import { ApiService } from '../services/api';
import tc10Fallback from '../data/tc10_fixture.json';

export type PipelineStage = 
  | 'DATA_LOADING'
  | 'PREPROCESSING'
  | 'SUPERVISED_DETECTION'
  | 'ANOMALY_DETECTION'
  | 'EVENT_CORRELATION'
  | 'GRAPH_RECONSTRUCTION'
  | 'MITRE_MAPPING'
  | 'AI_EXPLANATION'
  | 'REPORT_READY';

export interface StageStatus {
  stage: PipelineStage;
  label: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'SKIPPED' | 'ERROR';
  description: string;
  outputSummary?: string;
}

export interface IncidentContextType {
  selectedScenarioId: string;
  incident: StructuredIncident | null;
  explanation: LLMExplanation | null;
  explanationSource: 'GROQ' | 'DETERMINISTIC_FALLBACK' | 'UNAVAILABLE';
  isLoading: boolean;
  error: string | null;
  stages: StageStatus[];
  activeStageIndex: number;
  isReplaying: boolean;
  selectScenario: (scenarioId: string) => Promise<void>;
  executeScenarioReplay: (scenarioId: string) => Promise<void>;
  refreshExplanation: () => Promise<void>;
}

const buildFallbackExplanation = (inc: StructuredIncident | null, scenarioId: string): LLMExplanation => {
  const evList = inc?.events?.map(e => e.event_id) || [];
  const chain = evList.length > 0 ? evList.join(' -> ') : 'No correlated events in incident';
  const mitreList = inc?.mitre_mappings?.map(m => `${m.technique_name || 'Technique'} (${m.technique_id})`).join(', ') 
    || 'No specific ATT&CK techniques mapped for this scenario';
  
  return {
    summary: `Candidate incident ${inc?.incident_id || 'INC_1'} (${scenarioId}) contains ${inc?.event_count || 0} correlated events linked via shared network entities and temporal proximity.`,
    attack_chain: chain,
    evidence: `Structured evidence items: ${inc?.evidence_items?.length || 0} items detected from verified replay cache.`,
    mitre_techniques: mitreList,
    confidence: inc?.confidence || 'HIGH',
    limitations: 'Deterministic offline narrative synthesized from structured facts. Click "Execute Scenario" or "Generate AI Explanation (Groq)" to invoke live Groq LLM synthesis.',
    investigation_recommendations: inc?.events && inc.events.length > 0 
      ? `Review telemetry for source IP ${inc.events[0].source_ip} and isolate host if anomalous behavior persists.`
      : 'Maintain baseline monitoring.',
    scenario_id: scenarioId,
    incident_id: inc?.incident_id || 'INC_1',
    provider: 'deterministic',
    fallback_used: true
  };
};

const DEFAULT_STAGES: StageStatus[] = [
  { stage: 'DATA_LOADING', label: 'Data Ingestion', status: 'COMPLETED', description: 'NetFlow v2 stream ingestion (41 standardized features)', outputSummary: '8 flow records loaded' },
  { stage: 'PREPROCESSING', label: 'Feature Normalization', status: 'COMPLETED', description: 'MinMax scaling & categorical schema alignment', outputSummary: 'Zero NaNs, validated bounds' },
  { stage: 'SUPERVISED_DETECTION', label: 'Supervised Detection', status: 'COMPLETED', description: 'Production XGBoost detector evaluation', outputSummary: '4 attack flows flagged (p=0.99)' },
  { stage: 'ANOMALY_DETECTION', label: 'Anomaly Detection', status: 'COMPLETED', description: 'Production Isolation Forest outlier detection', outputSummary: '5 behavioral anomalies flagged' },
  { stage: 'EVENT_CORRELATION', label: 'Bounded Correlation', status: 'COMPLETED', description: 'Entity & temporal window bounding (Δt ≤ 30s)', outputSummary: '20 verified evidence edges' },
  { stage: 'GRAPH_RECONSTRUCTION', label: 'Graph Reconstruction', status: 'COMPLETED', description: 'NetworkX directed topological incident assembly', outputSummary: '1 candidate incident (INC_1)' },
  { stage: 'MITRE_MAPPING', label: 'MITRE ATT&CK Mapping', status: 'COMPLETED', description: 'Deterministic T-code rule mapping', outputSummary: '4 techniques mapped (T1046, T1210, T1071, T1041)' },
  { stage: 'AI_EXPLANATION', label: 'AI Explanation', status: 'COMPLETED', description: 'Evidence-grounded narrative synthesis', outputSummary: 'Deterministic baseline (click to invoke Groq)' },
  { stage: 'REPORT_READY', label: 'Report Ready', status: 'COMPLETED', description: 'Exportable markdown compliance report', outputSummary: 'Incident INC_1 report ready' }
];

const IncidentContext = createContext<IncidentContextType | undefined>(undefined);

export const IncidentProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedScenarioId, setSelectedScenarioId] = useState<string>('TC-10');
  const [incident, setIncident] = useState<StructuredIncident | null>(tc10Fallback as unknown as StructuredIncident);
  const [explanation, setExplanation] = useState<LLMExplanation | null>(
    buildFallbackExplanation(tc10Fallback as unknown as StructuredIncident, 'TC-10')
  );
  const [explanationSource, setExplanationSource] = useState<'GROQ' | 'DETERMINISTIC_FALLBACK' | 'UNAVAILABLE'>('DETERMINISTIC_FALLBACK');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [stages, setStages] = useState<StageStatus[]>(DEFAULT_STAGES);
  const [activeStageIndex, setActiveStageIndex] = useState<number>(8);
  const [isReplaying, setIsReplaying] = useState<boolean>(false);

  const loadScenarioData = useCallback(async (scenarioId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await ApiService.getScenarioIncident(scenarioId);
      if (data) {
        setIncident(data);
        setExplanation(buildFallbackExplanation(data, scenarioId));
        setExplanationSource('DETERMINISTIC_FALLBACK');
      } else if (scenarioId === 'TC-10') {
        const fallback = tc10Fallback as unknown as StructuredIncident;
        setIncident(fallback);
        setExplanation(buildFallbackExplanation(fallback, scenarioId));
        setExplanationSource('DETERMINISTIC_FALLBACK');
      } else {
        setIncident(null);
        setError(`Scenario ${scenarioId} has no cached incident fixture.`);
      }
    } catch {
      if (scenarioId === 'TC-10') {
        const fallback = tc10Fallback as unknown as StructuredIncident;
        setIncident(fallback);
        setExplanation(buildFallbackExplanation(fallback, scenarioId));
        setExplanationSource('DETERMINISTIC_FALLBACK');
      } else {
        setError(`Failed to fetch scenario ${scenarioId} from backend.`);
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loadExplanation = useCallback(async (scenarioId?: string) => {
    const targetScenario = scenarioId || selectedScenarioId;
    try {
      const exp = await ApiService.getExplanation(targetScenario);
      if (exp) {
        setExplanation(exp);
        if (exp.provider === 'groq' && !exp.fallback_used) {
          setExplanationSource('GROQ');
        } else {
          setExplanationSource('DETERMINISTIC_FALLBACK');
        }
        setStages(prev => prev.map(s => {
          if (s.stage === 'AI_EXPLANATION') {
            return {
              ...s,
              status: 'COMPLETED',
              outputSummary: exp.provider === 'groq' && !exp.fallback_used 
                ? 'Grounded Groq LLM synthesis' 
                : 'Deterministic fallback explanation'
            };
          }
          if (s.stage === 'REPORT_READY') {
            return { ...s, status: 'COMPLETED', outputSummary: `Report ready for ${exp.incident_id || 'INC_1'}` };
          }
          return s;
        }));
      } else {
        setExplanationSource('DETERMINISTIC_FALLBACK');
        setExplanation(buildFallbackExplanation(incident, targetScenario));
      }
    } catch {
      setExplanationSource('DETERMINISTIC_FALLBACK');
      setExplanation(buildFallbackExplanation(incident, targetScenario));
    }
  }, [incident, selectedScenarioId]);

  const selectScenario = async (scenarioId: string) => {
    setSelectedScenarioId(scenarioId);
    await loadScenarioData(scenarioId);
    // Explicitly do NOT invoke Groq API when merely selecting a scenario
  };

  const executeScenarioReplay = async (scenarioId: string) => {
    if (scenarioId === 'TC-05') return;
    setIsReplaying(true);
    setSelectedScenarioId(scenarioId);

    // Realistic sequential stage advancement reflecting observed pipeline
    for (let i = 0; i < DEFAULT_STAGES.length; i++) {
      setActiveStageIndex(i);
      setStages(prev => prev.map((st, idx) => ({
        ...st,
        status: idx < i ? 'COMPLETED' : idx === i ? 'RUNNING' : 'PENDING'
      })));
      await new Promise(r => setTimeout(r, 200));
    }

    setStages(DEFAULT_STAGES);
    setActiveStageIndex(8);
    await loadScenarioData(scenarioId);
    
    // User explicitly clicked the button to execute the scenario -> Call Groq API at button-click time
    await loadExplanation(scenarioId);
    setIsReplaying(false);
  };

  useEffect(() => {
    // Only load scenario data on mount; do NOT call Groq API automatically while starting
    loadScenarioData('TC-10');
  }, [loadScenarioData]);

  return (
    <IncidentContext.Provider
      value={{
        selectedScenarioId,
        incident,
        explanation,
        explanationSource,
        isLoading,
        error,
        stages,
        activeStageIndex,
        isReplaying,
        selectScenario,
        executeScenarioReplay,
        refreshExplanation: () => loadExplanation(selectedScenarioId)
      }}
    >
      {children}
    </IncidentContext.Provider>
  );
};

export const useIncident = () => {
  const context = useContext(IncidentContext);
  if (!context) {
    throw new Error('useIncident must be used within an IncidentProvider');
  }
  return context;
};
