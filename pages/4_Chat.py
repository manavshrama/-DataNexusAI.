import streamlit as st
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re
from utils.theme import load_css, glass_card, render_hero
from components.sidebar_ui import render_sidebar
from services.vector_store import initialize_vector_store
from utils.llm_utils import get_chat_response

st.set_page_config(page_title="DataNexusAI - Chat", page_icon="💬", layout="wide", initial_sidebar_state="expanded")
load_css()
render_sidebar()

render_hero("Neural Chat", "Ask anything about your data. Get code, charts, and insights instantly.")

# Initialize Session State
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'settings' not in st.session_state:
    st.session_state['settings'] = {}

# --- Build dataset context for system prompt ---
if 'df' not in st.session_state or st.session_state['df'] is None:
    st.info("⚠️ No dataset loaded. Upload a CSV/Excel file on the **Upload** page for data-specific analysis.")
    dataset_summary = "No dataset uploaded."
else:
    df = st.session_state['df']
    file_name = st.session_state.get('file_name', 'Unnamed')
    n_rows, n_cols = df.shape
    null_counts = df.isnull().sum()
    total_nulls = int(null_counts.sum())
    duplicate_rows = int(df.duplicated().sum())
    numeric_cols = list(df.select_dtypes(include='number').columns)
    categorical_cols = list(df.select_dtypes(include='object').columns)
    dtypes_summary = ", ".join([f"{col}({df[col].dtype})" for col in df.columns])

    dataset_summary = (
        f"Dataset: {file_name} | Shape: {n_rows} rows × {n_cols} cols | "
        f"Columns & dtypes: [{dtypes_summary}] | "
        f"Total nulls: {total_nulls} | Duplicate rows: {duplicate_rows} | "
        f"Numeric columns: {numeric_cols} | Categorical columns: {categorical_cols}"
    )

# --- Build data snapshot for LLM grounding ---
data_snapshot = ""
if 'df' in st.session_state and st.session_state['df'] is not None:
    _df = st.session_state['df']
    _snap_df = _df.iloc[:, :20] if _df.shape[1] > 20 else _df
    buf = io.StringIO()
    buf.write("#### df.head()\n")
    _snap_df.head().to_string(buf)
    buf.write("\n\n#### df.describe()\n")
    _snap_df.describe(include='all').to_string(buf)
    data_snapshot = buf.getvalue()
    if _df.shape[1] > 20:
        data_snapshot += f"\n\n(Showing first 20 of {_df.shape[1]} columns)"

# --- Execution Engine ---
def execute_code_blocks(text):
    """Parses and executes python code blocks found in the text."""
    code_blocks = re.findall(r'```python\n(.*?)\n```', text, re.DOTALL)
    for code in code_blocks:
        with st.expander("🛠️ Executing Generated Code", expanded=False):
            st.code(code, language='python')
            try:
                # Setup execution context
                exec_globals = {
                    'pd': pd,
                    'np': np,
                    'plt': plt,
                    'sns': sns,
                    'px': px,
                    'st': st,
                    'df': st.session_state['df'],
                    'io': io
                }
                # Execute the code
                exec(code, exec_globals)
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")

# --- Sidebar: Dataset Context & Quick Actions ---
with st.sidebar:
    st.markdown("### 📋 Dataset Context")
    if 'df' in st.session_state and st.session_state['df'] is not None:
        df = st.session_state['df']
        st.caption(f"**File:** {st.session_state.get('file_name', 'N/A')}")
        st.caption(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} cols")
        st.caption(f"**Nulls:** {int(df.isnull().sum().sum())}  |  **Duplicates:** {int(df.duplicated().sum())}")
        with st.expander("Column Details", expanded=False):
            for col in df.columns:
                st.caption(f"`{col}` — {df[col].dtype} — {df[col].isnull().sum()} nulls")
    else:
        st.caption("No dataset loaded.")

    st.markdown("---")
    st.markdown("### ⚡ Quick Queries")

    queries = {
        "EDA": [
            "Show summary statistics and data distribution",
            "Generate a correlation heatmap for numeric columns",
            "Plot histograms for all numeric features"
        ],
        "Cleaning": [
            "Detect outliers using boxplots and show cleaning code",
            "Provide code to handle missing values and download the result"
        ],
        "Visuals": [
            "Create a Sunburst chart for categorical hierarchy",
            "Generate a Violin plot to show distribution density",
            "Show a Treemap of the composition",
            "Plot a correlation heatmap with annotations",
            "Create an interactive Choropleth map if location data exists"
        ]
    }

    for category, qs in queries.items():
        st.markdown(f"**{category}**")
        for q in qs:
            if st.button(q, key=f"q_{q}", use_container_width=True):
                st.session_state['messages'].append({"role": "user", "content": q})
                st.rerun()

# --- Chat display ---
chat_container = st.container()

with chat_container:
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                execute_code_blocks(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask anything about your data, charts, or files..."):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        api_key = st.session_state['settings'].get('api_key')
        with st.spinner("Processing request..."):
            response = get_chat_response(st.session_state['messages'], api_key, dataset_summary, data_snapshot)
            st.markdown(response)
            execute_code_blocks(response)
            st.session_state['messages'].append({"role": "assistant", "content": response})

# --- Chat Management ---
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state['messages'] = []
        st.rerun()
