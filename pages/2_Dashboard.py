import streamlit as st
import pandas as pd
from utils.theme import load_css, glass_card
from utils.navigation import sidebar_nav
from utils.data_utils import get_df_summary, infer_column_types
from utils.chart_utils import create_histogram, create_bar_chart, create_heatmap

st.set_page_config(page_title="DataNexusAI - Dashboard", page_icon="📊", layout="wide")
load_css()
sidebar_nav(1)

if st.session_state.get('df') is None:
    st.warning("No data found. Please upload a dataset first.")
    if st.button("Go to Upload"):
        st.switch_page("pages/3_Upload.py")
    st.stop()

df = st.session_state['df']
summary = get_df_summary(df)
numeric_cols, categorical_cols, datetime_cols = infer_column_types(df)

st.markdown(f'<h1 class="gradient-text">Dashboard</h1>', unsafe_allow_html=True)

# Metrics Bar
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("Total Rows", f"{summary['rows']:,}")
m_col2.metric("Total columns", summary['cols'])
m_col3.metric("Missing Values", f"{summary['nulls']:,}")
m_col4.metric("Numeric Fields", summary['numeric_cols'])

# Data Filtering in Sidebar
with st.sidebar:
    st.markdown("### 🔍 Filters")
    if numeric_cols:
        filter_col = st.selectbox("Filter by numeric range", numeric_cols)
        min_v = float(df[filter_col].min())
        max_v = float(df[filter_col].max())
        val_range = st.slider(f"{filter_col} Range", min_v, max_v, (min_v, max_v))
        df = df[(df[filter_col] >= val_range[0]) & (df[filter_col] <= val_range[1])]

# Column Explorer
st.markdown("### 🧭 Column Explorer")
col_to_explore = st.selectbox("Select a column to visualize", df.columns)

exp_col1, exp_col2 = st.columns([2, 1])

with exp_col1:
    if col_to_explore in numeric_cols:
        st.plotly_chart(create_histogram(df, col_to_explore), use_container_width=True)
    elif col_to_explore in categorical_cols:
        st.plotly_chart(create_bar_chart(df, col_to_explore), use_container_width=True)
    else:
        st.write("Visualizations for this data type are still in development.")

with exp_col2:
    st.markdown("#### Statistics")
    st.write(df[col_to_explore].describe())

# Correlation Heatmap
if len(numeric_cols) > 1:
    st.markdown("### 🕸️ Correlation Heatmap")
    st.plotly_chart(create_heatmap(df), use_container_width=True)

st.session_state['df_filtered'] = df
