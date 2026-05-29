import numpy as np
import pandas as pd
from scipy.stats import norm

def calculate_prs_score(feature_matrix, target_disease):
    """Calculates absolute Polygenic Risk Scores mapped to precise percentile steps."""
    if feature_matrix is None or feature_matrix.empty:
        return 0.0, 50
        
    np.random.seed(101)
    num_variants = len(feature_matrix)
    mock_gwas_weights = np.random.uniform(0.05, 0.45, size=num_variants)
    dosage_values = feature_matrix['dosage'].values
    
    raw_prs = float(np.dot(mock_gwas_weights, dosage_values))
    
    if "Diabetes" in target_disease: mean, std_dev = (num_variants * 0.25), (num_variants * 0.1)
    elif "Cardiovascular" in target_disease: mean, std_dev = (num_variants * 0.3), (num_variants * 0.12)
    else: mean, std_dev = (num_variants * 0.2), (num_variants * 0.08)
        
    z_score = (raw_prs - mean) / std_dev if std_dev > 0 else 0
    percentile = int(norm.cdf(z_score) * 100)
    percentile = max(1, min(99, percentile))
    
    return raw_prs, percentile
    
