export type PageId =
  | 'overview'
  | 'scenarios'
  | 'models'
  | 'cross-dataset'
  | 'unseen-attack'
  | 'graph'
  | 'mitre'
  | 'ai-explanation'
  | 'methodology';

export interface PageMeta {
  id: PageId;
  title: string;
  shortLabel: string;
  iconName: string;
  description: string;
  phaseMilestone: string;
}

export const PAGES: PageMeta[] = [
  {
    id: 'overview',
    title: 'Security Command Center',
    shortLabel: 'Overview',
    iconName: 'Shield',
    description: 'Operational threat monitoring, active incident telemetry, and pipeline execution.',
    phaseMilestone: 'Phase 12B.1',
  },
  {
    id: 'scenarios',
    title: 'Scenario Lab (TC-01 – TC-10)',
    shortLabel: 'Scenarios',
    iconName: 'FlaskConical',
    description: 'Catalogue of 10 test scenarios with verified provenance, honest statuses, and execution controls.',
    phaseMilestone: 'Phase 12B.1',
  },
  {
    id: 'models',
    title: 'Model Evaluation & Benchmarks',
    shortLabel: 'Model Eval',
    iconName: 'Cpu',
    description: 'In-distribution performance for XGBoost, Random Forest, LightGBM, Isolation Forest, and Autoencoder.',
    phaseMilestone: 'Phase 12B.1',
  },
  {
    id: 'cross-dataset',
    title: 'Cross-Dataset Generalization',
    shortLabel: 'Cross-Dataset',
    iconName: 'Network',
    description: 'Real evaluation on 17.1M flows (NF-CSE-CIC-IDS2018-v2), distribution shift, and ToN-IoT audit.',
    phaseMilestone: 'Phase 12B.1',
  },
  {
    id: 'unseen-attack',
    title: 'Unseen Attack-Family Evaluation',
    shortLabel: 'Unseen Family',
    iconName: 'Target',
    description: 'Hold-out family zero-shot generalization experiments for Fuzzers and Reconnaissance.',
    phaseMilestone: 'Phase 12B.1',
  },
  {
    id: 'graph',
    title: 'Attack Graph & Event Investigation',
    shortLabel: 'Attack Graph',
    iconName: 'GitFork',
    description: 'Interactive Cytoscape.js reconstruction of the verified 8-event chain and isolated noise event.',
    phaseMilestone: 'Phase 12B.1',
  },
  {
    id: 'mitre',
    title: 'MITRE ATT&CK Matrix Mapping',
    shortLabel: 'MITRE Mapping',
    iconName: 'Layers',
    description: 'Deterministic ATT&CK tactic/technique mapping with source evidence links and confidence scoring.',
    phaseMilestone: 'Phase 12B.1',
  },
  {
    id: 'ai-explanation',
    title: 'AI Incident Explanation & Report',
    shortLabel: 'AI Report',
    iconName: 'FileText',
    description: 'Evidence-grounded narrative analysis, Groq/fallback status, and downloadable markdown reports.',
    phaseMilestone: 'Phase 12B.1',
  },
  {
    id: 'methodology',
    title: 'Methodology, Provenance & Limitations',
    shortLabel: 'Methodology',
    iconName: 'BookOpen',
    description: 'Dataset provenance, ablation study findings, NetFlow v2 policy, and claims boundary audit.',
    phaseMilestone: 'Phase 12B.1',
  },
];
