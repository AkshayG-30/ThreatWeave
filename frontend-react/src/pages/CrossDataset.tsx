import React from 'react';
import { PageHeader } from '../components/PageHeader';
import { Network, AlertOctagon, XCircle, Database, ShieldAlert } from 'lucide-react';

export const CrossDataset: React.FC = () => {
  return (
    <div className="soc-placeholder-container">
      <PageHeader 
        title="Cross-Dataset Generalization & Transfer Lab" 
        subtitle="Empirical evaluation of the NF-UNSW-NB15-v2 model on external network distributions, exposing distribution shift."
        milestoneTag="Phase 12B.1 Verified"
      />

      <div className="soc-banner-notice">
        <Network size={18} style={{ color: 'var(--tw-accent-cyan)', flexShrink: 0, marginTop: '2px' }} />
        <div>
          <strong>Scientific Honesty & Verified Reality:</strong> Rather than claiming universal transferability, ThreatWeave physically evaluated 
          <code className="font-mono"> 17,129,715 flows</code> from the real <code className="font-mono">NF-CSE-CIC-IDS2018-v2</code> dataset. 
          Results prove severe cross-dataset distribution shift (<code className="font-mono">F1: 1.96%, FPR: 41.50%</code>), 
          demonstrating why raw supervised predictions cannot be trusted in isolation without correlation and triage.
        </div>
      </div>

      <div className="soc-grid-2col">
        {/* Real CIC-IDS2018 Evaluation */}
        <div className="soc-card" style={{ gap: '0.75rem' }}>
          <div className="soc-card-header">
            <div className="soc-card-title">
              <AlertOctagon size={16} style={{ color: 'var(--tw-accent-amber)' }} />
              <span>Real Evaluation: NF-CSE-CIC-IDS2018-V2</span>
            </div>
            <span className="soc-badge soc-badge-amber">17.1M FLOWS EVALUATED</span>
          </div>

          <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.82rem' }}>
            Production XGBoost model (trained on NF-UNSW) evaluated without retraining against 17,129,715 NetFlow v2 records.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.4rem' }}>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>Accuracy</div>
              <div style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--tw-text-primary)' }}>52.05%</div>
            </div>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>Precision</div>
              <div style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--tw-accent-rose)' }}>1.30%</div>
            </div>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>Recall</div>
              <div style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--tw-accent-amber)' }}>4.06%</div>
            </div>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>F1-Score</div>
              <div style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--tw-accent-rose)' }}>1.96%</div>
            </div>
          </div>

          {/* Verified Confusion Matrix */}
          <div style={{ background: 'var(--tw-bg-input)', padding: '0.75rem', borderRadius: 'var(--tw-radius-sm)', fontSize: '0.75rem' }}>
            <div style={{ fontWeight: 600, color: 'var(--tw-text-primary)', marginBottom: '0.4rem' }}>
              Confusion Matrix (Total Flows: 17,129,715)
            </div>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center' }}>
              <thead>
                <tr style={{ color: 'var(--tw-text-muted)', borderBottom: '1px solid var(--tw-border-subtle)' }}>
                  <th style={{ textAlign: 'left', padding: '0.2rem' }}>Actual \ Predicted</th>
                  <th>Predicted Benign</th>
                  <th>Predicted Attack</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody className="font-mono">
                <tr>
                  <td style={{ textAlign: 'left', padding: '0.25rem 0.2rem', color: 'var(--tw-text-secondary)' }}>Actual Benign</td>
                  <td style={{ color: 'var(--tw-accent-emerald)' }}>8,833,889 (TN)</td>
                  <td style={{ color: 'var(--tw-accent-rose)' }}>6,267,796 (FP)</td>
                  <td>15,101,685</td>
                </tr>
                <tr>
                  <td style={{ textAlign: 'left', padding: '0.25rem 0.2rem', color: 'var(--tw-text-secondary)' }}>Actual Attack</td>
                  <td style={{ color: 'var(--tw-accent-rose)' }}>1,945,768 (FN)</td>
                  <td style={{ color: 'var(--tw-accent-emerald)' }}>82,262 (TP)</td>
                  <td>2,028,030</td>
                </tr>
              </tbody>
            </table>
            <div className="font-mono" style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem', marginTop: '0.35rem' }}>
              FPR: 41.50% • Specificity: 58.50% • Artifact: experiments/cross_dataset_real/metrics.json
            </div>
          </div>
        </div>

        {/* NF-ToN-IoT Structural Rejection Audit */}
        <div className="soc-card" style={{ gap: '0.75rem' }}>
          <div className="soc-card-header">
            <div className="soc-card-title">
              <XCircle size={16} style={{ color: 'var(--tw-accent-rose)' }} />
              <span>NF-ToN-IoT Incompatibility Audit</span>
            </div>
            <span className="soc-badge soc-badge-rose">REJECTED BY AUDIT</span>
          </div>

          <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.82rem' }}>
            Audited for secondary cross-dataset evaluation. Formally rejected due to severe structural incompatibility with our frozen 41-feature standard.
          </p>

          <div style={{ background: 'var(--tw-bg-card)', padding: '0.85rem', borderRadius: 'var(--tw-radius-sm)', border: '1px solid var(--tw-border-subtle)' }}>
            <div style={{ fontWeight: 600, color: 'var(--tw-accent-rose)', marginBottom: '0.35rem', fontSize: '0.88rem' }}>
              Missing Pipeline Features: 31 / 41 (75.6% Incompatible)
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--tw-text-secondary)', lineHeight: 1.4 }}>
              ToN-IoT lacks essential flow metrics including TCP window sizes, retransmission counts, TCP flag distributions, packet inter-arrival times, and ICMP metadata.
            </div>
          </div>

          <div style={{ background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.25)', padding: '0.75rem', borderRadius: 'var(--tw-radius-sm)', fontSize: '0.78rem', color: 'var(--tw-text-secondary)' }}>
            <strong style={{ color: 'var(--tw-accent-rose)' }}>Refusal of Synthetic Imputation:</strong> Many systems fill missing features with zeros or means. ThreatWeave rejected this practice to maintain scientific integrity and prevent false conclusions.
          </div>

          <div className="font-mono" style={{ fontSize: '0.72rem', color: 'var(--tw-text-muted)' }}>
            Audit Decision: REJECTED • Artifact: experiments/cross_dataset_toniot/inspection.json
          </div>
        </div>
      </div>

      {/* Target Dataset Category Breakdown Table */}
      <div className="soc-card" style={{ gap: '0.75rem' }}>
        <div className="soc-card-header" style={{ marginBottom: 0 }}>
          <div className="soc-card-title">
            <Database size={16} style={{ color: 'var(--tw-accent-cyan)' }} />
            <span>CIC-IDS2018 Attack Detection Breakdown (experiments/cross_dataset_real/target_attack_categories.csv)</span>
          </div>
          <span className="soc-badge soc-badge-muted font-mono">14 ATTACK CATEGORIES</span>
        </div>

        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', textAlign: 'left' }}>
          <thead>
            <tr style={{ color: 'var(--tw-text-muted)', borderBottom: '1px solid var(--tw-border-subtle)' }}>
              <th style={{ padding: '0.45rem' }}>Attack Category</th>
              <th>Support Flows</th>
              <th>Detected Flows</th>
              <th>Detection Rate (Recall)</th>
              <th>Transfer Analysis</th>
            </tr>
          </thead>
          <tbody className="font-mono">
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
              <td style={{ padding: '0.45rem', color: 'var(--tw-text-primary)' }}>Infilteration</td>
              <td>115,513</td>
              <td style={{ color: 'var(--tw-accent-emerald)' }}>76,184</td>
              <td style={{ color: 'var(--tw-accent-emerald)' }}>65.95%</td>
              <td style={{ color: 'var(--tw-text-muted)' }}>Partial feature alignment with UNSW exploit signatures</td>
            </tr>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
              <td style={{ padding: '0.45rem', color: 'var(--tw-text-primary)' }}>DDoS attacks-LOIC-HTTP</td>
              <td>207,078</td>
              <td>5,847</td>
              <td>2.82%</td>
              <td style={{ color: 'var(--tw-text-muted)' }}>Heavy distribution divergence from UNSW DoS</td>
            </tr>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
              <td style={{ padding: '0.45rem', color: 'var(--tw-text-primary)' }}>DoS attacks-Hulk</td>
              <td>432,648</td>
              <td>192</td>
              <td>0.04%</td>
              <td style={{ color: 'var(--tw-text-muted)' }}>Near-total miss due to different packet rate distribution</td>
            </tr>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
              <td style={{ padding: '0.45rem', color: 'var(--tw-text-primary)' }}>SSH-Bruteforce</td>
              <td>94,979</td>
              <td>30</td>
              <td>0.03%</td>
              <td style={{ color: 'var(--tw-text-muted)' }}>Lacks direct UNSW counterpart; flagged as background</td>
            </tr>
            <tr>
              <td style={{ padding: '0.45rem', color: 'var(--tw-text-primary)' }}>DDOS attack-HOIC</td>
              <td>1,066,881</td>
              <td>0</td>
              <td style={{ color: 'var(--tw-accent-rose)' }}>0.00%</td>
              <td style={{ color: 'var(--tw-accent-rose)' }}>Complete detection collapse under protocol shift</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
