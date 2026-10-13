import React from 'react';
import { PageHeader } from '../components/PageHeader';
import { StatusBadge } from '../components/StatusBadge';
import { useIncident } from '../context/IncidentContext';
import { 
  Shield, 
  GitFork, 
  Layers, 
  FileText, 
  Play, 
  RefreshCw, 
  CheckCircle2, 
  AlertTriangle,
  ArrowRight,
  Database,
  Cpu
} from 'lucide-react';
import type { PageId } from '../types/navigation';

interface SecurityOverviewProps {
  onNavigate: (page: PageId) => void;
}

export const SecurityOverview: React.FC<SecurityOverviewProps> = ({ onNavigate }) => {
  const { 
    selectedScenarioId, 
    incident, 
    stages, 
    isReplaying, 
    executeScenarioReplay 
  } = useIncident();

  return (
    <div className="soc-placeholder-container">
      <PageHeader 
        title="Security Command Center" 
        subtitle="Operational threat telemetry, verified multi-stage campaign reconstruction, and pipeline execution."
        milestoneTag="Phase 12E Verified"
        actions={
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <button 
              className="soc-btn soc-btn-secondary"
              onClick={() => onNavigate('scenarios')}
            >
              <span>Scenario Lab</span>
            </button>
            <button 
              className="soc-btn soc-btn-primary"
              disabled={isReplaying}
              onClick={() => executeScenarioReplay(selectedScenarioId)}
            >
              {isReplaying ? (
                <>
                  <RefreshCw size={13} className="animate-spin" />
                  <span>Replaying Stages...</span>
                </>
              ) : (
                <>
                  <Play size={13} />
                  <span>Replay Pipeline Execution</span>
                </>
              )}
            </button>
          </div>
        }
      />

      {/* Execution Context Banner */}
      <div className="soc-banner-notice" style={{ borderColor: 'rgba(6, 182, 212, 0.35)' }}>
        <Database size={18} style={{ color: 'var(--tw-accent-cyan)', flexShrink: 0, marginTop: '2px' }} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem', flex: 1 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
            <span>
              <strong>Execution Mode:</strong>{' '}
              <span className="font-mono" style={{ color: 'var(--tw-accent-cyan)' }}>
                {(incident?.execution_mode || 'CONTROLLED_REPLAY').replace('_', ' ')} ({selectedScenarioId})
              </span>
            </span>
            <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
              <span className="soc-badge soc-badge-emerald font-mono">DETERMINISTIC CACHE GUARD ACTIVE</span>
              <span className="soc-badge soc-badge-purple font-mono">{incident?.source_dataset || 'NF-UNSW-NB15-v2'}</span>
            </div>
          </div>
          <span style={{ fontSize: '0.78rem', color: 'var(--tw-text-muted)' }}>
            Telemetry represents verified {incident?.execution_mode === 'LIVE_INFERENCE' ? 'model inference on untouched test split' : (incident?.execution_mode === 'RECORDED_EVALUATION' ? 'recorded benchmark experiment artifact' : 'controlled attack replay')} ({incident?.incident_id || 'INC_1'}).
          </span>
        </div>
      </div>

      {/* Top Telemetry Row */}
      <div className="soc-metrics-grid">
        <div className="soc-stat-card">
          <div className="soc-stat-header">
            <span>Threat Severity</span>
            {selectedScenarioId === 'TC-01' ? (
              <CheckCircle2 size={15} style={{ color: 'var(--tw-accent-emerald)' }} />
            ) : (
              <AlertTriangle size={15} style={{ color: 'var(--tw-accent-rose)' }} />
            )}
          </div>
          <div className="soc-stat-value" style={{ color: selectedScenarioId === 'TC-01' ? 'var(--tw-accent-emerald)' : 'var(--tw-accent-rose)' }}>
            {selectedScenarioId === 'TC-01' ? 'NORMAL' : 'CRITICAL'}
          </div>
          <div className="soc-stat-footer font-mono">
            Active Campaign: {incident?.incident_id || 'INC_1'}
          </div>
        </div>

        <div className="soc-stat-card">
          <div className="soc-stat-header">
            <span>Chain Events</span>
            <Shield size={15} style={{ color: 'var(--tw-accent-cyan)' }} />
          </div>
          <div className="soc-stat-value font-mono">
            {incident?.event_count ?? 8}
          </div>
          <div className="soc-stat-footer">
            {incident && incident.event_count > 0 
              ? `Loaded network flows (${incident.events[0]?.event_id} to ${incident.events[incident.events.length - 1]?.event_id})`
              : 'Correlated attack flows (EV_01 to EV_08)'}
          </div>
        </div>

        <div className="soc-stat-card">
          <div className="soc-stat-header">
            <span>Evidence Edges</span>
            <GitFork size={15} style={{ color: 'var(--tw-accent-purple)' }} />
          </div>
          <div className="soc-stat-value font-mono">
            {incident?.edges?.length ?? 20}
          </div>
          <div className="soc-stat-footer font-mono">
            Score: {incident ? incident.correlation_score.toFixed(1) : '22.8'}
          </div>
        </div>

        <div className="soc-stat-card">
          <div className="soc-stat-header">
            <span>MITRE Techniques</span>
            <Layers size={15} style={{ color: 'var(--tw-accent-emerald)' }} />
          </div>
          <div className="soc-stat-value font-mono">
            {incident?.mitre_mappings?.length ?? 4}
          </div>
          <div className="soc-stat-footer">
            {incident && incident.mitre_mappings.length === 0
              ? 'Zero attack techniques (Benign Baseline)'
              : 'Deterministic rule-grounded T-codes'}
          </div>
        </div>
      </div>

      {/* Real Nine-Stage Pipeline Visualization */}
      <div className="soc-card" style={{ gap: '0.65rem' }}>
        <div className="soc-card-header" style={{ marginBottom: '0.25rem' }}>
          <div className="soc-card-title">
            <Cpu size={16} style={{ color: 'var(--tw-accent-cyan)' }} />
            <span>Layered Defense Execution Pipeline (9 Stages)</span>
          </div>
          <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
            <span className="soc-badge soc-badge-cyan font-mono" style={{ fontSize: '0.68rem' }}>
              REPLAY OBSERVABILITY
            </span>
          </div>
        </div>

        <div className="pipeline-stepper">
          {stages.map((st, idx) => {
            const isCompleted = st.status === 'COMPLETED';
            const isRunning = st.status === 'RUNNING';
            return (
              <div 
                key={st.stage} 
                className={`pipeline-step-item ${isCompleted ? 'completed' : isRunning ? 'running' : ''}`}
              >
                <div className="pipeline-step-header">
                  <span className="font-mono" style={{ color: isRunning ? 'var(--tw-accent-cyan)' : 'var(--tw-text-muted)' }}>
                    0{idx + 1}
                  </span>
                  {isCompleted ? (
                    <CheckCircle2 size={12} style={{ color: 'var(--tw-accent-emerald)' }} />
                  ) : isRunning ? (
                    <RefreshCw size={12} className="animate-spin" style={{ color: 'var(--tw-accent-cyan)' }} />
                  ) : (
                    <span style={{ fontSize: '0.65rem', color: 'var(--tw-text-muted)' }}>•</span>
                  )}
                </div>
                <div className="pipeline-step-title">{st.label}</div>
                <div className="pipeline-step-desc">{st.description}</div>
                {st.outputSummary && (
                  <div className="font-mono" style={{ fontSize: '0.65rem', color: isCompleted ? 'var(--tw-accent-emerald)' : 'var(--tw-text-muted)', marginTop: 'auto', paddingTop: '0.2rem' }}>
                    {st.outputSummary}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Fast Navigation to Incident Investigation */}
      <div className="soc-grid-2col">
        {/* Topology Summary */}
        <div className="soc-card" style={{ gap: '0.75rem' }}>
          <div className="soc-card-header">
            <div className="soc-card-title">
              <GitFork size={16} style={{ color: 'var(--tw-accent-cyan)' }} />
              <span>Attack Graph Topology ({incident?.incident_id || 'INC_1'})</span>
            </div>
            <button className="soc-btn soc-btn-secondary" onClick={() => onNavigate('graph')} style={{ padding: '0.25rem 0.6rem', fontSize: '0.72rem' }}>
              <span>Interactive Graph</span>
              <ArrowRight size={12} />
            </button>
          </div>
          <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.82rem' }}>
            {incident && incident.edges.length === 0
              ? 'Normal background baseline: zero correlation edges between flows.'
              : `The reconstruction organizes ${incident?.event_count ?? 8} sequence events spanning detected network actions.`}
          </p>
          <div className="font-mono" style={{ fontSize: '0.75rem', background: 'var(--tw-bg-input)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)', color: 'var(--tw-text-muted)' }}>
            Attack Chain: {incident && incident.events.length > 0 ? incident.events.map(e => e.event_id).join(' → ') : 'EV_01 → EV_02 → ...'}<br />
            Isolated Noise: {incident?.edges.length === 0 ? '0 noise (all normal)' : '100% filtered from candidate incident'}
          </div>
        </div>

        {/* Intelligence & Report */}
        <div className="soc-card" style={{ gap: '0.75rem' }}>
          <div className="soc-card-header">
            <div className="soc-card-title">
              <FileText size={16} style={{ color: 'var(--tw-accent-purple)' }} />
              <span>AI Explanation & Compliance Report</span>
            </div>
            <button className="soc-btn soc-btn-secondary" onClick={() => onNavigate('ai-explanation')} style={{ padding: '0.25rem 0.6rem', fontSize: '0.72rem' }}>
              <span>View Report</span>
              <ArrowRight size={12} />
            </button>
          </div>
          <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.82rem' }}>
            Grounded contextual incident narrative linking network evidence directly to Enterprise ATT&CK matrix classifications without LLM hallucination.
          </p>
          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
            {incident && incident.mitre_mappings.length > 0 ? (
              incident.mitre_mappings.map(m => (
                <span key={m.technique_id} className="soc-badge soc-badge-cyan">
                  {m.technique_id}: {m.tactic?.toUpperCase() || 'TECHNIQUE'}
                </span>
              ))
            ) : (
              <span className="soc-badge soc-badge-muted font-mono">
                ZERO ATT&CK TECHNIQUES (BENIGN FLOWS)
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
