import numpy as np
import pandas as pd

def calculate_prs_score(feature_matrix, target_disease):
    """
    Calculates the Polygenic Risk Score (PRS) based on risk allele dosage weights
    and maps the absolute score to a relative population percentile curve.
    """
    # Safeguard if the incoming feature matrix is empty or None
    if feature_matrix is None or feature_matrix.empty:
        return 0.0, 50
        
    # 1. Compute a simulated raw Polygenic Risk Score
    # Real PRS sums up (Log-Odds of Risk Allele * Allele Dosage) across target SNPs
    np.random.seed(101)  # Keeps results stable across refreshes
    
    # Generate mock allele weights corresponding to the selected target disease
    num_variants = len(feature_matrix) if len(feature_matrix) > 0 else 10
    mock_gwas_weights = np.random.uniform(0.05, 0.45, size=num_variants)
    
    # Take dosage from dataframe if available, otherwise default to a standard array
    dosage_values = feature_matrix['dosage'].values if 'dosage' in feature_matrix.columns else np.random.randint(0, 3, size=num_variants)
    
    # Math calculation: Dot product of variant weights and variant dosages
    raw_prs = np.dot(mock_gwas_weights[:len(dosage_values)], dosage_values)
    
    # 2. Map the raw score to a normal population distribution curve
    # This derives where this individual falls relative to a global cohort
    if "Diabetes" in target_disease:
        mean, std_dev = 2.5, 0.8
    elif "Cardiovascular" in target_disease:
        mean, std_dev = 3.0, 1.1
    else:  # Alzheimer's Disease
        mean, std_dev = 1.8, 0.6
        
    # Calculate a standard Z-score
    z_score = (raw_prs - mean) / std_dev if std_dev > 0 else 0
    
    # Translate Z-score into a clean percentile integer (bounded between 1 and 99)
    from scipy.stats import norm
    percentile = int(norm.cdf(z_score) * 100)
    percentile = max(1, min(99, percentile))
    
    return float(raw_prs), percentile
    
