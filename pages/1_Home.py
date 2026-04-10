import streamlit as st
from utils.theme import load_css, glass_card
from utils.navigation import sidebar_nav

st.set_page_config(page_title="DataNexusAI - Home", page_icon="🌌", layout="wide")
load_css()
sidebar_nav(0)

# Hero Section
st.markdown("""
<div class="glass-card shimmer-card" style="text-align: center; padding: 5rem 2rem; border-bottom: 2px solid var(--glass-border);">
    <h1 class="shimmer-text" style="font-size: 4rem; line-height: 1.2; margin-bottom: 1.5rem;">DataNexusAI — Your AI-Powered Data Universe</h1>
    <p style="font-size: 1.4rem; margin-bottom: 3rem; opacity: 0.8; max-width: 800px; margin-left: auto; margin-right: auto;">
        Unlock the secrets of your data with advanced analysis, AI-powered insights, and no-code machine learning.
    </p>
</div>
""", unsafe_allow_html=True)

# CTA Buttons placed directly under the hero banner
cta_col1, cta_col2, cta_col3, cta_col4 = st.columns([1, 2, 2, 1])
with cta_col2:
    if st.button("🚀 Upload Data", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Upload.py")
with cta_col3:
    if st.button("💬 Start Chatting", use_container_width=True):
        st.switch_page("pages/4_Chat.py")

st.write("## ")

# Feature Cards
cols = st.columns(3)
with cols[0]:
    st.markdown("""
    <div class="glass-card">
        <h3>📊 Data Analysis</h3>
        <p>Auto-generate rich visualizations and deep insights from any dataset.</p>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown("""
    <div class="glass-card">
        <h3>🤖 AI Chat</h3>
        <p>Talk to your data in natural language and get instant answers.</p>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown("""
    <div class="glass-card">
        <h3>⚡ ML Studio</h3>
        <p>Train, evaluate, and deploy machine learning models without writing a line of code.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("## ")

# Quick Stats
st.markdown("### Platform Pulse")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("Datasets Analyzed", "1,248", "+12%")
m_col2.metric("Models Trained", "452", "+5%")
m_col3.metric("Queries Answered", "15.4K", "+8%")
m_col4.metric("Charts Generated", "8.9K", "+20%")

st.write("## ")

# Getting Started
with st.expander("📖 New to DataNexusAI? Let's get started."):
    st.markdown("""
    1. **Upload Data**: Go to the Upload section and drop your CSV or Excel file.
    2. **Explore Dashboard**: View automated visualizations and statistical summaries.
    3. **Chat with AI**: Ask specific questions about your data trends or anomalies.
    4. **Train Model**: Use the ML Studio to build predictive models on your target variables.
    """)
