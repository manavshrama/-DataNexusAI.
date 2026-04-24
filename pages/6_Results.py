import streamlit as st
import pandas as pd
from utils.theme import load_css, glass_card, render_hero
from components.sidebar_ui import render_sidebar

st.set_page_config(page_title="DataNexusAI - Results", page_icon="📥", layout="wide")
load_css()
render_sidebar()

render_hero("Results Vault", "Evaluate performance, explore predictions, and export your model")

# ── Summary Cards ──────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    df = st.session_state.get('df')
    if df is not None:
        content = f"""
        <div style="text-align:center;">
            <h2 style="margin-bottom:0;">{st.session_state.get('file_name', 'N/A')}</h2>
            <p style="color:#00C9A7; font-weight:600;">{df.shape[0]:,} Rows × {df.shape[1]} Columns</p>
        </div>
        """
        glass_card(content, title="Active Dataset", subtitle="Data Source Connectivity")
    else:
        glass_card('<div style="text-align:center; padding:1rem; opacity:0.5;">No active data universe found.</div>', title="Dataset", subtitle="Disconnected")

with c2:
    results = st.session_state.get('ml_results', [])
    if results:
        task = st.session_state.get('ml_task', 'Classification')
        metric_key = "Accuracy" if task == "Classification" else "R² Score"
        best = max(results, key=lambda r: r.get(metric_key, 0))
        content = f"""
        <div style="text-align:center;">
            <h2 style="margin-bottom:0; color:#6C63FF;">{best['Model']}</h2>
            <p style="font-weight:600;">{metric_key}: {best.get(metric_key, 'N/A')}</p>
        </div>
        """
        glass_card(content, title="Top Performer", subtitle="Best Trained Model")
    else:
        glass_card('<div style="text-align:center; padding:1rem; opacity:0.5;">Forge a model to see performance.</div>', title="Model Performance", subtitle="Inactive")

with c3:
    chat_count = len(st.session_state.get('messages', []))
    content = f"""
    <div style="text-align:center;">
        <h2 style="margin-bottom:0;">{chat_count}</h2>
        <p style="font-weight:600;">Interactions Logged</p>
    </div>
    """
    glass_card(content, title="AI Intelligence", subtitle="Nexus Chat Logs")

st.write("---")

# ── Model Report Card ──────────────────────────────────────────────────
if st.session_state.get('trained_models'):
    st.markdown("### 📄 Model Report Card")
    
    trained = st.session_state['trained_models']
    model_tabs = st.tabs([f"Model: {name}" for name in trained.keys()])

    for tab, model_name in zip(model_tabs, trained.keys()):
        with tab:
            info = trained[model_name]
            metrics = info['metrics']
            y_test = info['y_test']
            y_pred = info['y_pred']

            # High-Performance Metrics
            st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
            cols = st.columns(len([k for k in metrics if k != "Model"]))
            display_metrics = [(k, v) for k, v in metrics.items() if k != "Model"]
            for i, (k, v) in enumerate(display_metrics):
                with cols[i]:
                    st.metric(label=k, value=v)

            # Performance Visuals
            st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
            v1, v2 = st.columns([2, 1])
            
            with v1:
                task = st.session_state.get('ml_task', 'Classification')
                if task == "Classification":
                    import plotly.figure_factory as ff
                    from sklearn.metrics import confusion_matrix as cm_fn
                    import numpy as np

                    cm = cm_fn(y_test, y_pred)
                    labels = [str(l) for l in sorted(y_test.unique())]
                    fig = ff.create_annotated_heatmap(
                        z=cm, x=labels, y=labels,
                        colorscale="Viridis", showscale=True
                    )
                    fig.update_layout(
                        title=f"{model_name} Confusion Matrix",
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="white", family="Inter"),
                        xaxis_title="Predicted Class", yaxis_title="Actual Class",
                        margin=dict(t=50, b=50, l=50, r=50)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with v2:
                st.markdown("#### Insight Summary")
                st.info(f"Model {model_name} shows strong performance in {task} tasks. Review the confusion matrix for specific class misalignments.")

# ── Export & Connectivity ──────────────────────────────────────────────
st.markdown("### 📥 Nexus Export Center")

exp_cols = st.columns(4)

export_types = [
    ("📊 Results CSV", "ml_results", "model_results.csv"),
    ("📂 Full Dataset", "df", "dataset.csv"),
    ("🧠 Best Model", "trained_models", "best_model.pkl"),
    ("💬 Chat Logs", "messages", "chat_history.json")
]

for i, (label, key, fname) in enumerate(export_types):
    with exp_cols[i]:
        if st.session_state.get(key):
            # Special handling for Model Pickle
            if key == "trained_models":
                import pickle, io
                best_name = list(st.session_state[key].keys())[0]
                best_obj = st.session_state[key][best_name]['model']
                buf = io.BytesIO()
                pickle.dump(best_obj, buf)
                st.download_button(label, buf.getvalue(), fname, "application/octet-stream", use_container_width=True)
            elif key == "df":
                csv = st.session_state[key].to_csv(index=False)
                st.download_button(label, csv, fname, "text/csv", use_container_width=True)
            elif key == "messages":
                import json
                log = json.dumps(st.session_state[key], indent=2)
                st.download_button(label, log, fname, "application/json", use_container_width=True)
            else:
                csv = pd.DataFrame(st.session_state[key]).to_csv(index=False)
                st.download_button(label, csv, fname, "text/csv", use_container_width=True)
        else:
            st.button(label, disabled=True, use_container_width=True)

if not any([st.session_state.get('df'), st.session_state.get('ml_results'), st.session_state.get('messages')]):
    st.info("The Export Center is empty. Connect a dataset and generate intelligence to see results.")
