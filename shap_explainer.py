import shap
import pandas as pd
import numpy as np

[span_87](start_span)def explain_prediction(model, X_sample: pd.DataFrame, feature_names: list) -> dict:[span_87](end_span)
    [span_88](start_span)"""Generates localized variant structural contributions using SHAP TreeExplainer."""[span_88](end_span)
    [span_89](start_span)clf = model.named_steps['clf'][span_89](end_span)
    [span_90](start_span)scaler = model.named_steps['scaler'][span_90](end_span)
    [span_91](start_span)X_scaled = scaler.transform(X_sample)[span_91](end_span)
    
    [span_92](start_span)explainer = shap.TreeExplainer(clf)[span_92](end_span)
    [span_93](start_span)shap_vals = explainer.shap_values(X_scaled)[span_93](end_span)
    
    # Handle both binary list formats and raw multi-arrays safely
    if isinstance(shap_vals, list):
        [span_94](start_span)sv = shap_vals[1][0][span_94](end_span)
    elif len(shap_vals.shape) == 3:
        sv = shap_vals[0, :, 1]
    else:
        [span_95](start_span)sv = shap_vals[0] if len(shap_vals.shape) == 1 else shap_vals[0, :][span_95](end_span)
        
    shap_df = pd.DataFrame({
        [span_96](start_span)'feature': feature_names,[span_96](end_span)
        [span_97](start_span)'shap_value': sv,[span_97](end_span)
        [span_98](start_span)'dosage': X_sample.values[0][span_98](end_span)
    })
    
    # [span_99](start_span)Sort by absolute impact[span_99](end_span)
    [span_100](start_span)shap_df = shap_df.reindex(shap_df.shap_value.abs().sort_values(ascending=False).index)[span_100](end_span)
    [span_101](start_span)return shap_df.head(10).to_dict('records')[span_101](end_span)

