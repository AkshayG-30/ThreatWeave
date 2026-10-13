# Phase 2 Dataset Report

## 1. Dataset Source
The primary dataset used is **NF-UNSW-NB15-v2**. This is the 43-feature NetFlow-based standardization of the UNSW-NB15 dataset, sourced from the UQ eSpace repository (Research Data Management, University of Queensland).

## 2. Actual Downloaded File
The downloaded file is a Zip archive named `fe6cb615d161452c_MOHANAD_A4706.zip`. Upon extraction, it provided the primary raw dataset file:
`data/raw/NF-UNSW-NB15-v2/extracted/fe6cb615d161452c_MOHANAD_A4706/data/NF-UNSW-NB15-v2.csv`

## 3. Dataset Size
- **File size**: 421.40 MB
- **Total rows**: 2,390,275

## 4. Features
The dataset contains 45 columns. The feature set comprises network flow metrics including ports, IP addresses, bytes, packets, durations, and TCP flags (e.g., `L4_SRC_PORT`, `IN_BYTES`, `TCP_FLAGS`, `FLOW_DURATION_MILLISECONDS`).

## 5. Labels
The target columns are:
- `Label` (Binary classification: 0 for Benign, 1 for Attack)
- `Attack` (Multiclass classification: Benign or one of 9 attack families)

## 6. Class Distribution (Raw)
The dataset is heavily imbalanced:
- **Benign**: 2,295,222
- **Attacks**: 95,053 (Exploits, Fuzzers, Generic, Reconnaissance, DoS, Analysis, Backdoor, Shellcode, Worms).

## 7. Missing Values
Profiling across the entire 2.39M row dataset confirmed there are exactly **0** missing values (NaN) in all 45 columns.

## 8. Leakage Risks
The `IPV4_SRC_ADDR` and `IPV4_DST_ADDR` identifier columns introduce a significant risk of spatial data leakage (the model might learn to block specific IPs from the lab environment rather than identifying anomalous behavior). These have been formally restricted in `data/metadata/feature_policy.md` and are systematically dropped by the preprocessing pipeline before training.

## 9. Canonical Mapping
Fields mapped without fabrication:
- `source_ip` (from `IPV4_SRC_ADDR`)
- `destination_ip` (from `IPV4_DST_ADDR`)
- `source_port` (from `L4_SRC_PORT`)
- `destination_port` (from `L4_DST_PORT`)
- `protocol` (from `PROTOCOL`)
- `label` (from `Label`)
- `attack_type` (from `Attack`)

**Note**: `timestamp`, `host`, `user`, and `process` do not exist in this dataset and are strictly set to `NULL`/`None`.

## 10. Sampling Strategy
To produce a manageable MVP subset, a **Stratified Sample of 150,000 rows** was generated using `sklearn.model_selection.train_test_split` with a fixed `random_state=42`, stratifying on the `Attack` column to ensure all minority classes (such as Worms, Shellcode, Backdoors) are preserved proportionally. 

## 11. Split Strategy
The 150,000-row sample will be processed using a standard **70% / 15% / 15%** (Train / Validation / Test) split. 
- The split is applied *prior* to numerical scaling.
- The `StandardScaler` is strictly fit on the Training subset to prevent temporal data leakage.

## 12. Processed Sample
The final stratified sample has been successfully created with exactly 150,000 rows and saved in the efficient Parquet format at `data/processed/nf_unsw_nb15_v2_sample_150k.parquet`. The sample includes:
- 144,035 Benign records
- 5,965 Attack records distributed across all 9 classes.

## 13. Limitations
1. The absence of timestamps restricts true temporal analysis or time-based splitting.
2. High class imbalance remains in the MVP sample (consistent with the real world, but potentially challenging for baseline models).
