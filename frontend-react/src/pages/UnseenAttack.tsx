import React from 'react';
import { PageHeader } from '../components/PageHeader';
import { Target, AlertTriangle, ShieldCheck, Database, FileCode } from 'lucide-react';

export const UnseenAttack: React.FC = () => {
  return (
    <div className="soc-placeholder-container">
      <PageHeader 
        title="Unseen Attack-Family Evaluation" 
        subtitle="Zero-shot generalization experiments evaluating detection capability when entire attack families are excluded from training."
        milestoneTag="Phase 12B.1 Verified"
      />

      <div className="soc-banner-notice">
        <Target size={18} style={{ color: 'var(--tw-accent-cyan)', flexShrink: 0, marginTop: '2px' }} />
        <div>
          <strong>Scientific Scope Boundary:</strong> These are hold-out attack family experiments, 
          <strong> NOT genuine zero-days in the wild</strong>. The models evaluated were trained from scratch with the targeted family completely held out from the training split.
          Confusion matrices strictly sum to declared test sizes (<code className="font-mono">Fuzzers: 30,207; Recon: 29,609</code>).
        </div>
      </div>

      <div className="soc-grid-2col">
        {/* Fuzzers Holdout */}
        <div className="soc-card" style={{ gap: '0.75rem' }}>
          <div className="soc-card-header">
            <div className="soc-card-title">
              <AlertTriangle size={16} style={{ color: 'var(--tw-accent-amber)' }} />
              <span>Held-Out Family: Fuzzers</span>
            </div>
            <span className="soc-badge soc-badge-amber">SUPPORT: 1,400 ATTACK FLOWS</span>
          </div>

          <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.82rem' }}>
            Model trained on 119,793 samples with zero Fuzzers flows. Evaluated on 30,207 test flows containing 1,400 held-out Fuzzers instances.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.4rem' }}>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>Recall</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--tw-accent-amber)' }}>68.64%</div>
            </div>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>Precision</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--tw-text-primary)' }}>93.12%</div>
            </div>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>F1-Score</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--tw-text-primary)' }}>79.03%</div>
            </div>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>FPR</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--tw-accent-emerald)' }}>0.25%</div>
            </div>
          </div>

          {/* Fuzzers Confusion Matrix */}
          <div style={{ background: 'var(--tw-bg-input)', padding: '0.75rem', borderRadius: 'var(--tw-radius-sm)', fontSize: '0.75rem' }}>
            <div style={{ fontWeight: 600, color: 'var(--tw-text-primary)', marginBottom: '0.4rem' }}>
              Confusion Matrix (Sum: 30,207)
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
                  <td style={{ color: 'var(--tw-accent-emerald)' }}>28,736 (TN)</td>
                  <td style={{ color: 'var(--tw-accent-rose)' }}>71 (FP)</td>
                  <td>28,807</td>
                </tr>
                <tr>
                  <td style={{ textAlign: 'left', padding: '0.25rem 0.2rem', color: 'var(--tw-text-secondary)' }}>Actual Fuzzers</td>
                  <td style={{ color: 'var(--tw-accent-amber)' }}>439 (FN)</td>
                  <td style={{ color: 'var(--tw-accent-emerald)' }}>961 (TP)</td>
                  <td>1,400</td>
                </tr>
              </tbody>
            </table>
            <div className="font-mono" style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem', marginTop: '0.35rem' }}>
              Artifact: experiments/unseen_attack/models/xgb_holdout_Fuzzers.json
            </div>
          </div>
        </div>

        {/* Reconnaissance Holdout */}
        <div className="soc-card" style={{ gap: '0.75rem' }}>
          <div className="soc-card-header">
            <div className="soc-card-title">
              <ShieldCheck size={16} style={{ color: 'var(--tw-accent-emerald)' }} />
              <span>Held-Out Family: Reconnaissance</span>
            </div>
            <span className="soc-badge soc-badge-emerald">SUPPORT: 802 ATTACK FLOWS</span>
          </div>

          <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.82rem' }}>
            Model trained on 120,391 samples with zero Reconnaissance flows. Evaluated on 29,609 test flows containing 802 held-out scanning instances.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.4rem' }}>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>Recall</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--tw-accent-emerald)' }}>100.0%</div>
            </div>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>Precision</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--tw-text-primary)' }}>87.46%</div>
            </div>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>F1-Score</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--tw-text-primary)' }}>93.31%</div>
            </div>
            <div style={{ background: 'var(--tw-bg-card)', padding: '0.65rem', borderRadius: 'var(--tw-radius-sm)' }}>
              <div style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem' }}>FPR</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--tw-accent-emerald)' }}>0.40%</div>
            </div>
          </div>

          {/* Reconnaissance Confusion Matrix */}
          <div style={{ background: 'var(--tw-bg-input)', padding: '0.75rem', borderRadius: 'var(--tw-radius-sm)', fontSize: '0.75rem' }}>
            <div style={{ fontWeight: 600, color: 'var(--tw-text-primary)', marginBottom: '0.4rem' }}>
              Confusion Matrix (Sum: 29,609)
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
                  <td style={{ color: 'var(--tw-accent-emerald)' }}>28,692 (TN)</td>
                  <td style={{ color: 'var(--tw-accent-rose)' }}>115 (FP)</td>
                  <td>28,807</td>
                </tr>
                <tr>
                  <td style={{ textAlign: 'left', padding: '0.25rem 0.2rem', color: 'var(--tw-text-secondary)' }}>Actual Recon</td>
                  <td style={{ color: 'var(--tw-accent-emerald)' }}>0 (FN)</td>
                  <td style={{ color: 'var(--tw-accent-emerald)' }}>802 (TP)</td>
                  <td>802</td>
                </tr>
              </tbody>
            </table>
            <div className="font-mono" style={{ color: 'var(--tw-text-muted)', fontSize: '0.7rem', marginTop: '0.35rem' }}>
              Artifact: experiments/unseen_attack/models/xgb_holdout_Reconnaissance.json
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
