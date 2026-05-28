import shap
import pandas as pd
import numpy as np

def explain_prediction(model, X_sample: pd.DataFrame, feature_names: list) -> dict:
    """Generates localized variant structural contributions using SHAP TreeExplainer."""
    clf = model.named_steps['clf']
    scaler = model.named_steps['scaler']
    X_scaled = scaler.transform(X_sample)
    
    explainer = shap.TreeExplainer(clf)
    shap_vals = explainer.shap_values(X_scaled)
    
    if isinstance(shap_vals, list):
        sv = shap_vals[1][0]
    elif len(shap_vals.shape) == 3:
        sv = shap_vals[0, :, 1]
    else:
        sv = shap_vals[0] if len(shap_vals.shape) == 1 else shap_vals[0, :]
        
    shap_df = pd.DataFrame({
        'feature': feature_names,
        'shap_value': sv,
        'dosage': X_sample.values[0]
    })
    
    shap_df = shap_df.reindex(shap_df.shap_value.abs().sort_values(ascending=False).index)
    return shap_df.head(10).to_dict('records')
    
