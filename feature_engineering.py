import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

[span_42](start_span)def build_feature_matrix(dosage_matrix: pd.DataFrame, n_pcs: int = 10) -> pd.DataFrame:[span_42](end_span)
    [span_43](start_span)"""Applies standard scaling and adds top-N ancestry PCs to the dosage data."""[span_43](end_span)
    [span_44](start_span)X = dosage_matrix.fillna(dosage_matrix.mean())[span_44](end_span)
    [span_45](start_span)scaler = StandardScaler()[span_45](end_span)
    [span_46](start_span)X_scaled = scaler.fit_transform(X)[span_46](end_span)
    
    [span_47](start_span)pca = PCA(n_components=n_pcs, random_state=42)[span_47](end_span)
    [span_48](start_span)pcs = pca.fit_transform(X_scaled)[span_48](end_span)
    
    pc_df = pd.DataFrame(
        pcs, 
        [span_49](start_span)columns=[f'PC{i+1}' for i in range(n_pcs)],[span_49](end_span)
        index=dosage_matrix.index
    [span_50](start_span))
    
    return pd.concat([dosage_matrix, pc_df], axis=1)[span_50](end_span)

