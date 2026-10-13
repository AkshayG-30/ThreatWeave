import React from 'react';
import { PageHeader } from '../components/PageHeader';
import { useIncident } from '../context/IncidentContext';
import { Layers, ShieldCheck, ExternalLink, Link2, AlertCircle } from 'lucide-react';

export const MitreMapping: React.FC = () => {
  const { incident, selectedScenarioId } = useIncident();

  const mappings = incident?.mitre_mappings || [];
  const evidenceItems = incident?.evidence_items || [];

  return (
    <div className="soc-placeholder-container">
      <PageHeader 
        title="MITRE ATT&CK Matrix Mapping" 
        subtitle="Deterministic mapping of correlated network events to standard MITRE Enterprise ATT&CK tactics and techniques."
        milestoneTag="Phase 12E Verified"
      />

      <div className="soc-banner-notice">
        <Layers size={18} style={{ color: 'var(--tw-accent-cyan)', flexShrink: 0, marginTop: '2px' }} />
        <div>
          <strong>Deterministic Grounding Contract:</strong> All ATT&CK classifications originate directly from 
          <code className="font-mono"> app.services.mitre_mapper.MitreMapper</code>. 
          Techniques are anchored to explicit network telemetry from incident 
          <strong className="font-mono" style={{ color: 'var(--tw-accent-cyan)' }}> {incident?.incident_id || 'INC_1'}</strong> ({selectedScenarioId}), not inferred by generative LLMs.
        </div>
      </div>

      {/* Technique Cards Grid */}
      <div className="soc-card" style={{ gap: '0.85rem' }}>
        <div className="soc-card-header" style={{ marginBottom: 0 }}>
          <div className="soc-card-title">
            <ShieldCheck size={16} style={{ color: 'var(--tw-accent-emerald)' }} />
            <span>Active Campaign Techniques ({mappings.length} Techniques Mapped)</span>
          </div>
          <span className="soc-badge soc-badge-emerald font-mono">DETERMINISTIC RULES</span>
        </div>

        {mappings.length === 0 ? (
          <div style={{ padding: '2rem 1rem', textAlign: 'center', color: 'var(--tw-text-muted)', fontSize: '0.85rem', background: 'var(--tw-bg-card)', borderRadius: 'var(--tw-radius-sm)', border: '1px solid var(--tw-border-subtle)' }}>
            Zero ATT&CK Techniques Mapped for {selectedScenarioId}: Telemetry represents normal baseline traffic or non-technique outlier flows.
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '0.85rem' }}>
            {mappings.map((m, idx) => (
            <div 
              key={idx} 
              style={{ 
                background: 'var(--tw-bg-card)', 
                padding: '0.9rem', 
                borderRadius: 'var(--tw-radius-sm)', 
                border: '1px solid var(--tw-border-subtle)',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.45rem'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                  <span className="font-mono" style={{ fontWeight: 700, color: 'var(--tw-accent-cyan)', fontSize: '1rem' }}>
                    {m.technique_id}
                  </span>
                  <span className={`soc-badge ${m.tactic === 'Discovery' ? 'soc-badge-purple' : m.tactic === 'Command and Control' ? 'soc-badge-amber' : m.tactic === 'Exfiltration' ? 'soc-badge-rose' : 'soc-badge-cyan'}`}>
                    {m.tactic?.toUpperCase()}
                  </span>
                </div>
                <span className={`soc-badge ${m.confidence === 'HIGH' ? 'soc-badge-emerald' : 'soc-badge-amber'}`}>
                  {m.confidence} CONFIDENCE
                </span>
              </div>

              <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--tw-text-primary)' }}>
                {m.technique_name}
              </div>

              <div style={{ color: 'var(--tw-text-secondary)', fontSize: '0.78rem', lineHeight: 1.4 }}>
                {m.evidence}
              </div>

              <div style={{ 
                background: 'var(--tw-bg-input)', 
                padding: '0.45rem 0.6rem', 
                borderRadius: 'var(--tw-radius-sm)',
                marginTop: 'auto',
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                fontSize: '0.72rem'
              }}>
                <Link2 size={12} style={{ color: 'var(--tw-accent-cyan)' }} />
                <span style={{ color: 'var(--tw-text-muted)' }}>Source Events:</span>
                <span className="font-mono" style={{ color: 'var(--tw-text-secondary)' }}>
                  {m.source_event_ids.join(', ')}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
      </div>

      {/* Correlated Evidence Items */}
      <div className="soc-card" style={{ gap: '0.85rem' }}>
        <div className="soc-card-header" style={{ marginBottom: 0 }}>
          <div className="soc-card-title">
            <Link2 size={16} style={{ color: 'var(--tw-accent-purple)' }} />
            <span>Correlated Evidence Items ({evidenceItems.length} Structured Anchors)</span>
          </div>
          <span className="soc-badge soc-badge-purple font-mono">EVIDENCE ANCHORS</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '0.85rem' }}>
          {evidenceItems.map((e, idx) => (
            <div 
              key={idx}
              style={{ 
                background: 'var(--tw-bg-card)', 
                padding: '0.85rem', 
                borderRadius: 'var(--tw-radius-sm)', 
                border: '1px solid var(--tw-border-subtle)',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.35rem'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="font-mono" style={{ color: 'var(--tw-accent-purple)', fontWeight: 600 }}>
                  {e.evidence_id}
                </span>
                <span className="soc-badge soc-badge-cyan font-mono">
                  {e.type} • {e.strength}
                </span>
              </div>
              <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.8rem' }}>
                {e.description}
              </p>
              {e.source_event_ids && e.source_event_ids.length > 0 && (
                <div className="font-mono" style={{ fontSize: '0.72rem', color: 'var(--tw-text-muted)' }}>
                  Linked Events: {e.source_event_ids.join(', ')}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
