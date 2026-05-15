import streamlit as st
from modules.data_loader import DataLoader
from utils.auth import logout
from utils.state_manager import get_working_df, set_working_df, get_audit_log, get_vault_assets

def render_sidebar():
    """Render the sidebar with logo, API configuration, file info, and logout."""
    with st.sidebar:
        # Logo and Branding
        st.markdown('<div style="text-align: center; padding-bottom: 20px;">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=100)
        st.markdown('<h1 class="gradient-text" style="font-size: 1.8rem; margin-bottom: 0;">NEXUS AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 0.7rem; color: #00D2FF; letter-spacing: 0.3em; margin-top: -5px; font-weight: 700;">COMMAND CENTER</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('---')
        
        # API Configuration
        st.subheader("🔑 API Configuration")
        st.session_state.groq_key = st.text_input("Groq API Key", value=st.session_state.get('groq_key', ''), type="password")
        st.session_state.gemini_key = st.text_input("Gemini API Key", value=st.session_state.get('gemini_key', ''), type="password")
        
        # Engine Status
        is_neural = bool(st.session_state.groq_key or st.session_state.gemini_key)
        status_color = "#00D2FF" if is_neural else "#FFA500"
        status_text = "NEURAL MODE" if is_neural else "LOCAL FALLBACK MODE"
        st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; border-left: 4px solid {status_color}; margin-top: 10px;">
                <p style="font-size: 0.6rem; color: #888; margin: 0;">ENGINE STATUS</p>
                <p style="font-size: 0.8rem; font-weight: 800; color: {status_color}; margin: 0;">{status_text}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # File/Data Info
        if get_working_df() is not None:
            st.markdown("---")
            st.subheader("📊 Dataset Stats")
            st.caption(f"**Name:** {st.session_state.get('file_name', 'Unnamed Dataset')}")
            stats = DataLoader.get_stats(get_working_df())
            st.caption(f"**Rows:** {stats['rows']:,}")
            st.caption(f"**Cols:** {stats['cols']:,}")
            
            if st.button("Reset All Data", use_container_width=True):
                set_working_df(st.session_state.df_original.copy())
                st.rerun()

            # Session History
            with st.expander("🕒 Session History", expanded=False):
                st.markdown("**Recent Actions**")
                audit_log = get_audit_log()
                if audit_log:
                    for entry in audit_log[-5:][::-1]:  # Show last 5
                        st.caption(f"- {entry['action']}")
                else:
                    st.caption("No actions logged.")
                
                st.markdown("---")
                st.markdown("**Stored Assets**")
                vault = get_vault_assets()
                if vault:
                    for asset in vault[-5:][::-1]:
                        st.caption(f"- {asset['type']} saved")
                else:
                    st.caption("Vault is empty.")
        else:
            st.info("No data loaded. Visit Upload tab.")
        
        st.markdown("---")
        # App Info and Logout
        if st.button("🔓 Sign Out", use_container_width=True):
            logout()
            
        st.caption("v1.2.3 | Nexus System Core")
