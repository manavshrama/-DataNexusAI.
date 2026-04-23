import streamlit as st
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as scipy_stats
import re
from utils.theme import load_css, glass_card
from utils.navigation import sidebar_nav
from utils.llm_utils import get_chat_response

st.set_page_config(page_title="DataNexusAI - AI Chat", page_icon="💬", layout="wide")
load_css()
sidebar_nav(3)

st.markdown('<h1 class="gradient-text">AI Data Analyst</h1>', unsafe_allow_html=True)

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
                    'go': go,
                    'scipy_stats': scipy_stats,
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

    viz_tab, data_tab = st.tabs(["📊 Charts", "🔬 Data"])

    with viz_tab:
        viz_queries = {
            "Distribution": [
                "Plot histograms for all numeric columns",
                "Show box plots to detect outliers",
                "Create violin plots grouped by category",
                "Generate KDE density plots",
                "Q-Q plot for normality testing",
            ],
            "Comparison": [
                "Grouped bar chart comparing categories",
                "Lollipop chart for top 10 values",
                "Horizontal bar chart of category frequencies",
                "Stacked bar chart showing composition",
            ],
            "Relationship": [
                "Scatter matrix (pair plot) for all numeric cols",
                "Correlation heatmap",
                "Bubble chart with 3 variables",
                "Regression plot with trend lines",
                "Hexbin plot for dense data",
            ],
            "Composition": [
                "Pie/Donut chart for category proportions",
                "Treemap for hierarchical data",
                "Sunburst chart for nested categories",
                "Waterfall chart for sequential changes",
            ],
            "Time Series": [
                "Line chart for trends over time",
                "Area chart showing volume over time",
                "Candlestick chart for OHLC data",
            ],
            "Advanced": [
                "Parallel coordinates for all features",
                "Radar/Spider chart comparing profiles",
                "Sankey diagram for categorical flow",
                "Funnel chart for stage drop-off",
            ],
            "Statistical": [
                "Error bar chart (mean ± std)",
                "Residual plot for model diagnostics",
                "Count plot for categorical frequency",
            ],
        }
        for cat, qs in viz_queries.items():
            with st.expander(f"**{cat}**", expanded=False):
                for q in qs:
                    if st.button(q, key=f"viz_{cat}_{q}", use_container_width=True):
                        st.session_state['messages'].append({"role": "user", "content": q})
                        st.rerun()

    with data_tab:
        data_queries = {
            "EDA": [
                "Run full EDA: summary stats, nulls, distributions",
                "Show data types and memory usage",
            ],
            "Cleaning": [
                "Detect and fix all data quality issues",
                "Handle missing values with imputation code",
                "Remove duplicates and provide download",
            ],
            "Modeling": [
                "Recommend ML models for this dataset",
                "Generate a baseline ML pipeline",
            ],
        }
        for cat, qs in data_queries.items():
            with st.expander(f"**{cat}**", expanded=False):
                for q in qs:
                    if st.button(q, key=f"data_{cat}_{q}", use_container_width=True):
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
