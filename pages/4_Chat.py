import streamlit as st
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

if 'df' not in st.session_state or st.session_state['df'] is None:
    st.info("💡 You haven't uploaded a dataset yet. I can answer general questions, but upload a file for data-specific insights!")
    dataset_summary = "No dataset uploaded."
else:
    df = st.session_state['df']
    dataset_summary = f"Dataset: {st.session_state.get('file_name', 'Unnamed')}. Rows: {df.shape[0]}, Columns: {', '.join(df.columns)}."

# Sidebar Context
with st.sidebar:
    st.markdown("### 📋 Chat Context")
    st.write(dataset_summary)
    
    st.markdown("### 💡 Sample Questions")
    samples = [
        "What are the main trends?",
        "Show me a summary of numeric columns",
        "Which category is most frequent?",
        "Visualize the correlation between variables"
    ]
    for q in samples:
        if st.button(q, use_container_width=True):
            st.session_state['messages'].append({"role": "user", "content": q})
            # Trigger rerun to show message immediately
            st.rerun()

# Chat display
chat_container = st.container()

with chat_container:
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            bubble_class = "user-bubble" if message["role"] == "user" else "assistant-bubble"
            st.markdown(f"""
            <div class="chat-bubble {bubble_class}">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("Ask anything about your data..."):
    # Clearer chat layout
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-bubble user-bubble">{prompt}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        api_key = st.session_state['settings'].get('api_key')
        with st.spinner("Thinking..."):
            response = get_chat_response(st.session_state['messages'], api_key, dataset_summary)
            st.markdown(f'<div class="chat-bubble assistant-bubble">{response}</div>', unsafe_allow_html=True)
            st.session_state['messages'].append({"role": "assistant", "content": response})

# Chat Management
if st.button("🗑️ Clear Chat History"):
    st.session_state['messages'] = []
    st.rerun()
