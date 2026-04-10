import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score, f1_score, mean_squared_error
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor
import joblib
import streamlit as st

def train_model(df, target, features, task_type, model_name):
    """Simple wrapper for training models."""
    X = df[features]
    y = df[target]
    
    # Preprocessing: Fill nulls with median/mode (simplified for now)
    X = X.fillna(X.median(numeric_only=True))
    if y.dtype == 'object':
        y = pd.get_dummies(y, drop_first=True)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    if task_type == "Classification":
        if model_name == "Random Forest":
            model = RandomForestClassifier()
        elif model_name == "XGBoost":
            model = XGBClassifier()
        else:
            model = RandomForestClassifier()
            
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = {
            "Accuracy": accuracy_score(y_test, y_pred),
            "F1": f1_score(y_test, y_pred, average='weighted')
        }
    else:
        if model_name == "Random Forest":
            model = RandomForestRegressor()
        elif model_name == "XGBoost":
            model = XGBRegressor()
        else:
            model = RandomForestRegressor()
            
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = {
            "R2": r2_score(y_test, y_pred),
            "MSE": mean_squared_error(y_test, y_pred)
        }
        
    return model, metrics

def save_model(model, filename):
    joblib.dump(model, filename)
