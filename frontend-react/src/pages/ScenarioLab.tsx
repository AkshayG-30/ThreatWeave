import React, { useState } from 'react';
import { PageHeader } from '../components/PageHeader';
import { StatusBadge } from '../components/StatusBadge';
import { SCENARIO_CATALOGUE } from '../types/scenario';
import { useIncident } from '../context/IncidentContext';
import { 
  FlaskConical, 
  Play, 
  AlertCircle, 
  Database, 
  FileCode, 
  CheckCircle2, 
  ArrowRight,
  RefreshCw
} from 'lucide-react';
import type { PageId } from '../types/navigation';

interface ScenarioLabProps {
  onNavigate: (page: PageId) => void;
}

export const ScenarioLab: React.FC<ScenarioLabProps> = ({ onNavigate }) => {
  const { 
    selectedScenarioId, 
    incident, 
    isReplaying, 
    executeScenarioReplay 
  } = useIncident();

  const [notification, setNotification] = useState<string | null>(null);

  const handleExecute = async (id: string) => {
    if (id === 'TC-05') return;
    await executeScenarioReplay(id);
    setNotification(`${id} scenario successfully loaded and verified. Telemetry synchronized across Command Center, Attack Graph, MITRE Matrix, and AI Report.`);
  };

  return (
    <div className="soc-placeholder-container">
      <PageHeader 
        title="Scenario Lab" 
        subtitle="Catalogue of ten test scenarios with verified provenance, underlying evidence, and execution readiness."
        milestoneTag="Phase 12E Verified"
      />

      {notification && (
        <div style={{
          background: 'rgba(16, 185, 129, 0.12)',
          border: '1px solid rgba(16, 185, 129, 0.4)',
          borderRadius: 'var(--tw-radius-md)',
          padding: '0.75rem 1rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          color: 'var(--tw-accent-emerald)',
          fontSize: '0.82rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <CheckCircle2 size={16} />
            <span>{notification}</span>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button 
              className="soc-btn soc-btn-primary" 
              onClick={() => onNavigate('graph')}
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.72rem' }}
            >
              <span>View Graph</span>
              <ArrowRight size={12} />
            </button>
            <button 
              className="soc-btn soc-btn-secondary" 
              onClick={() => setNotification(null)}
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.72rem' }}
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      <div className="soc-banner-notice">
        <FlaskConical size={18} style={{ color: 'var(--tw-accent-cyan)', flexShrink: 0, marginTop: '2px' }} />
        <div>
          <strong>Scientific Integrity Guard:</strong> In accordance with the Phase 12A audit, scenarios are never marked 
          <code className="font-mono"> VERIFIED</code> until underlying fixtures and outputs exist. 
          Unpopulated scenarios have execution disabled with explicit provenance and prerequisites documented below.
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '1rem' }}>
        {SCENARIO_CATALOGUE.map((sc) => {
          const isSelected = selectedScenarioId === sc.id;
          return (
            <div 
              key={sc.id} 
              className="soc-card" 
              style={{ 
                gap: '0.7rem',
                borderColor: isSelected ? 'var(--tw-accent-cyan)' : 'var(--tw-border-subtle)',
                boxShadow: isSelected ? '0 0 14px rgba(6, 182, 212, 0.15)' : undefined
              }}
            >
              <div className="soc-card-header" style={{ marginBottom: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span className="font-mono" style={{ fontWeight: 700, color: 'var(--tw-accent-cyan)', fontSize: '1rem' }}>
                    {sc.id}
                  </span>
                  <span style={{ fontSize: '0.88rem', fontWeight: 600 }}>{sc.name}</span>
                </div>
                <StatusBadge status={sc.status} />
              </div>

              <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.82rem', flex: 1 }}>
                {sc.description}
              </p>

              <div style={{ 
                background: 'var(--tw-bg-input)', 
                padding: '0.65rem', 
                borderRadius: 'var(--tw-radius-sm)', 
                fontSize: '0.74rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.35rem',
                color: 'var(--tw-text-muted)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <Database size={12} style={{ color: 'var(--tw-accent-purple)' }} />
                  <span>Dataset: <strong style={{ color: 'var(--tw-text-secondary)' }}>{sc.sourceDataset}</strong></span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <FileCode size={12} style={{ color: 'var(--tw-accent-cyan)' }} />
                  <span>Artifact: <code className="font-mono" style={{ color: 'var(--tw-text-secondary)' }}>{sc.underlyingArtifact}</code></span>
                </div>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.35rem', marginTop: '0.15rem' }}>
                  <AlertCircle size={12} style={{ color: sc.isExecutable ? 'var(--tw-accent-emerald)' : 'var(--tw-accent-amber)', flexShrink: 0, marginTop: '2px' }} />
                  <span style={{ color: sc.isExecutable ? 'var(--tw-accent-emerald)' : 'var(--tw-accent-amber)', lineHeight: 1.3 }}>
                    {sc.statusReason}
                  </span>
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.25rem' }}>
                <span className="soc-badge soc-badge-muted font-mono" style={{ fontSize: '0.68rem' }}>
                  {sc.primaryCapability}
                </span>
                
                {sc.isExecutable ? (
                  <button 
                    className="soc-btn soc-btn-primary"
                    disabled={isReplaying}
                    onClick={() => handleExecute(sc.id)}
                    style={{ padding: '0.35rem 0.8rem' }}
                  >
                    {isReplaying && selectedScenarioId === sc.id ? (
                      <>
                        <RefreshCw size={12} className="animate-spin" />
                        <span>Replaying & Calling Groq...</span>
                      </>
                    ) : (
                      <>
                        <Play size={12} />
                        <span>Execute Scenario</span>
                      </>
                    )}
                  </button>
                ) : (
                  <button 
                    className="soc-btn soc-btn-secondary"
                    disabled={true}
                    title={sc.statusReason}
                    style={{ padding: '0.35rem 0.8rem' }}
                  >
                    <span>Execution Disabled</span>
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
