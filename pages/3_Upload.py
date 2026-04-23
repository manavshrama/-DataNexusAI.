import streamlit as st
import pandas as pd
from utils.theme import load_css, glass_card
from utils.navigation import sidebar_nav
from utils.data_utils import process_data

st.set_page_config(page_title="DataNexusAI - Gateway", page_icon="📂", layout="wide")
load_css()
sidebar_nav(2)

st.markdown('<h1 class="gradient-text">Nexus Data Gateway</h1>', unsafe_allow_html=True)
st.markdown('<p style="opacity:0.6; margin-bottom:2rem;">Bridge your local datasets into the Nexus intelligence core.</p>', unsafe_allow_html=True)

# ── The Dropzone ───────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card" style="border: 2px dashed rgba(108, 99, 255, 0.4); text-align: center; padding: 4rem 2rem;">
    <h2 style="font-size: 3rem; margin-bottom: 1rem;">🛰️</h2>
    <h2 class="gradient-text">Initialize Connection</h2>
    <p style="font-size: 1.1rem; opacity: 0.7; margin-bottom: 0;">Drag & drop your files into the field below</p>
    <p style="font-size: 0.85rem; opacity: 0.4;">Supported Formats: CSV, XLSX, JSON (Max 50MB)</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["csv", "xlsx", "json"], label_visibility="collapsed")

if uploaded_file is not None:
    with st.spinner("Synchronizing data nodes..."):
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_json(uploaded_file)
            
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
        with st.container(border=True):
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
