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
from modules.chatbot import ChatbotModule

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

from services.execution_service import execute_code_blocks

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
                execute_code_blocks(message["content"], st.session_state.get('df'))

# --- Chat Input ---
if prompt := st.chat_input("Ask anything about your data, charts, or files..."):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # --- Initialize Services ---
        bot = ChatbotModule(
            groq_key=st.session_state.get('groq_key'),
            gemini_key=st.session_state.get('gemini_key')
        )
        embedder, chroma_client, chat_collection, doc_collection = initialize_vector_store()

        with st.spinner("Neural Cache Lookup..."):
            # --- SEMANTIC CACHE LAYER ---
            cached_answer = None
            if chat_collection and embedder:
                try:
                    q_vector = embedder.encode(prompt).tolist()
                    cache_res = chat_collection.query(
                        query_embeddings=[q_vector], 
                        n_results=1,
                        where={"role": "assistant"}
                    )
                    if cache_res and cache_res['distances'] and cache_res['distances'][0]:
                        if cache_res['distances'][0][0] < 0.1: 
                            cached_answer = cache_res['documents'][0][0]
                            st.caption("🚀 Retrieved from Zero-Token Neural Cache")
                except Exception as e:
                    pass

        if cached_answer:
            st.markdown(cached_answer)
            st.session_state['messages'].append({"role": "assistant", "content": cached_answer})
            execute_code_blocks(cached_answer, st.session_state.get('df'))
        else:
            with st.spinner("Nexus AI is processing..."):
                # Use the consolidated ask method
                response_data = bot.ask(prompt, st.session_state.get('df'), st.session_state['messages'])
                
                answer = response_data.get("answer", "No response generated.")
                code = response_data.get("python_code", "")
                
                st.markdown(answer)
                if code:
                    execute_code_blocks(f"```python\n{code}\n```", st.session_state.get('df'))
                
                full_response = f"{answer}\n\n```python\n{code}\n```" if code else answer
                st.session_state['messages'].append({"role": "assistant", "content": full_response})
                
                # Store in Neural Cache
                if chat_collection and embedder:
                    try:
                        import time, uuid
                        vector = embedder.encode(full_response).tolist()
                        chat_collection.add(
                            embeddings=[vector],
                            documents=[full_response],
                            metadatas=[{"role": "assistant", "timestamp": time.time(), "session_id": st.session_state.get('session_id', 'default')}],
                            ids=[f"cache_{uuid.uuid4().hex}"]
                        )
                    except Exception:
                        pass

# --- Chat Management ---
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state['messages'] = []
        st.rerun()
