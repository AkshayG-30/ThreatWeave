import React from 'react';
import { PageHeader } from '../components/PageHeader';
import { BookOpen, CheckCircle, XCircle, Database, GitMerge, FileCode } from 'lucide-react';

export const Methodology: React.FC = () => {
  return (
    <div className="soc-placeholder-container">
      <PageHeader 
        title="Methodology, Dataset Provenance & Limitations" 
        subtitle="Layered ablation study findings, NetFlow v2 feature policy, and claims boundary audit."
        milestoneTag="Phase 12B.1 Verified"
      />

      <div className="soc-banner-notice">
        <BookOpen size={18} style={{ color: 'var(--tw-accent-cyan)', flexShrink: 0, marginTop: '2px' }} />
        <div>
          <strong>Scientific Integrity Contract:</strong> ThreatWeave strictly delineates verified engineering achievements 
          from known theoretical and empirical boundaries. Below is the audited breakdown from <code className="font-mono">docs/CLAIMS_AUDIT.md</code> 
          and the formal multi-layer ablation study (<code className="font-mono">experiments/ablation/ablation_results.json</code>).
        </div>
      </div>

      {/* Layered Ablation Study Table */}
      <div className="soc-card" style={{ gap: '0.75rem' }}>
        <div className="soc-card-header" style={{ marginBottom: 0 }}>
          <div className="soc-card-title">
            <GitMerge size={16} style={{ color: 'var(--tw-accent-cyan)' }} />
            <span>Formal Layered Ablation Study (experiments/ablation/ablation_results.json)</span>
          </div>
          <span className="soc-badge soc-badge-cyan font-mono">STAGES A THROUGH E</span>
        </div>

        <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.82rem' }}>
          Quantifying the contribution of each architectural layer: Supervised point detection → Anomaly detection → Bounded correlation → Graph assembly → Contextual explanation.
        </p>

        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', textAlign: 'left' }}>
          <thead>
            <tr style={{ color: 'var(--tw-text-muted)', borderBottom: '1px solid var(--tw-border-subtle)' }}>
              <th style={{ padding: '0.5rem' }}>Layer Configuration</th>
              <th>Recall</th>
              <th>Precision</th>
              <th>F1-Score</th>
              <th>FPR</th>
              <th>Architectural Effect & Evidence</th>
            </tr>
          </thead>
          <tbody className="font-mono">
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
              <td style={{ padding: '0.5rem', color: 'var(--tw-text-primary)' }}><strong>Stage A: Baseline</strong> (Supervised XGBoost)</td>
              <td style={{ color: 'var(--tw-accent-emerald)' }}>99.89%</td>
              <td>91.60%</td>
              <td>95.56%</td>
              <td style={{ color: 'var(--tw-accent-emerald)' }}>0.38%</td>
              <td style={{ color: 'var(--tw-text-secondary)' }}>Rapid point-detections, 1 FN on test split (TP: 894, FP: 82)</td>
            </tr>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
              <td style={{ padding: '0.5rem', color: 'var(--tw-text-primary)' }}><strong>Stage B: + Anomaly</strong> (Isolation Forest)</td>
              <td style={{ color: 'var(--tw-accent-emerald)' }}>100.0%</td>
              <td style={{ color: 'var(--tw-accent-amber)' }}>37.01%</td>
              <td>54.03%</td>
              <td style={{ color: 'var(--tw-accent-rose)' }}>7.05%</td>
              <td style={{ color: 'var(--tw-text-secondary)' }}>Rescues 1 FN raising recall to 100%, but spikes FPR from 0.38% to 7.05% (1,523 FPs)</td>
            </tr>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
              <td style={{ padding: '0.5rem', color: 'var(--tw-text-primary)' }}><strong>Stage C: + Correlation</strong> (Entity & Temporal)</td>
              <td style={{ color: 'var(--tw-accent-emerald)' }}>100.0%</td>
              <td>Bound</td>
              <td>Bound</td>
              <td style={{ color: 'var(--tw-accent-emerald)' }}>Filtered</td>
              <td style={{ color: 'var(--tw-text-secondary)' }}>100% chain completeness, 100% noise isolation (orphans uncorrelated anomaly alerts)</td>
            </tr>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
              <td style={{ padding: '0.5rem', color: 'var(--tw-text-primary)' }}><strong>Stage D: + Graph</strong> (NetworkX Directed)</td>
              <td style={{ color: 'var(--tw-accent-emerald)' }}>100.0%</td>
              <td>1.0 Prec</td>
              <td>20 Edges</td>
              <td>0.0 Noise</td>
              <td style={{ color: 'var(--tw-text-secondary)' }}>Constructs 20 directed evidence relationships across 8 campaign nodes in 1 connected component</td>
            </tr>
            <tr>
              <td style={{ padding: '0.5rem', color: 'var(--tw-text-primary)' }}><strong>Stage E: + AI Explanation</strong> (Groq / Fallback)</td>
              <td style={{ color: 'var(--tw-accent-cyan)' }}>Grounded</td>
              <td>Grounded</td>
              <td>Schema</td>
              <td>Verified</td>
              <td style={{ color: 'var(--tw-text-secondary)' }}>Contextual narrative synthesis strictly constrained to structured incident facts</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Claims Audit Grid */}
      <div className="soc-grid-2col">
        {/* Supported Claims */}
        <div className="soc-card" style={{ gap: '0.65rem' }}>
          <div className="soc-card-header">
            <div className="soc-card-title">
              <CheckCircle size={16} style={{ color: 'var(--tw-accent-emerald)' }} />
              <span>Supported Capabilities (Physical Proof)</span>
            </div>
            <span className="soc-badge soc-badge-emerald">VERIFIED</span>
          </div>

          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.45rem', fontSize: '0.8rem', color: 'var(--tw-text-secondary)' }}>
            <li>✓ <strong>Supervised Detection:</strong> Frozen production XGBoost (99.89% recall on NF-UNSW).</li>
            <li>✓ <strong>Anomaly Outlier Detection:</strong> Frozen Isolation Forest operating in 41-feature space.</li>
            <li>✓ <strong>Bounded Correlation:</strong> Entity-sharing and temporal windowing (Δt ≤ 30s) mitigating anomaly alert fatigue.</li>
            <li>✓ <strong>Graph Reconstruction:</strong> Directed topological assembly mapping 8 attack events and 20 edges.</li>
            <li>✓ <strong>Deterministic ATT&CK Mapping:</strong> Anchored to explicit evidence (T1046, T1210, T1071, T1041).</li>
            <li>✓ <strong>Cross-Dataset Real Evaluation:</strong> Evaluated on 17.1M flows from NF-CSE-CIC-IDS2018-v2.</li>
            <li>✓ <strong>Hold-Out Family Generalization:</strong> Fuzzers (F1: 79.03%) and Reconnaissance (Recall: 100%).</li>
          </ul>
        </div>

        {/* Claims We Must Not Make */}
        <div className="soc-card" style={{ gap: '0.65rem' }}>
          <div className="soc-card-header">
            <div className="soc-card-title">
              <XCircle size={16} style={{ color: 'var(--tw-accent-rose)' }} />
              <span>Audited Boundaries & Non-Claims</span>
            </div>
            <span className="soc-badge soc-badge-rose">LIMITATIONS</span>
          </div>

          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.45rem', fontSize: '0.8rem', color: 'var(--tw-text-muted)' }}>
            <li>✗ <strong>Zero-Day in the Wild:</strong> Evaluated on held-out academic families, not uncatalogued zero-days in live networks.</li>
            <li>✗ <strong>SOTA Claims:</strong> Architectural demonstration, not hyperparameter-tuned academic benchmark SotA.</li>
            <li>✗ <strong>GNN Graph Reasoning:</strong> Evaluated and deferred; single-incident training graphs risk severe overfitting.</li>
            <li>✗ <strong>GRU Temporal Modeling:</strong> Deferred because NF-UNSW lacks chronological microsecond timestamps.</li>
            <li>✗ <strong>NF-ToN-IoT Evaluation:</strong> Rejected by audit due to 31 missing features.</li>
            <li>✗ <strong>LLM Improves Accuracy:</strong> LLM operates purely post-detection with zero classification capability.</li>
            <li>✗ <strong>Autoencoder Universally Superior:</strong> Higher precision (+14%) but lower recall (-1.3%) than Isolation Forest.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
