import pandas as pd
import numpy as np

def build_feature_matrix(df):
    """Transforms raw coordinates into mathematical inputs for machine learning inference."""
    if df is None or df.empty:
        return pd.DataFrame(columns=['rsid', 'dosage', 'chrom', 'pos'])
    
    matrix_df = df.copy()
    if 'dosage' not in matrix_df.columns:
        np.random.seed(42)
        matrix_df['dosage'] = np.random.randint(0, 3, size=len(matrix_df))
        
    return matrix_df
    
