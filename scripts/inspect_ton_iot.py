import os
import json
import pandas as pd
import numpy as np
from pathlib import Path

def get_dtype_str(dt):
    if pd.api.types.is_numeric_dtype(dt): return "numeric"
    return "categorical"

def main():
    EXP_DIR = Path("D:/Zephyr/ThreatWeave/experiments/cross_dataset_toniot")
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    
    TON_PATH = Path("D:/Zephyr/ThreatWeave/data/raw/NF-ToN-IoT.parquet")
    FEATURES_PATH = Path("D:/Zephyr/ThreatWeave/models/feature_columns.json")
    UNSW_PATH = Path("D:/Zephyr/ThreatWeave/data/processed/nf_unsw_nb15_v2_sample_150k.csv")
    
    # 1. Dataset Inspection
    print("Loading NF-ToN-IoT dataset...")
    df_ton = pd.read_parquet(TON_PATH)
    
    num_rows, num_cols = df_ton.shape
    columns = list(df_ton.columns)
    dtypes = {col: str(dt) for col, dt in df_ton.dtypes.items()}
    missing_values = df_ton.isnull().sum().to_dict()
    duplicate_rows = int(df_ton.duplicated().sum())
    
    label_dist = df_ton['Label'].value_counts().to_dict() if 'Label' in df_ton else {}
    attack_dist = df_ton['Attack'].value_counts().to_dict() if 'Attack' in df_ton else {}
    
    categorical_cols = df_ton.select_dtypes(exclude=[np.number]).columns
    numeric_cols = df_ton.select_dtypes(include=[np.number]).columns
    
    cat_uniques = {col: df_ton[col].nunique() for col in categorical_cols if df_ton[col].nunique() < 50}
    num_stats = df_ton[numeric_cols].agg(['min', 'max']).to_dict()
    
    inspection_json = {
        "rows": num_rows,
        "columns": num_cols,
        "column_names": columns,
        "dtypes": dtypes,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "label_distribution": label_dist,
        "attack_distribution": attack_dist,
        "categorical_uniques": cat_uniques,
        "numeric_min_max": num_stats
    }
    
    with open(EXP_DIR / "inspection.json", "w") as f:
        json.dump(inspection_json, f, indent=4)
        
    inspection_md = f"""# NF-ToN-IoT Dataset Inspection Report

## Summary
- **Rows**: {num_rows}
- **Columns**: {num_cols}
- **Duplicate Rows**: {duplicate_rows}

## Column Names
{', '.join(columns)}

## Missing Values
"""
    has_missing = any(v > 0 for v in missing_values.values())
    if not has_missing:
        inspection_md += "No missing values found in any column.\n"
    else:
        for k, v in missing_values.items():
            if v > 0:
                inspection_md += f"- {k}: {v}\n"
                
    inspection_md += "\n## Label Distribution\n"
    for k, v in label_dist.items():
        inspection_md += f"- **{k}**: {v}\n"
        
    inspection_md += "\n## Attack Distribution\n"
    for k, v in attack_dist.items():
        inspection_md += f"- **{k}**: {v}\n"
        
    with open(EXP_DIR / "inspection_report.md", "w") as f:
        f.write(inspection_md)
        
    # 2. Schema Compatibility
    with open(FEATURES_PATH, 'r') as f:
        prod_features = json.load(f)
        
    ton_cols_set = set(columns)
    prod_features_set = set(prod_features)
    
    shared_features = list(ton_cols_set.intersection(prod_features_set))
    missing_features = list(prod_features_set - ton_cols_set)
    extra_features = list(ton_cols_set - prod_features_set)
    
    # Datatypes check for shared features
    dtype_issues = []
    for f in shared_features:
        if not pd.api.types.is_numeric_dtype(df_ton[f]):
            dtype_issues.append(f"{f}: expected numeric, got {df_ton[f].dtype}")
            
    ip_cols = [c for c in extra_features if 'IP' in c.upper() or 'ADDR' in c.upper()]
    label_cols = [c for c in extra_features if 'LABEL' in c.upper()]
    attack_cols = [c for c in extra_features if 'ATTACK' in c.upper()]
    
    if len(missing_features) == 0 and len(dtype_issues) == 0:
        compatibility_status = "VALID FOR DIRECT CROSS-DATASET INFERENCE"
        transform_required = "None. Just feature selection and IP dropping."
    elif len(missing_features) > 0 and len(missing_features) < 5:
        compatibility_status = "REQUIRES CONTROLLED ADAPTER"
        transform_required = f"Requires mapping or imputing {len(missing_features)} missing features."
    else:
        compatibility_status = "NOT COMPATIBLE"
        transform_required = "Too many structural mismatches."
        
    comp_md = f"""# Schema Compatibility Report

## Final Verdict
**{compatibility_status}**

## Details
- **Production Model Expected Features**: {len(prod_features)}
- **Shared Features Present**: {len(shared_features)}
- **Missing Production Features**: {len(missing_features)} ({', '.join(missing_features) if missing_features else 'None'})
- **Extra Features in NF-ToN-IoT**: {len(extra_features)}
- **Datatype Mismatches**: {len(dtype_issues)}

## Specific Columns
- **IP Identifier Columns (to drop)**: {', '.join(ip_cols)}
- **Label/Target Columns**: {', '.join(label_cols)}
- **Attack/Category Columns**: {', '.join(attack_cols)}

## Transformation Required
{transform_required}
"""
    with open(EXP_DIR / "compatibility_report.md", "w") as f:
        f.write(comp_md)
        
    # 3. Leakage Check
    leakage_pass = True
    leakage_notes = []
    
    for pf in prod_features:
        if 'LABEL' in pf.upper() or 'ATTACK' in pf.upper():
            leakage_pass = False
            leakage_notes.append(f"Target column leaked into feature list: {pf}")
        if 'IP' in pf.upper() or 'ADDR' in pf.upper():
            leakage_pass = False
            leakage_notes.append(f"IP Identifier leaked into feature list: {pf}")
            
    if not leakage_pass:
        leakage_status = "FAIL"
    else:
        leakage_status = "PASS"
        
    with open(EXP_DIR / "leakage_check.txt", "w") as f:
        f.write(f"Leakage Status: {leakage_status}\n")
        for n in leakage_notes: f.write(f"- {n}\n")
        f.write(f"\nFinal Verified Production Feature List ({len(prod_features)}):\n{', '.join(prod_features)}\n")
        
    # 4. Distribution Check
    print("Performing Distribution Check...")
    if UNSW_PATH.exists():
        df_unsw = pd.read_csv(UNSW_PATH)
        
        dist_md = "# Distribution Shift Analysis\n\n"
        dist_md += "| Feature | UNSW Mean | ToN Mean | UNSW Std | ToN Std | Shift Observed |\n"
        dist_md += "|---|---|---|---|---|---|\n"
        
        for f in shared_features:
            if f in df_unsw.columns and pd.api.types.is_numeric_dtype(df_ton[f]):
                u_mean, t_mean = df_unsw[f].mean(), df_ton[f].mean()
                u_std, t_std = df_unsw[f].std(), df_ton[f].std()
                
                # Simple shift heuristic
                shift = "HIGH" if abs(u_mean - t_mean) > (u_std + t_std)/2 else "LOW"
                dist_md += f"| {f} | {u_mean:.2f} | {t_mean:.2f} | {u_std:.2f} | {t_std:.2f} | {shift} |\n"
                
        with open(EXP_DIR / "distribution_report.md", "w") as f:
            f.write(dist_md)
            
    print("Done. No inference was executed.")

if __name__ == "__main__":
    main()
