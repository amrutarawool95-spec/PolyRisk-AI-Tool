import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def build_feature_matrix(dosage_matrix: pd.DataFrame, n_pcs: int = 10) -> pd.DataFrame:
    """Applies standard scaling and adds top-N ancestry PCs to the dosage data."""
    X = dosage_matrix.fillna(dosage_matrix.mean())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=n_pcs, random_state=42)
    pcs = pca.fit_transform(X_scaled)
    
    pc_df = pd.DataFrame(
        pcs, 
        columns=[f'PC{i+1}' for i in range(n_pcs)],
        index=dosage_matrix.index
    )
    
    return pd.concat([dosage_matrix, pc_df], axis=1)
    
