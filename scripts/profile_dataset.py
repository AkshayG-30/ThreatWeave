import pandas as pd
import json
import os
from pathlib import Path

file_path = Path(r"D:\Zephyr\ThreatWeave\data\raw\NF-UNSW-NB15-v2\extracted\fe6cb615d161452c_MOHANAD_A4706\data\NF-UNSW-NB15-v2.csv")

file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

# Initialize profiling metrics
row_count = 0
missing_values = {}
label_distribution = {}
attack_distribution = {}

# We'll peek at the first chunk to get columns and dtypes
chunk_iter = pd.read_csv(file_path, chunksize=100000)
first_chunk = next(chunk_iter)
columns = list(first_chunk.columns)
dtypes = {k: str(v) for k, v in first_chunk.dtypes.items()}

# Reset iterator for full pass
chunk_iter = pd.read_csv(file_path, chunksize=100000)

for chunk in chunk_iter:
    row_count += len(chunk)
    
    # Missing values
    na_counts = chunk.isna().sum()
    for col, count in na_counts.items():
        missing_values[col] = missing_values.get(col, 0) + count
        
    # Class distributions
    if 'Label' in chunk.columns:
        for val, count in chunk['Label'].value_counts().items():
            label_distribution[str(val)] = label_distribution.get(str(val), 0) + count
            
    if 'Attack' in chunk.columns:
        for val, count in chunk['Attack'].value_counts().items():
            attack_distribution[str(val)] = attack_distribution.get(str(val), 0) + count

# Format the results
profile_dict = {
    "file_name": file_path.name,
    "file_size_mb": round(file_size_mb, 2),
    "row_count": row_count,
    "column_count": len(columns),
    "columns": columns,
    "dtypes": dtypes,
    "missing_values": missing_values,
    "label_distribution": label_distribution,
    "attack_distribution": attack_distribution
}

# Write JSON
out_json = Path(r"D:\Zephyr\ThreatWeave\data\metadata\nf_unsw_nb15_v2_profile.json")
out_json.parent.mkdir(parents=True, exist_ok=True)
with open(out_json, "w") as f:
    json.dump(profile_dict, f, indent=4)

# Write MD
md_content = f"""# NF-UNSW-NB15-v2 Dataset Profile

- **File**: {file_path.name}
- **Size**: {file_size_mb:.2f} MB
- **Rows**: {row_count}
- **Columns**: {len(columns)}

## Columns and Types
"""
for col in columns:
    md_content += f"- `{col}` ({dtypes[col]}): {missing_values.get(col, 0)} missing values\n"

md_content += "\n## Label Distribution\n"
for k, v in label_distribution.items():
    md_content += f"- {k}: {v}\n"
    
md_content += "\n## Attack Categories\n"
for k, v in attack_distribution.items():
    md_content += f"- {k}: {v}\n"

out_md = Path(r"D:\Zephyr\ThreatWeave\data\metadata\nf_unsw_nb15_v2_profile.md")
with open(out_md, "w") as f:
    f.write(md_content)

print("Profiling complete. Outputs saved to data/metadata.")
