import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any
import uuid
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from app.schemas.event import CanonicalEvent

class DataPipeline:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.features_to_scale = []
        self.categorical_features = []
        
        # Identifiers to drop for ML
        self.drop_for_ml = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR']
        # Targets
        self.targets = ['Label', 'Attack']
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Loads raw dataset."""
        return pd.read_csv(filepath)
        
    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Validates that the dataframe contains expected targets and basic columns."""
        required = self.drop_for_ml + self.targets
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        return True

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fills or drops missing values."""
        # For NF-UNSW-NB15-v2, no NaNs usually, but safe to dropna
        return df.dropna().copy()
        
    def select_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Separates features and targets, and drops ML-forbidden identifiers."""
        X = df.drop(columns=self.drop_for_ml + self.targets, errors='ignore')
        y_label = df['Label'] if 'Label' in df.columns else None
        y_attack = df['Attack'] if 'Attack' in df.columns else None
        return X, y_label, y_attack
        
    def numeric_conversion(self, df: pd.DataFrame) -> pd.DataFrame:
        """Converts columns to numeric, coerces errors."""
        df_num = df.copy()
        for col in df_num.columns:
            if df_num[col].dtype == 'object':
                try:
                    df_num[col] = pd.to_numeric(df_num[col])
                except ValueError:
                    pass # Keep object if truly categorical
        return df_num

    def normalize(self, df: pd.DataFrame, is_train: bool = True) -> pd.DataFrame:
        """Normalizes numeric features. Fits only on train to prevent leakage."""
        df_norm = df.copy()
        
        if is_train:
            self.features_to_scale = df_norm.select_dtypes(include=[np.number]).columns.tolist()
            df_norm[self.features_to_scale] = self.scaler.fit_transform(df_norm[self.features_to_scale])
        else:
            if self.features_to_scale:
                df_norm[self.features_to_scale] = self.scaler.transform(df_norm[self.features_to_scale])
                
        # Handle any created NaNs or Infs from scaling zero variance cols
        df_norm = df_norm.replace([np.inf, -np.inf], np.nan).fillna(0)
        return df_norm

    def split_data(self, df: pd.DataFrame, stratify_col: str = 'Attack') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Splits into 70/15/15 train/val/test."""
        # 70% Train, 30% Temp
        train_df, temp_df = train_test_split(
            df, test_size=0.3, stratify=df[stratify_col], random_state=self.random_state
        )
        # Split Temp into 15% Val and 15% Test
        val_df, test_df = train_test_split(
            temp_df, test_size=0.5, stratify=temp_df[stratify_col], random_state=self.random_state
        )
        return train_df, val_df, test_df

    def process_to_canonical(self, df: pd.DataFrame) -> List[CanonicalEvent]:
        """Maps dataset row to CanonicalEvent schema without fabricating."""
        events = []
        for _, row in df.iterrows():
            event = CanonicalEvent(
                event_id=str(uuid.uuid4()),
                timestamp=0.0, # Not fabricated, placeholder for required float
                source_ip=str(row.get('IPV4_SRC_ADDR')),
                destination_ip=str(row.get('IPV4_DST_ADDR')),
                source_port=int(row.get('L4_SRC_PORT', 0)),
                destination_port=int(row.get('L4_DST_PORT', 0)),
                protocol=str(row.get('PROTOCOL', '')),
                host=None,
                user=None,
                process=None,
                event_type="netflow",
                label=int(row.get('Label', 0)),
                attack_type=str(row.get('Attack', 'Benign'))
            )
            events.append(event)
        return events

def create_mvp_sample(raw_path: str, output_path: str, sample_size: int = 150000):
    """Creates a stratified MVP sample and saves to disk."""
    df = pd.read_csv(raw_path)
    
    if len(df) <= sample_size:
        sample_df = df
    else:
        # Stratify by attack to maintain class representation
        sample_df, _ = train_test_split(df, train_size=sample_size, stratify=df['Attack'], random_state=42)
        
    try:
        sample_df.to_parquet(output_path + ".parquet", index=False)
    except ImportError:
        sample_df.to_csv(output_path + ".csv", index=False)
        
    return sample_df
