import streamlit as st
import pandas as pd
from utils.theme import load_css, glass_card
from utils.navigation import sidebar_nav
from utils.data_utils import process_data

st.set_page_config(page_title="DataNexusAI - Upload", page_icon="📂", layout="wide")
load_css()
sidebar_nav(2)

st.markdown('<h1 class="gradient-text">Upload Your Data</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card" style="border: 2px dashed rgba(255,255,255,0.2); text-align: center; padding: 3rem;">
    <p style="font-size: 1.5rem; opacity: 0.7;">📥 Drag & Drop or Click to Browse</p>
    <p style="font-size: 0.9rem; opacity: 0.5;">Support for CSV, XLSX, and JSON (Max 50MB)</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["csv", "xlsx", "json"], label_visibility="collapsed")

if uploaded_file is not None:
    with st.spinner("Processing your data..."):
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
            
            st.success(f"Successfully loaded '{uploaded_file.name}' with {df.shape[0]} rows and {df.shape[1]} columns!")
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

if st.session_state.get('df') is not None:
    df = st.session_state['df']
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Data Preview")
        st.dataframe(df.head(100), use_container_width=True)
        
    with col2:
        st.markdown("### Schema Inspector")
        with st.expander("View Details", expanded=True):
            schema_df = pd.DataFrame({
                "Column": df.columns,
                "Type": df.dtypes.astype(str),
                "Non-Null": df.notna().sum().values,
                "Unique": df.nunique().values
            })
            st.table(schema_df)
            
        if st.button("🚀 Analyze This Dataset", type="primary", use_container_width=True):
            st.switch_page("pages/2_Dashboard.py")
else:
    st.info("Please upload a dataset to begin the analysis.")
