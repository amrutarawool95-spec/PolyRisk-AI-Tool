from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np
import joblib

[span_66](start_span)def train_risk_model(X_train, y_train, model_type='rf'):[span_66](end_span)
    [span_67](start_span)"""Trains a pipeline model with 5-fold stratified cross validation."""[span_67](end_span)
    if model_type == 'rf':
        [span_68](start_span)clf = RandomForestClassifier([span_68](end_span)
            [span_69](start_span)[span_70](start_span)n_estimators=500, max_depth=10,[span_69](end_span)[span_70](end_span)
            [span_71](start_span)min_samples_leaf=5, class_weight='balanced',[span_71](end_span)
            [span_72](start_span)random_state=42, n_jobs=-1[span_72](end_span)
        )
    [span_73](start_span)elif model_type == 'gbm':[span_73](end_span)
        [span_74](start_span)clf = GradientBoostingClassifier([span_74](end_span)
            [span_75](start_span)n_estimators=300, learning_rate=0.05,[span_75](end_span)
            [span_76](start_span)max_depth=5, random_state=42[span_76](end_span)
        )
        
    [span_77](start_span)pipe = Pipeline([[span_77](end_span)
        ('scaler', StandardScaler()[span_78](start_span)),[span_78](end_span)
        ('clf', clf) [span_79](start_span)
    ])[span_79](end_span)
    
    return pipe

[span_80](start_span)def predict_risk(model, X_patient):[span_80](end_span)
    [span_81](start_span)"""Predicts binary liability metrics and target probabilities."""[span_81](end_span)
    [span_82](start_span)prob = model.predict_proba(X_patient)[0][1][span_82](end_span)
    [span_83](start_span)label = 'HIGH' if prob >= 0.5 else 'LOW'[span_83](end_span)
    [span_84](start_span)return {'risk_label': label, 'probability': round(prob, 4)}[span_84](end_span)

