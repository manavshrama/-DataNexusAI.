import streamlit as st
from utils.constants import CUSTOM_CSS, PAGE_TITLE, PAGE_ICON
from services.vector_store import initialize_vector_store
from services.session_manager import init_session_state
from components.sidebar_ui import render_sidebar
from components.tab_renderers import (
    render_upload_tab, render_eda_tab, render_viz_tab, 
    render_ml_tab, render_chat_tab, render_export_tab
)

# --- PAGE CONFIG ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- CUSTOM CSS ---
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- INITIALIZE SERVICES ---
init_session_state()
embedder, chroma_client, chat_collection, doc_collection = initialize_vector_store()

# --- SIDEBAR ---
render_sidebar()

# --- MAIN APP ---
st.title("🔮 Data Science Hub")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📂 Upload", "📊 EDA", "🎨 Viz", "🤖 ML Lab", "💬 AI Chat", "📥 Export"
])

with tab1:
    render_upload_tab(doc_collection, embedder)

with tab2:
    render_eda_tab()

with tab3:
    render_viz_tab()

with tab4:
    render_ml_tab()

with tab5:
    render_chat_tab(chroma_client, embedder, chat_collection, doc_collection)

with tab6:
    render_export_tab()
