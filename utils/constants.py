# --- CUSTOM CSS ---
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #0b1c30 !important;
        color: #f8f9ff !important;
    }
    
    /* Stitch Headers */
    h1, h2, h3, [data-testid="stHeader"] {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 700 !important;
        color: #f8f9ff !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #071321 !important;
        border-right: 1px solid rgba(115, 118, 135, 0.1) !important;
    }
    
    /* Surface Cards (Stitch Tonal Layering) */
    div[data-testid="stMetric"], .stChatMessage, div[data-testid="stExpander"] {
        background-color: #11253e !important;
        border: 1px solid rgba(115, 118, 135, 0.15) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
    }
    
    /* Stitch Primary Button */
    .stButton > button {
        background: linear-gradient(135deg, #0049db 0%, #2962ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 600 !important;
        font-family: 'Manrope', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(0, 73, 219, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 73, 219, 0.4) !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px !important;
        white-space: pre !important;
        background-color: rgba(115, 118, 135, 0.05) !important;
        border-radius: 8px 8px 0 0 !important;
        color: rgba(248, 249, 255, 0.5) !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0049db !important;
        color: white !important;
    }

    /* Glass Effects */
    .glass-card {
        background: rgba(17, 37, 62, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
    }
</style>
"""

# --- UI STRINGS ---
PAGE_TITLE = "Data Nexus AI"
PAGE_ICON = "🔮"
APP_HEADER = "🔮 Data Science Hub"
AI_ANALYST_TITLE = "💬 AI Data Analyst"
ML_LAB_TITLE = "🤖 Machine Learning Lab"
VIZ_STUDIO_TITLE = "Data Visualization Studio"
EDA_TITLE = "Exploratory Data Analysis"
EXPORT_TITLE = "Export Cleaned Data"
UPLOAD_TITLE = "Step 1: Upload & Initial stats"
