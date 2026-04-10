import sys

# Standard Fix for ChromaDB/SQLite version conflict on Streamlit Cloud
try:
    import pysqlite3 as sqlite3

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import streamlit as st
from utils.constants import CUSTOM_CSS, PAGE_TITLE, PAGE_ICON, APP_HEADER
from services.vector_store import initialize_vector_store
from services.session_manager import init_session_state
from components.sidebar_ui import render_sidebar
from components.tab_renderers import (
    render_upload_tab,
    render_eda_tab,
    render_viz_tab,
    render_ml_tab,
    render_chat_tab,
    render_export_tab,
    render_insights_tab,
)

# --- PAGE CONFIG ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- CUSTOM CSS ---
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- KEEP-ALIVE MECHANISM ---
# Add a keep-alive component to prevent Streamlit Cloud from sleeping the app
keep_alive_placeholder = st.empty()


def keep_alive():
    import time

    while True:
        time.sleep(300)  # Sleep for 5 minutes
        keep_alive_placeholder.text(f"Last refresh: {time.strftime('%H:%M:%S')}")
        st.rerun()


# Start keep-alive in a separate thread (though Streamlit may not support it fully)
import threading

keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
keep_alive_thread.start()

# --- INITIALIZE SERVICES ---
init_session_state()
embedder, chroma_client, chat_collection, doc_collection = initialize_vector_store()

# --- SIDEBAR ---
render_sidebar()

from utils.constants import APP_HEADER

# --- MAIN APP ---
st.title(APP_HEADER)
st.sidebar.caption("Build: 2026.03.28-v1.1 (Modularized)")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "📂 Upload",
        "📊 EDA",
        "🎨 Viz",
        "🤖 ML Lab",
        "💬 AI Chat",
        "📥 Export",
        "🔮 Insights",
    ]
)

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

with tab7:
    render_insights_tab()
