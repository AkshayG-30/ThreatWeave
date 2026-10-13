export type ScenarioStatus = 
  | 'VERIFIED'
  | 'IMPLEMENTATION REQUIRED'
  | 'EXPERIMENTAL ARTIFACT PRESENT'
  | 'REQUIRES DATA'
  | 'BLOCKED';

export interface ScenarioMeta {
  id: string;
  name: string;
  description: string;
  category: string;
  primaryCapability: string;
  status: ScenarioStatus;
  statusReason: string;
  sourceDataset: string;
  underlyingArtifact: string;
  isExecutable: boolean;
}

export const SCENARIO_CATALOGUE: ScenarioMeta[] = [
  {
    id: 'TC-01',
    name: 'Benign Traffic Baseline',
    description: 'Validates detector specificity and evaluates against false alarm spikes on normal network flows.',
    category: 'Baseline',
    primaryCapability: 'SPECIFICITY / FPR',
    status: 'VERIFIED',
    statusReason: 'Verified zero false alarms across both Supervised XGBoost and Anomaly Isolation Forest on normal network flows from untouched test split.',
    sourceDataset: 'NF-UNSW-NB15-v2 (Test Split)',
    underlyingArtifact: 'backend/app/cache/TC-01.json',
    isExecutable: true,
  },
  {
    id: 'TC-02',
    name: 'Known Attack — Exploits',
    description: 'Demonstrates high-confidence supervised XGBoost detection on real network exploit flows.',
    category: 'Supervised Detection',
    primaryCapability: 'KNOWN ATTACK RECALL',
    status: 'VERIFIED',
    statusReason: 'Verified 100% detection recall (297/297 in test split) on Exploit flow signatures using frozen production XGBoost.',
    sourceDataset: 'NF-UNSW-NB15-v2',
    underlyingArtifact: 'backend/app/cache/TC-02.json',
    isExecutable: true,
  },
  {
    id: 'TC-03',
    name: 'Known Attack — Generic / DoS',
    description: 'Tests volumetric and protocol-based attack patterns with supervised signature matching.',
    category: 'Supervised Detection',
    primaryCapability: 'DOS / VOLUMETRIC RECALL',
    status: 'VERIFIED',
    statusReason: 'Verified 100% detection on DoS (54/54) and Generic (156/156) in test split with T1498/T1499 MITRE mapping.',
    sourceDataset: 'NF-UNSW-NB15-v2',
    underlyingArtifact: 'backend/app/cache/TC-03.json',
    isExecutable: true,
  },
  {
    id: 'TC-04',
    name: 'Isolation Forest Anomaly Example',
    description: 'Demonstrates unsupervised behavioral outlier detection flagging abnormal statistical features.',
    category: 'Anomaly Detection',
    primaryCapability: 'BEHAVIORAL OUTLIER',
    status: 'VERIFIED',
    statusReason: 'Verified unsupervised behavioral outlier detection using frozen models/isolation_forest.joblib (threshold 0.0094).',
    sourceDataset: 'NF-UNSW-NB15-v2',
    underlyingArtifact: 'backend/app/cache/TC-04.json',
    isExecutable: true,
  },
  {
    id: 'TC-05',
    name: 'Autoencoder Anomaly Example',
    description: 'Reconstruction error anomaly detection benchmark comparing against tree-based isolation.',
    category: 'Anomaly Detection',
    primaryCapability: 'DEEP RECONSTRUCTION ERROR',
    status: 'EXPERIMENTAL ARTIFACT PRESENT',
    statusReason: 'Disabled: Neural network weights do not exist on disk for live inference. Benchmark comparison recorded in experiments/anomaly_benchmark/.',
    sourceDataset: 'NF-UNSW-NB15-v2',
    underlyingArtifact: 'experiments/anomaly_benchmark/comparison.json',
    isExecutable: false,
  },
  {
    id: 'TC-06',
    name: 'Detector Agreement (Supervised + Anomaly)',
    category: 'Consensus Detection',
    description: 'Consensus scenario where both supervised XGBoost and unsupervised Isolation Forest trigger positive.',
    primaryCapability: 'DUAL-ENGINE AGREEMENT',
    status: 'VERIFIED',
    statusReason: 'Verified dual-positive consensus (533 flows in test split) with high-confidence agreement and correlation edges.',
    sourceDataset: 'NF-UNSW-NB15-v2',
    underlyingArtifact: 'backend/app/cache/TC-06.json',
    isExecutable: true,
  },
  {
    id: 'TC-07',
    name: 'Detector Disagreement',
    description: 'Edge-case scenario evaluating divergence between supervised classifier and anomaly detector.',
    category: 'Triage / Boundary',
    primaryCapability: 'DISCREPANCY RESOLUTION',
    status: 'VERIFIED',
    statusReason: 'Verified model divergence (443 XGB-only and 1,442 IF-only flows in test split) highlighting defense-in-depth complementarity.',
    sourceDataset: 'NF-UNSW-NB15-v2',
    underlyingArtifact: 'backend/app/cache/TC-07.json',
    isExecutable: true,
  },
  {
    id: 'TC-08',
    name: 'Held-Out Fuzzers Evaluation',
    description: 'Zero-shot generalization test evaluating an XGBoost model trained with the entire Fuzzers family excluded.',
    category: 'Generalization',
    primaryCapability: 'HOLDOUT FAMILY GENERALIZATION',
    status: 'VERIFIED',
    statusReason: 'Recorded experiment: Model trained with 0 Fuzzers samples achieves 68.64% zero-shot recall on 30,207 test support flows (1,400 Fuzzers).',
    sourceDataset: 'NF-UNSW-NB15-v2 (Zero-Shot Fuzzers Holdout)',
    underlyingArtifact: 'backend/app/cache/TC-08.json',
    isExecutable: true,
  },
  {
    id: 'TC-09',
    name: 'Held-Out Reconnaissance Evaluation',
    description: 'Zero-shot generalization test evaluating an XGBoost model trained with Reconnaissance completely held out.',
    category: 'Generalization',
    primaryCapability: 'HOLDOUT FAMILY GENERALIZATION',
    status: 'VERIFIED',
    statusReason: 'Recorded experiment: Model trained with 0 Reconnaissance samples achieves 100.0% zero-shot recall on 29,609 test support flows.',
    sourceDataset: 'NF-UNSW-NB15-v2 (Zero-Shot Reconnaissance Holdout)',
    underlyingArtifact: 'backend/app/cache/TC-09.json',
    isExecutable: true,
  },
  {
    id: 'TC-10',
    name: 'Controlled Multi-Stage APT Replay',
    description: 'End-to-end controlled incident replay demonstrating correlation, graph reconstruction, MITRE mapping and AI explanation.',
    category: 'End-to-End Campaign',
    primaryCapability: 'FULL MULTI-STAGE RECONSTRUCTION',
    status: 'VERIFIED',
    statusReason: 'Fully verified in backend/app/cache/TC-10.json with 8 attack events, 1 isolated noise event, 20 graph edges, and passing unit tests.',
    sourceDataset: 'Controlled Topology Replay',
    underlyingArtifact: 'backend/app/cache/TC-10.json',
    isExecutable: true,
  },
];
