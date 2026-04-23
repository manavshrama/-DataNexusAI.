import streamlit as st
import pandas as pd
import io
import json
import pickle
from utils.theme import load_css
from utils.navigation import sidebar_nav

st.set_page_config(page_title="DataNexusAI - Results & Export", page_icon="📋", layout="wide")
load_css()
sidebar_nav(5)

st.markdown('<h1 class="gradient-text">Results & Universal Export</h1>', unsafe_allow_html=True)

# ── Status Check ──
df = st.session_state.get('df')
ml_results = st.session_state.get('ml_results', [])
messages = st.session_state.get('messages', [])
trained_models = st.session_state.get('trained_models', {})

if not any([df is not None, ml_results, messages]):
    st.info("💡 No data or results to export yet. Start by uploading data or chatting with the AI.")
    st.stop()

# ── Summary Metrics ──
m1, m2, m3, m4 = st.columns(4)
if df is not None:
    m1.metric("Dataset Rows", f"{df.shape[0]:,}")
    m2.metric("Dataset Columns", df.shape[1])
m3.metric("Models Trained", len(ml_results))
m4.metric("Chat Interactions", len(messages))

st.markdown("---")

# ── Universal Export Tabs ──
data_tab, report_tab, visual_tab, model_tab = st.tabs([
    "📂 Data Formats", "📄 Reports", "🖼️ Visuals", "🧠 ML Models"
])

# --- CATEGORY 1: DATA FORMATS ---
with data_tab:
    if df is not None:
        st.markdown("### Export Dataset")
        st.write("Download your processed dataset in various industry-standard formats.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV
            st.download_button(
                label="📥 Download as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="dataset.csv",
                mime="text/csv",
                use_container_width=True
            )
            # JSON
            st.download_button(
                label="📥 Download as JSON",
                data=df.to_json(orient='records', indent=2).encode('utf-8'),
                file_name="dataset.json",
                mime="application/json",
                use_container_width=True
            )
            # Excel
            try:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                st.download_button(
                    label="📥 Download as Excel",
                    data=output.getvalue(),
                    file_name="dataset.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Excel error: {e}")

        with col2:
            # Parquet
            try:
                output = io.BytesIO()
                df.to_parquet(output)
                st.download_button(
                    label="📥 Download as Parquet",
                    data=output.getvalue(),
                    file_name="dataset.parquet",
                    mime="application/octet-stream",
                    use_container_width=True
                )
            except:
                st.button("📥 Parquet (Engine Needed)", disabled=True, use_container_width=True)
            
            # Markdown
            st.download_button(
                label="📥 Download as Markdown",
                data=df.head(100).to_markdown().encode('utf-8'),
                file_name="dataset_summary.md",
                mime="text/markdown",
                use_container_width=True
            )
            
            # TSV
            st.download_button(
                label="📥 Download as TSV",
                data=df.to_csv(sep='\t', index=False).encode('utf-8'),
                file_name="dataset.tsv",
                mime="text/tab-separated-values",
                use_container_width=True
            )

        with col3:
            # LaTeX
            st.download_button(
                label="📥 Download as LaTeX",
                data=df.head(50).to_latex().encode('utf-8'),
                file_name="dataset.tex",
                mime="text/plain",
                use_container_width=True
            )
            # HTML Table
            st.download_button(
                label="📥 Download as HTML Table",
                data=df.to_html().encode('utf-8'),
                file_name="dataset.html",
                mime="text/html",
                use_container_width=True
            )
            # XML
            try:
                st.download_button(
                    label="📥 Download as XML",
                    data=df.to_xml().encode('utf-8'),
                    file_name="dataset.xml",
                    mime="application/xml",
                    use_container_width=True
                )
            except:
                st.button("📥 XML (Not Supported)", disabled=True, use_container_width=True)

# --- CATEGORY 2: REPORTS ---
with report_tab:
    st.markdown("### Generate Reports")
    st.write("Export combined summaries of your analysis and conversations.")
    
    rep_col1, rep_col2 = st.columns(2)
    
    with rep_col1:
        # Chat History JSON
        if messages:
            chat_json = json.dumps(messages, indent=2).encode('utf-8')
            st.download_button(
                label="💬 Download Chat History (JSON)",
                data=chat_json,
                file_name="chat_history.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Model Results CSV
        if ml_results:
            results_df = pd.DataFrame(ml_results)
            st.download_button(
                label="📊 Download ML Results (CSV)",
                data=results_df.to_csv(index=False).encode('utf-8'),
                file_name="ml_performance_results.csv",
                mime="text/csv",
                use_container_width=True
            )

    with rep_col2:
        st.info("PDF and DOCX reporting engines are being initialized. Use the 'AI Chat' to request specific text-based reports for now!")

# --- CATEGORY 3: VISUALS ---
with visual_tab:
    st.markdown("### Export Visualizations")
    saved_charts = st.session_state.get('saved_charts', [])
    if not saved_charts:
        st.warning("No charts saved yet. Use the Chat to generate and save visualizations.")
    else:
        st.write(f"You have {len(saved_charts)} saved charts ready for export.")
        # Future implementation: List saved chart objects and provide PNG/SVG downloads

# --- CATEGORY 4: ML MODELS ---
with model_tab:
    if trained_models:
        st.markdown("### Export Trained Models")
        st.write("Download your trained models as serialized objects for deployment.")
        
        for model_name, info in trained_models.items():
            model_obj = info['model']
            
            m_col1, m_col2 = st.columns([3, 1])
            m_col1.write(f"**Model:** {model_name}")
            
            buf = io.BytesIO()
            pickle.dump(model_obj, buf)
            m_col2.download_button(
                label=f"📥 Download .pkl",
                data=buf.getvalue(),
                file_name=f"{model_name.replace(' ', '_')}.pkl",
                mime="application/octet-stream",
                key=f"dl_{model_name}"
            )
    else:
        st.info("Train a model in the 'ML Studio' to see export options here.")

st.markdown("---")
st.caption("Nexus Engine v1.1 | All exports are generated in-memory for security and speed.")
