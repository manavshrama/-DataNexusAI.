import streamlit as st
import pandas as pd
from utils.theme import load_css
from utils.navigation import sidebar_nav

st.set_page_config(page_title="DataNexusAI - Results", page_icon="📋", layout="wide")
load_css()
sidebar_nav(5)

st.markdown('<h1 class="gradient-text">Results & Reports</h1>', unsafe_allow_html=True)

# ── Summary Cards ──────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    df = st.session_state.get('df')
    if df is not None:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <p style="font-size:0.9rem; opacity:0.6;">Dataset</p>
            <h2>{st.session_state.get('file_name', 'N/A')}</h2>
            <p>{df.shape[0]:,} rows × {df.shape[1]} cols</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <p style="font-size:0.9rem; opacity:0.6;">Dataset</p>
            <h2>No data loaded</h2>
        </div>
        """, unsafe_allow_html=True)

with c2:
    results = st.session_state.get('ml_results', [])
    if results:
        task = st.session_state.get('ml_task', 'Classification')
        metric_key = "Accuracy" if task == "Classification" else "R² Score"
        best = max(results, key=lambda r: r.get(metric_key, 0))
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <p style="font-size:0.9rem; opacity:0.6;">Best Model</p>
            <h2>{best['Model']}</h2>
            <p>{metric_key}: {best.get(metric_key, 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <p style="font-size:0.9rem; opacity:0.6;">Best Model</p>
            <h2>No models trained</h2>
        </div>
        """, unsafe_allow_html=True)

with c3:
    chart_count = len(st.session_state.get('saved_charts', []))
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <p style="font-size:0.9rem; opacity:0.6;">Saved Charts</p>
        <h2>{chart_count}</h2>
    </div>
    """, unsafe_allow_html=True)

# ── Model Report Card ──────────────────────────────────────────────────
if st.session_state.get('trained_models'):
    st.markdown("### 📄 Model Report Card")

    trained = st.session_state['trained_models']
    model_tabs = st.tabs(list(trained.keys()))

    for tab, model_name in zip(model_tabs, trained.keys()):
        with tab:
            info = trained[model_name]
            metrics = info['metrics']
            y_test = info['y_test']
            y_pred = info['y_pred']

            # Metrics display
            metric_cols = st.columns(len([k for k in metrics if k != "Model"]))
            for i, (k, v) in enumerate([(k, v) for k, v in metrics.items() if k != "Model"]):
                metric_cols[i].metric(k, v)

            # Confusion matrix for classification
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
                    title="Confusion Matrix",
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", family="Inter"),
                    xaxis_title="Predicted", yaxis_title="Actual"
                )
                st.plotly_chart(fig, use_container_width=True)

# ── Export Options ─────────────────────────────────────────────────────
st.markdown("### 📥 Export Options")

exp_cols = st.columns(4)

with exp_cols[0]:
    if st.session_state.get('ml_results'):
        res_df = pd.DataFrame(st.session_state['ml_results'])
        csv = res_df.to_csv(index=False)
        st.download_button("📊 Download Results CSV", csv, "model_results.csv", "text/csv", use_container_width=True)

with exp_cols[1]:
    if st.session_state.get('df') is not None:
        csv_data = st.session_state['df'].to_csv(index=False)
        st.download_button("📂 Download Dataset CSV", csv_data, "dataset.csv", "text/csv", use_container_width=True)

with exp_cols[2]:
    if st.session_state.get('trained_models'):
        import pickle
        import io
        best_name = list(st.session_state['trained_models'].keys())[0]
        best_obj = st.session_state['trained_models'][best_name]['model']
        buf = io.BytesIO()
        pickle.dump(best_obj, buf)
        st.download_button("🧠 Download Best Model (.pkl)", buf.getvalue(), f"{best_name}.pkl",
                           "application/octet-stream", use_container_width=True)

with exp_cols[3]:
    if st.session_state.get('messages'):
        import json
        chat_json = json.dumps(st.session_state['messages'], indent=2)
        st.download_button("💬 Download Chat Log", chat_json, "chat_history.json",
                           "application/json", use_container_width=True)

if not any([st.session_state.get('df'), st.session_state.get('ml_results'), st.session_state.get('messages')]):
    st.info("Nothing to export yet. Upload data, train models, or chat with AI to generate reports.")
