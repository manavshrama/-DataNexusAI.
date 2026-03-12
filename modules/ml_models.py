import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, silhouette_score
import plotly.express as px
import plotly.graph_objects as go

# Classification
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis

# Regression
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, HuberRegressor, BayesianRidge, SGDRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNNRegressor

# Clustering
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, MeanShift, Birch
from sklearn.mixture import GaussianMixture

class MLModule:
    """Machine Learning module for Classification, Regression, Clustering, and AutoML."""
    
    def __init__(self):
        self.classification_models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(),
            "AdaBoost": AdaBoostClassifier(),
            "Extra Trees": ExtraTreesClassifier(),
            "Bagging": BaggingClassifier(),
            "SVM (RBF kernel)": SVC(probability=True),
            "K-Nearest Neighbors": KNeighborsClassifier(),
            "Naive Bayes": GaussianNB(),
            "LDA": LinearDiscriminantAnalysis(),
            "QDA": QuadraticDiscriminantAnalysis(),
            "SGD Classifier": SGDClassifier()
        }
        
        self.regression_models = {
            "Linear Regression": LinearRegression(),
            "Ridge": Ridge(),
            "Lasso": Lasso(),
            "ElasticNet": ElasticNet(),
            "Huber Regressor": HuberRegressor(),
            "Bayesian Ridge": BayesianRidge(),
            "Decision Tree Regressor": DecisionTreeRegressor(),
            "Random Forest Regressor": RandomForestRegressor(),
            "Gradient Boosting Regressor": GradientBoostingRegressor(),
            "AdaBoost Regressor": AdaBoostRegressor(),
            "Extra Trees Regressor": ExtraTreesRegressor(),
            "SVR": SVR(),
            "KNN Regressor": KNNRegressor(),
            "SGD Regressor": SGDRegressor()
        }
        
        self.clustering_models = {
            "KMeans": KMeans,
            "DBSCAN": DBSCAN,
            "Agglomerative Clustering": AgglomerativeClustering,
            "Gaussian Mixture": GaussianMixture,
            "Birch": Birch,
            "MeanShift": MeanShift
        }

    def preprocess(self, df, target, task="classification"):
        """Preprocesses the dataframe for ML tasks."""
        df = df.dropna().copy()
        
        # Encode target if needed
        y = df[target]
        if task == "classification" and y.dtype == object:
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        X = df.drop(columns=[target])
        # Simple encoding for object columns in X
        X = pd.get_dummies(X, drop_first=True)
        
        return X, y

    def train_classification(self, X, y, model_name, test_size=0.2, cv=5):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        model = self.classification_models[model_name]
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        metrics = {
            "Accuracy": accuracy_score(y_test, y_pred),
            "F1 (macro)": f1_score(y_test, y_pred, average='macro'),
            "Precision": precision_score(y_test, y_pred, average='macro'),
            "Recall": recall_score(y_test, y_pred, average='macro'),
        }
        
        if cv > 0:
            scores = cross_val_score(pipeline, X, y, cv=cv)
            metrics["CV Mean"] = scores.mean()
            metrics["CV Std"] = scores.std()
            
        cm = confusion_matrix(y_test, y_pred)
        
        importance = None
        if hasattr(model, 'feature_importances_'):
            importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_}).sort_values(by='Importance', ascending=False)
            
        return metrics, cm, importance

    def train_regression(self, X, y, model_name, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        model = self.regression_models[model_name]
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        metrics = {
            "R² Score": r2_score(y_test, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
            "MAE": mean_absolute_error(y_test, y_pred),
            "MSE": mean_squared_error(y_test, y_pred)
        }
        
        return metrics, y_test, y_pred

    def run_clustering(self, X, model_name, n_clusters=3):
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        if model_name == "KMeans":
            model = KMeans(n_clusters=n_clusters)
        elif model_name == "Gaussian Mixture":
            model = GaussianMixture(n_components=n_clusters)
        else:
            model = self.clustering_models[model_name]()
            
        labels = model.fit_predict(X_scaled)
        
        score = None
        if len(np.unique(labels)) > 1:
            score = silhouette_score(X_scaled, labels)
            
        return labels, score
