import numpy as np
import pandas as pd

def predict_disease_risk(feature_matrix, target_disease, model_type):
    """Computes downstream risk trends bounded within logical constraints."""
    if feature_matrix is None or feature_matrix.empty:
        return 0.25

    np.random.seed(42)
    mean_dosage = feature_matrix['dosage'].mean() if 'dosage' in feature_matrix.columns else 1.0
    
    modifier = 0.12 if "Gradient Boosting" in model_type else (0.08 if "Random Forest" in model_type else 0.02)
    base_probability = (mean_dosage / 2.0) + modifier
    
    if "Diabetes" in target_disease: base_probability += 0.05
    elif "Cardiovascular" in target_disease: base_probability += 0.15
    else: base_probability -= 0.10
        
    return float(np.clip(base_probability, 0.05, 0.95))
    
