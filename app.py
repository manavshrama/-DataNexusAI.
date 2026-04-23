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

# ── Sidebar Branding ──
with st.sidebar:
    st.markdown('<h1 class="gradient-text" style="font-size:1.8rem; margin-bottom:0;">🌌 DataNexusAI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.8rem; opacity:0.5; margin-left:2.4rem;">v1.2.0 | Advanced Intelligence</p>', unsafe_allow_html=True)
    st.write("---")

# ── Hero Section ──
st.markdown("""
<div style="text-align: center; padding: 3rem 0 4rem 0;">
    <h1 class="gradient-text" style="font-size: 4.5rem; line-height: 1.1; margin-bottom: 1rem;">
        The Next Frontier of<br>Data Intelligence
    </h1>
    <p style="font-size: 1.4rem; color: rgba(255,255,255,0.7); max-width: 800px; margin: 0 auto 2.5rem auto;">
        Experience seamless AI-driven analysis, visual exploration, and machine learning 
        within a high-performance glassmorphism ecosystem.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Primary Actions ──
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    st.markdown("""
    <div class="glass-card" style="min-height: 280px; text-align: center; border-bottom: 4px solid #6C63FF;">
        <h2 style="font-size: 3rem; margin-bottom: 1rem;">📊</h2>
        <h3 class="gradient-text">Studio</h3>
        <p style="font-size: 0.95rem; opacity: 0.7; margin-bottom: 1.5rem;">Explore 35+ advanced chart types in our high-precision Visual Universe.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Dashboard", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")

with c2:
    st.markdown("""
    <div class="glass-card" style="min-height: 280px; text-align: center; border-bottom: 4px solid #00C9A7;">
        <h2 style="font-size: 3rem; margin-bottom: 1rem;">🤖</h2>
        <h3 class="gradient-text">AI Chat</h3>
        <p style="font-size: 0.95rem; opacity: 0.7; margin-bottom: 1.5rem;">Talk to your data. Generate visuals and cleaned files via natural language.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Chat", use_container_width=True):
        st.switch_page("pages/4_Chat.py")

with c3:
    st.markdown("""
    <div class="glass-card" style="min-height: 280px; text-align: center; border-bottom: 4px solid #845EC2;">
        <h2 style="font-size: 3rem; margin-bottom: 1rem;">🧠</h2>
        <h3 class="gradient-text">ML Forge</h3>
        <p style="font-size: 0.95rem; opacity: 0.7; margin-bottom: 1.5rem;">Train, evaluate, and export professional models in a few clicks.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Access Forge", use_container_width=True):
        st.switch_page("pages/5_ML_Studio.py")

st.write("---")

# ── Platform Stats ──
s1, s2, s3, s4 = st.columns(4)
stats = [
    ("Processing Speed", "1.2 GB/s", "⚡"),
    ("Visual Variety", "35+ Types", "🎨"),
    ("Model Accuracy", "Up to 99%", "🎯"),
    ("Uptime", "99.9%", "🛡️")
]

for col, (label, val, icon) in zip([s1, s2, s3, s4], stats):
    with col:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 15px; padding: 1.5rem; text-align: center;">
            <p style="font-size: 0.8rem; opacity: 0.5; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">{label}</p>
            <h2 style="margin: 0; color: #00C9A7;">{icon} {val}</h2>
        </div>
        """, unsafe_allow_html=True)

st.write("")
if st.button("🚀  Start by Uploading Your Dataset", use_container_width=True):
    st.switch_page("pages/3_Upload.py")
