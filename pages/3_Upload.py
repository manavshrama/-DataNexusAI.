import streamlit as st
import pandas as pd
from utils.theme import load_css, glass_card, render_hero
from components.sidebar_ui import render_sidebar
from modules.data_loader import DataLoader
from services.vector_store import initialize_vector_store
from utils.data_utils import process_data

st.set_page_config(page_title="DataNexusAI - Upload", page_icon="📂", layout="wide", initial_sidebar_state="expanded")
load_css()
render_sidebar()

render_hero("Data Nexus", "Upload your dataset and let the engine take over")

uploaded_file = st.file_uploader("Upload Data", type=["csv", "xlsx", "json"])

if uploaded_file is not None:
    with st.spinner("Synchronizing data nodes..."):
        try:
            filename_lower = uploaded_file.name.lower()
            if filename_lower.endswith(".csv") or filename_lower.endswith(('.xlsx', '.xlsm', '.xltx', '.xltm', '.xls', '.xlsb', '.ods')):
                df, error = DataLoader.load_file(uploaded_file)
                if error:
                    raise ValueError(error)
            elif filename_lower.endswith(".json"):
                df = pd.read_json(uploaded_file)
            else:
                raise ValueError(f"Unsupported file format: {uploaded_file.name}")
            
            df = process_data(df)
            st.session_state['df'] = df
            st.session_state['file_name'] = uploaded_file.name
            
            st.success(f"Nexus Linked: '{uploaded_file.name}' — {df.shape[0]:,} records mapped.")
            
        except Exception as e:
            st.error(f"Synchronization failed: {str(e)}")

# ── Data Universe Preview ──────────────────────────────────────────────
if st.session_state.get('df') is not None:
    df = st.session_state['df']
    st.write("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔍 Global Node Preview")
        st.dataframe(df.head(50), use_container_width=True)
        
    with col2:
        st.markdown("### 🧭 Dimensional Schema")
        with st.container():
            schema_df = pd.DataFrame({
                "Dimension": df.columns,
                "Type": df.dtypes.astype(str),
                "Integrity": [f"{v}%" for v in (df.notna().sum().values / len(df) * 100).astype(int)]
            })
            st.dataframe(schema_df, use_container_width=True, hide_index=True)
            
        st.write("")
        if st.button("🚀  Enter Studio", type="primary", use_container_width=True):
            st.switch_page("pages/2_Dashboard.py")
else:
    st.info("The Gateway is idle. Upload a dataset to activate the Nexus.")
