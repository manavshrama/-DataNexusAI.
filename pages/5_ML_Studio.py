import streamlit as st
import pandas as pd
import numpy as np
import time
from utils.theme import load_css
from utils.navigation import sidebar_nav
from utils.data_utils import infer_column_types

st.set_page_config(page_title="DataNexusAI - ML Studio", page_icon="⚡", layout="wide")
load_css()
sidebar_nav(4)

st.markdown('<h1 class="gradient-text">ML Studio</h1>', unsafe_allow_html=True)
st.caption("No-code machine learning — select, train, evaluate, predict.")

if st.session_state.get('df') is None:
    st.warning("No dataset loaded. Please upload data first.")
    if st.button("Go to Upload"):
        st.switch_page("pages/3_Upload.py")
    st.stop()

df = st.session_state['df']
numeric_cols, categorical_cols, datetime_cols = infer_column_types(df)

# ── Step 1: Problem Setup ──────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
    <h3><span class="step-badge">1</span> Problem Setup</h3>
</div>
""", unsafe_allow_html=True)

col_setup1, col_setup2 = st.columns(2)

with col_setup1:
    target_col = st.selectbox("Target Column", df.columns, help="The column you want to predict")
    task_type = st.radio("Task Type", ["Classification", "Regression"], horizontal=True)

with col_setup2:
    available_features = [c for c in df.columns if c != target_col]
    feature_cols = st.multiselect("Feature Columns", available_features, default=available_features[:min(5, len(available_features))])

if not feature_cols:
    st.info("Select at least one feature column to continue.")
    st.stop()

# ── Step 2: Preprocessing ──────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
    <h3><span class="step-badge">2</span> Preprocessing Options</h3>
</div>
""", unsafe_allow_html=True)
with st.expander("⚙️ Configure Data Processing", expanded=False):
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        handle_nulls = st.checkbox("Handle Missing Values", value=True)
        scale_features = st.checkbox("Scale Features", value=False)
    with p_col2:
        encode_cats = st.checkbox("Encode Categoricals", value=True)
        test_split = st.slider("Test Set Size (%)", 10, 40, 20)

# ── Step 3: Model Selection ────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
    <h3><span class="step-badge">3</span> Model Selection</h3>
</div>
""", unsafe_allow_html=True)

if task_type == "Classification":
    model_options = ["Logistic Regression", "Random Forest", "XGBoost", "SVM", "KNN"]
else:
    model_options = ["Linear Regression", "Ridge", "Random Forest Regressor", "XGBoost Regressor", "SVR"]

selected_models = st.multiselect("Choose models to train", model_options, default=[model_options[0], model_options[1]])

# ── Step 4: Training & Progress ────────────────────────────────────────
st.markdown("""
<div class="glass-card">
    <h3><span class="step-badge">4</span> Training & Progress</h3>
</div>
""", unsafe_allow_html=True)

if st.button("🚀 Start Training", type="primary", use_container_width=True):
    if not selected_models:
        st.error("Please select at least one model.")
        st.stop()

    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import (accuracy_score, f1_score, r2_score,
                                 mean_squared_error, confusion_matrix, roc_auc_score)
    from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.svm import SVC, SVR
    from sklearn.neighbors import KNeighborsClassifier
    import plotly.express as px
    import plotly.figure_factory as ff

    work_df = df[feature_cols + [target_col]].copy()

    # Preprocessing
    if handle_nulls:
        for c in work_df.select_dtypes(include=[np.number]).columns:
            work_df[c].fillna(work_df[c].median(), inplace=True)
        for c in work_df.select_dtypes(include=['object', 'category']).columns:
            work_df[c].fillna(work_df[c].mode().iloc[0] if not work_df[c].mode().empty else "Unknown", inplace=True)

    # Encode target for classification
    le = None
    if task_type == "Classification" and work_df[target_col].dtype == 'object':
        le = LabelEncoder()
        work_df[target_col] = le.fit_transform(work_df[target_col])

    # Encode categorical features
    if encode_cats:
        cat_feats = [c for c in feature_cols if work_df[c].dtype == 'object']
        work_df = pd.get_dummies(work_df, columns=cat_feats, drop_first=True)
        updated_features = [c for c in work_df.columns if c != target_col]
    else:
        updated_features = feature_cols

    X = work_df[updated_features].select_dtypes(include=[np.number])
    y = work_df[target_col]

    if scale_features:
        scaler = StandardScaler()
        X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split / 100, random_state=42)

    # Model map
    MODEL_MAP = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": None,  # handled below
        "SVM": SVC(probability=True),
        "KNN": KNeighborsClassifier(),
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost Regressor": None,
        "SVR": SVR(),
    }

    # Try importing XGBoost
    try:
        from xgboost import XGBClassifier, XGBRegressor
        MODEL_MAP["XGBoost"] = XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss', random_state=42)
        MODEL_MAP["XGBoost Regressor"] = XGBRegressor(n_estimators=100, random_state=42)
    except ImportError:
        pass

    results = []
    trained = {}

    progress_bar = st.progress(0, text="Preparing...")
    for i, model_name in enumerate(selected_models):
        progress_bar.progress((i) / len(selected_models), text=f"Training {model_name}...")
        model_obj = MODEL_MAP.get(model_name)
        if model_obj is None:
            st.warning(f"Skipping {model_name} (not available).")
            continue

        t0 = time.time()
        model_obj.fit(X_train, y_train)
        train_time = round(time.time() - t0, 2)
        y_pred = model_obj.predict(X_test)

        row = {"Model": model_name, "Train Time (s)": train_time}
        if task_type == "Classification":
            row["Accuracy"] = round(accuracy_score(y_test, y_pred), 4)
            row["F1 Score"] = round(f1_score(y_test, y_pred, average='weighted'), 4)
            try:
                if hasattr(model_obj, "predict_proba"):
                    y_proba = model_obj.predict_proba(X_test)
                    if y_proba.shape[1] == 2:
                        row["ROC-AUC"] = round(roc_auc_score(y_test, y_proba[:, 1]), 4)
                    else:
                        row["ROC-AUC"] = round(roc_auc_score(y_test, y_proba, multi_class='ovr', average='weighted'), 4)
            except Exception:
                row["ROC-AUC"] = "N/A"
        else:
            row["R² Score"] = round(r2_score(y_test, y_pred), 4)
            row["MSE"] = round(mean_squared_error(y_test, y_pred), 4)

        results.append(row)
        trained[model_name] = {"model": model_obj, "metrics": row, "y_test": y_test, "y_pred": y_pred}

    progress_bar.progress(1.0, text="Done!")

    st.session_state['trained_models'] = trained
    st.session_state['ml_results'] = results
    st.session_state['ml_features'] = X.columns.tolist()
    st.session_state['ml_target'] = target_col
    st.session_state['ml_task'] = task_type
    st.session_state['ml_le'] = le

    st.success("Training complete!")

# ── Step 5: Results ────────────────────────────────────────────────────
if st.session_state.get('ml_results'):
    st.markdown("""
    <div class="glass-card">
        <h3><span class="step-badge">5</span> Results Comparison</h3>
    </div>
    """, unsafe_allow_html=True)
    
    res_df = pd.DataFrame(st.session_state['ml_results'])

    # Highlight best row
    if st.session_state.get('ml_task') == "Classification":
        best_idx = res_df["Accuracy"].idxmax() if "Accuracy" in res_df.columns else 0
        sort_col = "Accuracy"
    else:
        best_idx = res_df["R² Score"].idxmax() if "R² Score" in res_df.columns else 0
        sort_col = "R² Score"

    st.dataframe(res_df.sort_values(sort_col, ascending=False).style.highlight_max(
        subset=[sort_col], color="rgba(108, 99, 255, 0.3)"
    ), use_container_width=True)

    best_model_name = res_df.loc[best_idx, "Model"]
    st.info(f"🏆 Best model: **{best_model_name}**")

    # ── Step 6: Feature Importance ────────────────────────────────────
    best_model_obj = st.session_state['trained_models'][best_model_name]['model']
    if hasattr(best_model_obj, 'feature_importances_'):
        st.markdown("""
        <div class="glass-card">
            <h3><span class="step-badge">6</span> Feature Importance</h3>
        </div>
        """, unsafe_allow_html=True)
        feat_imp = pd.DataFrame({
            "Feature": st.session_state['ml_features'],
            "Importance": best_model_obj.feature_importances_
        }).sort_values("Importance", ascending=True).tail(15)

        fig = px.bar(feat_imp, x="Importance", y="Feature", orientation='h',
                     color="Importance", color_continuous_scale=["#845EC2", "#00C9A7"])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"), showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Step 7: Live Prediction ───────────────────────────────────────────
if st.session_state.get('trained_models'):
    st.markdown("""
    <div class="glass-card">
        <h3><span class="step-badge">7</span> Live Prediction</h3>
    </div>
    """, unsafe_allow_html=True)

    pred_model_name = st.selectbox("Select model for prediction",
                                    list(st.session_state['trained_models'].keys()))
    pred_model = st.session_state['trained_models'][pred_model_name]['model']

    input_cols = st.columns(min(4, len(st.session_state['ml_features'])))
    input_values = {}
    for i, feat in enumerate(st.session_state['ml_features']):
        with input_cols[i % len(input_cols)]:
            if df[feat].dtype in ['object', 'category'] if feat in df.columns else False:
                input_values[feat] = st.selectbox(f"{feat}", df[feat].unique(), key=f"pred_{feat}")
            else:
                default_val = float(df[feat].median()) if feat in df.columns else 0.0
                input_values[feat] = st.number_input(f"{feat}", value=default_val, key=f"pred_{feat}")

    if st.button("⚡ Predict", type="primary"):
        input_df = pd.DataFrame([input_values])
        try:
            prediction = pred_model.predict(input_df)[0]
            le = st.session_state.get('ml_le')
            if le is not None:
                prediction = le.inverse_transform([int(prediction)])[0]
            st.markdown(f"""
            <div class="prediction-card">
                <h2 class="gradient-text">Prediction Result</h2>
                <p style="font-size: 3rem; font-weight: 700;">{prediction}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
