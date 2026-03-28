import streamlit as st
import threading
import time
import uuid
import requests
import os

def keep_alive():
    """Background service to ping the app and prevent sleep."""
    app_url = os.environ.get("APP_URL") or (st.secrets.get("APP_URL") if "APP_URL" in st.secrets else None)
    if not app_url:
        return
    while True:
        try:
            requests.get(app_url, timeout=10)
        except Exception:
            pass
        time.sleep(270)

def init_session_state():
    """Initialize session state variables and start background threads."""
    # Try to get keys from secrets (for deployment)
    default_groq = ""
    default_gemini = ""
    if hasattr(st, "secrets"):
        default_groq = st.secrets.get("GROQ_API_KEY", "")
        default_gemini = st.secrets.get("GEMINI_API_KEY", "")

    keys = {
        "df": None,
        "df_cleaned": None,
        "df_original": None,
        "file_name": None,
        "chat_history": [],
        "groq_key": default_groq,
        "gemini_key": default_gemini,
        "eda_done": False,
        "ml_results": {},
        "keep_alive_started": False,
        "session_id": str(uuid.uuid4())
    }
    for k, v in keys.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if not st.session_state.keep_alive_started:
        st.session_state.keep_alive_started = True
        t = threading.Thread(target=keep_alive, daemon=True)
        t.start()
