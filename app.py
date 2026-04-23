# DATA NEXUS AI - UNIVERSAL ENGINE v1.1.0 (FORCE DEPLOY)
import sys

# Standard Fix for ChromaDB/SQLite version conflict on Streamlit Cloud
try:
    import pysqlite3 as sqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import streamlit as st
from utils.theme import load_css

# ── Page Config (MUST be first Streamlit command) ──
st.set_page_config(
    page_title="DataNexusAI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialize Session State ──
def init_state():
    defaults = {
        'df': None,
        'messages': [],
        'trained_models': {},
        'saved_charts': [],
        'ml_results': [],
        'settings': {
            'api_key': '',
            'theme_accent': '#6C63FF',
            'glass_opacity': 0.05,
        }
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
load_css()

# ── Sidebar branding (shown on default/home page) ──
with st.sidebar:
    st.markdown('<h1 class="gradient-text" style="font-size:1.6rem;">🌌 DataNexusAI</h1>', unsafe_allow_html=True)
    st.caption("v1.1.0 | Nexus Labs")

# ── Home Page Content ──
# (This file IS the home page in Streamlit's multi-page layout)

st.markdown("""
<div class="glass-card" style="text-align: center; padding: 4rem 2rem; margin-bottom: 2rem;">
    <h1 class="gradient-text" style="font-size: 3.2rem; margin-bottom: 0.5rem;">
        DataNexusAI
    </h1>
    <p style="font-size: 1.3rem; opacity: 0.85; margin-bottom: 0.2rem;">
        Your AI-Powered Data Universe
    </p>
    <p style="font-size: 1rem; opacity: 0.55;">
        Unlock insights with advanced analysis, AI chat, and no-code machine learning.
    </p>
</div>
""", unsafe_allow_html=True)

cta1, cta2 = st.columns(2)
with cta1:
    if st.button("🚀  Upload Data", use_container_width=True):
        st.switch_page("pages/3_Upload.py")
with cta2:
    if st.button("💬  Start AI Chat", use_container_width=True):
        st.switch_page("pages/4_Chat.py")

st.write("")

# Feature cards
cols = st.columns(3)
features = [
    ("📊", "Data Analysis", "Auto-generate rich visualizations and deep statistical insights from any dataset."),
    ("🤖", "AI Chat", "Talk to your data in natural language and get instant, contextual answers."),
    ("⚡", "ML Studio", "Train, evaluate, and deploy ML models — no code required."),
]
for col, (icon, title, desc) in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class="glass-card" style="min-height: 180px;">
            <h2 style="margin-bottom: 0.5rem;">{icon}</h2>
            <h3 style="margin-bottom: 0.5rem;">{title}</h3>
            <p style="opacity: 0.7; font-size: 0.95rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# Metrics
st.markdown("### Platform Pulse")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Datasets Analyzed", "1,248", "+12%")
m2.metric("Models Trained", "452", "+5%")
m3.metric("Queries Answered", "15.4K", "+8%")
m4.metric("Charts Generated", "8.9K", "+20%")

st.write("")

with st.expander("📖 New to DataNexusAI? Get started in 4 steps"):
    st.markdown("""
    1. **Upload** — Drop your CSV / Excel into the Upload page.
    2. **Dashboard** — View automated visualizations and data profiles.
    3. **AI Chat** — Ask natural-language questions about your data.
    4. **ML Studio** — Select a target, pick models, train, predict.
    """)
