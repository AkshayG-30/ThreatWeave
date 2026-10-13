import sys
sys.path.append('backend')
from app.services.pipeline import create_mvp_sample

raw_path = r"D:\Zephyr\ThreatWeave\data\raw\NF-UNSW-NB15-v2\extracted\fe6cb615d161452c_MOHANAD_A4706\data\NF-UNSW-NB15-v2.csv"
out_path = r"D:\Zephyr\ThreatWeave\data\processed\nf_unsw_nb15_v2_sample_150k"

print("Creating sample...")
sample_df = create_mvp_sample(raw_path, out_path, 150000)
print(f"Sample created with {len(sample_df)} rows.")
print(sample_df['Attack'].value_counts())
