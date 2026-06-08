import streamlit as st
import pandas as pd
import numpy as np
import time
from utils.theme import load_css, glass_card, render_hero
from components.sidebar_ui import render_sidebar
from utils.data_utils import infer_column_types

st.set_page_config(page_title="DataNexusAI - ML Studio", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
load_css()
render_sidebar()

render_hero("ML Studio", "Configure, train, and monitor your model in one workflow")

if st.session_state.get('df') is None:
    st.warning("No dataset detected in the nexus. Please upload data first.")
    if st.button("Go to Upload"):
        st.switch_page("pages/3_Upload.py")
    st.stop()

df = st.session_state['df']
numeric_cols, categorical_cols, datetime_cols = infer_column_types(df)

# ── Step 1: Problem Architecture ──────────────────────────────────────────────
st.markdown("### 🛠️ 1. Problem Architecture")
with st.container(border=True):
    col_setup1, col_setup2 = st.columns(2)
    with col_setup1:
        target_col = st.selectbox("Target Node (Prediction Goal)", df.columns, help="The column you want to predict")
        task_type = st.radio("Logic Mode", ["Classification", "Regression"], horizontal=True)
    with col_setup2:
        available_features = [c for c in df.columns if c != target_col]
        feature_cols = st.multiselect("Input Vectors (Features)", available_features, default=available_features[:min(5, len(available_features))])

if not feature_cols:
    st.info("Assign at least one input vector to continue.")
    st.stop()

# ── Step 2: Processing Matrix ──────────────────────────────────────────────
st.markdown("### ⚙️ 2. Processing Matrix")
with st.expander("Configure Neural Preprocessing", expanded=False):
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        handle_nulls = st.checkbox("Auto-Impute Missing Values", value=True)
        scale_features = st.checkbox("Standardize/Scale Features", value=False)
    with p_col2:
        encode_cats = st.checkbox("Neural Categorical Encoding", value=True)
        test_split = st.slider("Validation Split Size (%)", 10, 40, 20)

# ── Step 3: Model Selection ────────────────────────────────────────────
st.markdown("### 🧬 3. Algorithm Selection")
if task_type == "Classification":
    model_options = ["Logistic Regression", "Random Forest", "XGBoost", "SVM", "KNN"]
else:
    model_options = ["Linear Regression", "Ridge", "Random Forest Regressor", "XGBoost Regressor", "SVR"]

selected_models = st.multiselect("Select Algorithms to Forge", model_options, default=[model_options[0]])

# ── Step 4: Forge Execution ────────────────────────────────────────────
st.markdown("### 🚀 4. Forge Execution")
if st.button("Initiate Forge", use_container_width=True):
    if not selected_models:
        st.error("Select at least one algorithm for training.")
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

    work_df = df[feature_cols + [target_col]].copy()

    # Preprocessing logic
    if handle_nulls:
        for c in work_df.select_dtypes(include=[np.number]).columns:
            work_df[c] = work_df[c].fillna(work_df[c].median())
        for c in work_df.select_dtypes(include=['object', 'category']).columns:
            fill_val = work_df[c].mode().iloc[0] if not work_df[c].mode().empty else "Unknown"
            work_df[c] = work_df[c].fillna(fill_val)

    le = None
    if task_type == "Classification":
        target_series = work_df[target_col]
        # Check if the target is continuous float
        if pd.api.types.is_float_dtype(target_series):
            non_null_target = target_series.dropna()
            if not np.all(non_null_target == non_null_target.round()):
                st.error(f"❌ **Invalid Logic Mode**: Target column `{target_col}` contains continuous float values. Classification is only valid for discrete classes (integers, strings, categories). Please select **Regression** as the Logic Mode, or choose a discrete target column.")
                st.stop()
            else:
                work_df[target_col] = work_df[target_col].astype(int)
        
        # Encode non-numeric discrete targets
        if isinstance(work_df[target_col].dtype, pd.CategoricalDtype) or \
           work_df[target_col].dtype in ['object', 'category', 'bool'] or \
           not pd.api.types.is_numeric_dtype(work_df[target_col]):
            le = LabelEncoder()
            work_df[target_col] = le.fit_transform(work_df[target_col].astype(str))

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

    MODEL_MAP = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": None,
        "SVM": SVC(probability=True),
        "KNN": KNeighborsClassifier(),
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost Regressor": None,
        "SVR": SVR(),
    }

    try:
        from xgboost import XGBClassifier, XGBRegressor
        MODEL_MAP["XGBoost"] = XGBClassifier(n_estimators=100, eval_metric='logloss', random_state=42)
        MODEL_MAP["XGBoost Regressor"] = XGBRegressor(n_estimators=100, random_state=42)
    except: pass

    results, trained = [], {}
    progress_bar = st.progress(0, text="Initiating Forge...")

    for i, model_name in enumerate(selected_models):
        progress_bar.progress((i) / len(selected_models), text=f"Forging {model_name}...")
        model_obj = MODEL_MAP.get(model_name)
        if not model_obj: continue

        t0 = time.time()
        model_obj.fit(X_train, y_train)
        y_pred = model_obj.predict(X_test)
        
        row = {"Model": model_name, "Time (s)": round(time.time()-t0, 2)}
        if task_type == "Classification":
            row["Accuracy"] = round(accuracy_score(y_test, y_pred), 4)
            row["F1 Score"] = round(f1_score(y_test, y_pred, average='weighted'), 4)
        else:
            row["R² Score"] = round(r2_score(y_test, y_pred), 4)
            row["MSE"] = round(mean_squared_error(y_test, y_pred), 4)

        results.append(row)
        trained[model_name] = {"model": model_obj, "metrics": row, "y_test": y_test, "y_pred": y_pred}

    progress_bar.progress(1.0, text="Forge Complete!")
    st.session_state.update({'trained_models': trained, 'ml_results': results, 'ml_features': X.columns.tolist(), 'ml_target': target_col, 'ml_task': task_type, 'ml_le': le})
    st.success("Universal Intelligence successfully forged!")

# ── Step 5: Results ────────────────────────────────────────────────────
if st.session_state.get('ml_results'):
    st.write("---")
    st.markdown("### 🏆 5. Forge Leaderboard")
    res_df = pd.DataFrame(st.session_state['ml_results'])
    sort_col = "Accuracy" if st.session_state['ml_task'] == "Classification" else "R² Score"
    
    st.dataframe(res_df.sort_values(sort_col, ascending=False).style.format(precision=4).highlight_max(subset=[sort_col], color="rgba(0, 201, 167, 0.2)"), use_container_width=True)

    # ── Step 6: Feature Importance ────────────────────────────────────
    best_model_name = res_df.loc[res_df[sort_col].idxmax(), "Model"]
    best_model_obj = st.session_state['trained_models'][best_model_name]['model']
    
    if hasattr(best_model_obj, 'feature_importances_'):
        st.markdown("### 📊 6. Dimensional Impact")
        feat_imp = pd.DataFrame({"Feature": st.session_state['ml_features'], "Importance": best_model_obj.feature_importances_}).sort_values("Importance", ascending=True).tail(10)
        fig = px.bar(feat_imp, x="Importance", y="Feature", orientation='h', color="Importance", color_continuous_scale=["#6C63FF", "#00C9A7"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white", family="Inter"), showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

# ── Step 7: Neural Prediction ───────────────────────────────────────────
if st.session_state.get('trained_models'):
    st.write("---")
    st.markdown("### ⚡ 7. Neural Prediction")
    with st.container(border=True):
        pred_model_name = st.selectbox("Active Inference Model", list(st.session_state['trained_models'].keys()))
        pred_model = st.session_state['trained_models'][pred_model_name]['model']

        input_cols = st.columns(3)
        input_values = {}
        for i, feat in enumerate(st.session_state['ml_features']):
            with input_cols[i % 3]:
                if df[feat].dtype in ['object', 'category'] if feat in df.columns else False:
                    input_values[feat] = st.selectbox(f"{feat}", df[feat].unique(), key=f"p_{feat}")
                else:
                    input_values[feat] = st.number_input(f"{feat}", value=float(df[feat].median()) if feat in df.columns else 0.0, key=f"p_{feat}")

        if st.button("Initiate Prediction", type="primary", use_container_width=True):
            input_df = pd.DataFrame([input_values])
            prediction = pred_model.predict(input_df)[0]
            if st.session_state.get('ml_le'):
                prediction = st.session_state['ml_le'].inverse_transform([int(prediction)])[0]
            
            st.markdown(f"""
            <div style="background:rgba(108, 99, 255, 0.1); border:1px solid rgba(108, 99, 255, 0.3); border-radius:15px; padding:2rem; text-align:center; margin-top:1.5rem;">
                <h3 style="color:#00C9A7; margin-bottom:0.5rem;">Forge Inference Result</h3>
                <h1 style="font-size:3.5rem; margin:0;">{prediction}</h1>
            </div>
            """, unsafe_allow_html=True)
