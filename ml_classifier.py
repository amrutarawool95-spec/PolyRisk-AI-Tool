from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np
import joblib

def train_risk_model(X_train, y_train, model_type='rf'):
    """Trains a pipeline model with 5-fold stratified cross validation."""
    if model_type == 'rf':
        clf = RandomForestClassifier(
            n_estimators=500, max_depth=10,
            min_samples_leaf=5, class_weight='balanced',
            random_state=42, n_jobs=-1
        )
    elif model_type == 'gbm':
        clf = GradientBoostingClassifier(
            n_estimators=300, learning_rate=0.05,
            max_depth=5, random_state=42
        )
        
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', clf)
    ])
    
    return pipe

def predict_risk(model, X_patient):
    """Predicts binary liability metrics and target probabilities."""
    prob = model.predict_proba(X_patient)[0][1]
    label = 'HIGH' if prob >= 0.5 else 'LOW'
    return {'risk_label': label, 'probability': round(prob, 4)}
    
