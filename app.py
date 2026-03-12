"""
DataNexus AI – Natural Language CSV Data Analyst
Major Project · Powered by Google Gemini
Architecture: DRY, modular, clean separation of concerns
UI Direction: Editorial/utilitarian — ink-on-paper meets terminal
"""

import os, shutil, textwrap, traceback, re, json, time
from contextlib import redirect_stdout
from io import BytesIO, StringIO

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import google.generativeai as genai

# ═══════════════════════════════════════════════════════════════════════════════
# ▌ CONSTANTS  (single source of truth — no magic strings anywhere else)
# ═══════════════════════════════════════════════════════════════════════════════

GEMINI_API_KEY = "AIzaSyAElE3hYA0OVbU7GbviAhh7ICyadK6b6nE"
MODEL_NAME     = "gemini-2.0-flash"
CHARTS_DIR     = "./charts"
CHAT_HISTORY_WINDOW = 8
DF_UPDATE_SENTINEL  = "DataFrame has been updated."
CHART_JSON_PATH     = "temp_chart.json"

SYSTEM_INSTRUCTION = textwrap.dedent("""\
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATANEXUS AI — SYSTEM PROMPT  v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

── CONSTANTS (defined once; referenced by name below) ──────────────
  DF_UPDATE_SENTINEL  →  "DataFrame has been updated."
  CHART_SAVE_CMD      →  fig.write_json('temp_chart.json')
  CHART_LAYOUT        →  template='plotly_dark',
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)'
  PRE_IMPORTED        →  pd, np, px, go, plt, sns, pio, BytesIO, json
  CHART_CONFIRM_PHRASE→  "A chart was generated."
────────────────────────────────────────────────────────────────────


── IDENTITY ─────────────────────────────────────────────────────────
You are DataNexus AI, a senior data analyst assistant embedded in the
DataNexus platform. You are precise, efficient, and grounded entirely
in the data provided. You do not use filler phrases ("Great question!",
"Certainly!", "Of course!"). You do not narrate intent — you act.
When something fails, you state what failed and provide a fix immediately.
────────────────────────────────────────────────────────────────────


── CONTEXT ──────────────────────────────────────────────────────────
Every message you receive already contains:
  · DataFrame shape (rows × columns)
  · Column names and dtypes
  · First 5 rows as a sample
  · The user's request in plain English

The dataset is loaded as `df`. Do not ask the user to re-upload or
re-describe their data. Do not re-read the CSV. Everything required
is in the context provided.
────────────────────────────────────────────────────────────────────


── CONTRACT: CODE ────────────────────────────────────────────────────
RULE        All executable code lives in a single ```python … ``` block.
RULE        All libraries in PRE_IMPORTED are available without import.
RULE        After any DataFrame modification, print a brief summary
            (e.g. new shape, number of affected rows).
RULE        Code must be clean, idiomatic, and commented where non-obvious.
CONSEQUENCE If code cannot be written safely for the request, explain why
            and offer a safe alternative.
────────────────────────────────────────────────────────────────────


── CONTRACT: CHARTS ─────────────────────────────────────────────────
RULE        Always use Plotly (px or go). Never use matplotlib or seaborn
            for output charts.
RULE        After creating any figure, execute CHART_SAVE_CMD.
RULE        Apply CHART_LAYOUT to every figure via fig.update_layout(…).
RULE        Confirm every chart with CHART_CONFIRM_PHRASE.
RULE        Select the most appropriate chart type for the data and question.
            Do not default to bar charts when a histogram, scatter, box,
            heatmap, or time-series plot would be more informative.
CONSEQUENCE If no suitable chart type exists for the request, explain why
            and suggest the closest appropriate alternative.
────────────────────────────────────────────────────────────────────


── CONTRACT: DATAFRAME UPDATES ──────────────────────────────────────
RULE        Whenever df is modified — cleaning, filtering, encoding,
            feature engineering, type conversion, dropping rows or columns —
            the final line of your response must be DF_UPDATE_SENTINEL.
RULE        Do not emit DF_UPDATE_SENTINEL unless df was actually changed.
CONSEQUENCE Emitting DF_UPDATE_SENTINEL incorrectly will trigger a state
            update in the application. Accuracy here is critical.
────────────────────────────────────────────────────────────────────


── CONTRACT: RESPONSES ──────────────────────────────────────────────
RULE        Lead with the answer or action; explanation follows.
RULE        Use markdown tables for statistics and comparisons.
RULE        Use headers, bold, and code blocks only where they improve
            readability. Do not over-format short or simple responses.
RULE        If a request is ambiguous, state your assumption clearly
            and proceed. Ask for clarification only when proceeding
            without it would produce a meaningless or harmful result.
RULE        Never fabricate data, invent column values, or hallucinate
            statistics. Every insight must derive from actual df contents.
CONSEQUENCE If a request is unsafe, unethical, or technically impossible
            given the current data, decline politely and propose a
            practical alternative.
────────────────────────────────────────────────────────────────────


── CAPABILITIES ─────────────────────────────────────────────────────
Each category below defines the full scope of supported tasks.

  EXPLORATION       shape, dtypes, value counts, missing value analysis,
                    descriptive statistics, correlation, distribution checks,
                    duplicate detection.

  VISUALISATION     bar, line, scatter, histogram, box, violin, heatmap,
                    pair plot, time series, geographic (if lat/lon present).

  CLEANING          null imputation, duplicate removal, outlier detection,
                    type casting, string normalisation, date parsing,
                    whitespace trimming.

  FEATURE ENG.      label encoding, one-hot encoding, ordinal encoding,
                    binning, min-max scaling, standard scaling, derived
                    columns, date decomposition.

  MODELLING         classification, regression, clustering via scikit-learn;
                    train/test split, cross-validation, feature importance,
                    evaluation metrics (accuracy, RMSE, silhouette, etc.).

  EXPORT PREP       column renaming, reordering, row filtering, shape
                    confirmation before the user downloads the result.
────────────────────────────────────────────────────────────────────


── BOUNDARY CONDITIONS ──────────────────────────────────────────────
The following are explicitly out of scope:
  · Reading from or writing to external files other than CHART_SAVE_CMD.
  · Making network requests or API calls.
  · Generating synthetic or fake data to fill gaps without disclosure.
  · Modifying session state, environment variables, or system paths.
────────────────────────────────────────────────────────────────────
""")

SAMPLE_PROMPTS = [
    "Show basic statistics of the dataset",
    "List all columns with their data types",
    "Plot a correlation heatmap",
    "Handle missing values with mean imputation",
    "Create a bar chart of the top 10 values",
    "Drop duplicate rows",
    "Encode categorical columns with Label Encoding",
    "Train a simple Random Forest classifier",
]

GNDEC_KB: dict[tuple, str] = {
    ("established", "year", "founded", "when", "history"):
        "**GNDEC** (Guru Nanak Dev Engineering College) was **established in 1956** — one of the oldest engineering colleges in North India.",
    ("website", "official", "web", "url", "site"):
        "Official website: [https://www.gndec.ac.in/](https://www.gndec.ac.in/)",
    ("admission", "jee", "gate", "apply", "entrance", "how to join"):
        "**Admissions:**\n- B.Tech via **JEE Main** counselling\n- M.Tech via **GATE** scores\n- Portal: [admission.gndec.ac.in](https://admission.gndec.ac.in/)\n- WhatsApp: **73472-00448**",
    ("location", "address", "where", "city", "map"):
        "**Address:** Gill Park, Ludhiana, Punjab 141006, India",
    ("course", "branch", "program", "department", "btech", "mtech", "degree"):
        "**Courses:**\n- B.Tech: CSE, ECE, Mechanical, Civil, IT, EE & more\n- M.Tech · MBA · MCA · Ph.D.\n- New: B.Tech Robotics & AI",
    ("principal", "director", "head"):
        "Visit [gndec.ac.in](https://www.gndec.ac.in/) for current leadership.",
    ("placement", "job", "recruit", "company"):
        "Top recruiters include TCS, Infosys, Wipro, HCL. Details at [gndec.ac.in](https://www.gndec.ac.in/)",
}
GNDEC_FALLBACK = "For the latest information visit [https://www.gndec.ac.in/](https://www.gndec.ac.in/)"

DOWNLOAD_FORMATS = {
    "CSV":           ("datanexus_updated.csv",     "text/csv"),
    "Excel (.xlsx)": ("datanexus_updated.xlsx",    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    "Parquet":       ("datanexus_updated.parquet", "application/octet-stream"),
    "JSON":          ("datanexus_updated.json",    "application/json"),
}

SESSION_DEFAULTS = {
    "messages":       [],
    "original_df":    None,
    "current_df":     None,
    "message_count":  0,
    "chat_history":   [],
    "uploaded_name":  None,
}

# ─── Editorial / Utilitarian Design System ────────────────────────────────────
# Aesthetic: sparse ink-on-paper newsroom meets monospace terminal.
# Palette: warm cream paper, near-black ink, saffron accent, cool slate mid-tones.
# Fonts: "Playfair Display" (display/headings) + "IBM Plex Mono" (data/code).
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    background-color: #f5f0e8 !important;
    color: #1a1209 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #1a1209 !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * { color: #d4cabb !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(212,202,187,0.25) !important;
    color: #d4cabb !important;
    border-radius: 3px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    transition: background 0.2s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(212,202,187,0.1) !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f5f0e8 !important;
    font-size: 1rem !important;
}
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #7a7060 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
}
section[data-testid="stSidebar"] hr { border-color: rgba(212,202,187,0.12) !important; }

/* ── Prompt chips in sidebar ── */
.prompt-chip {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #7a7060;
    padding: 0.3rem 0;
    border-bottom: 1px solid rgba(212,202,187,0.08);
    cursor: default;
    letter-spacing: 0.01em;
}

/* ── Main area headers ── */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3 {
    font-family: 'Playfair Display', serif !important;
    color: #1a1209 !important;
    letter-spacing: -0.02em !important;
}

/* ── Hero ── */
.hero-wrap {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    padding: 2.5rem 0 0.5rem;
    border-bottom: 3px solid #1a1209;
    margin-bottom: 2rem;
}
.hero-logotype {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 3.2rem;
    color: #1a1209;
    letter-spacing: -0.04em;
    line-height: 1;
    margin: 0;
}
.hero-logotype em {
    font-style: italic;
    color: #c8860a;   /* saffron accent */
}
.hero-descriptor {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #7a7060;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    align-self: center;
    padding-bottom: 0.25rem;
    border-left: 2px solid #c8860a;
    padding-left: 0.75rem;
    margin-left: 0.5rem;
}

/* ── Rule lines ── */
.rule-thin { border: none; border-top: 1px solid #c8b99a; margin: 1.2rem 0; }
.rule-thick { border: none; border-top: 3px solid #1a1209; margin: 1.5rem 0; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #c8b99a !important;
    border-radius: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #7a7060 !important;
    border-radius: 0 !important;
    padding: 0.6rem 1.4rem !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #1a1209 !important;
    border-bottom: 2px solid #c8860a !important;
    font-weight: 600 !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #ede8df !important;
    border: 1px solid #c8b99a !important;
    border-left: 3px solid #c8860a !important;
    border-radius: 2px !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #7a7060 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.6rem !important;
    color: #1a1209 !important;
}

/* ── Buttons (main area) ── */
[data-testid="stMain"] .stButton > button,
[data-testid="stMain"] .stDownloadButton > button {
    background: #1a1209 !important;
    color: #f5f0e8 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.76rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    padding: 0.55rem 1.2rem !important;
    transition: background 0.2s !important;
}
[data-testid="stMain"] .stButton > button:hover,
[data-testid="stMain"] .stDownloadButton > button:hover {
    background: #c8860a !important;
    color: #1a1209 !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #ede8df !important;
    border: 1px solid #c8b99a !important;
    border-radius: 2px !important;
    margin-bottom: 0.75rem !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    border-left: 3px solid #c8860a !important;
}
[data-testid="stChatMessage"][data-testid*="assistant"] {
    border-left: 3px solid #1a1209 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {
    font-family: 'IBM Plex Sans', sans-serif !important;
    background: #ede8df !important;
    border: 1px solid #c8b99a !important;
    border-radius: 2px !important;
    color: #1a1209 !important;
}

/* ── Code blocks ── */
code, pre {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    background: #1a1209 !important;
    color: #d4cabb !important;
    border-radius: 2px !important;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border: 1px solid #c8b99a !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.76rem !important;
}

/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
    background: #ede8df !important;
    border: 2px dashed #c8b99a !important;
    border-radius: 2px !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] summary {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.76rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    color: #4a4030 !important;
}

/* ── Radio / Select ── */
[data-testid="stRadio"] label,
[data-testid="stSelectbox"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.76rem !important;
}

/* ── Status badges ── */
.badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 1px;
}
.badge-live  { background: #c8860a; color: #1a1209; }
.badge-empty { background: transparent; color: #7a7060; border: 1px solid #7a7060; }

/* ── FAB (floating GNDEC button) ── */
.fab-outer {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 999999;
}
.fab-outer .stButton > button {
    width: 64px !important;
    height: 64px !important;
    border-radius: 50% !important;
    background: #1a1209 !important;
    color: #f5f0e8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.55rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    border: 2px solid #c8860a !important;
    padding: 0 !important;
    box-shadow: 4px 4px 0 #c8860a !important;
    transition: box-shadow 0.15s, transform 0.15s !important;
}
.fab-outer .stButton > button:hover {
    background: #c8860a !important;
    color: #1a1209 !important;
    box-shadow: 2px 2px 0 #1a1209 !important;
    transform: translate(2px, 2px) !important;
}

/* ── Info / warning / success boxes ── */
[data-testid="stAlert"] {
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
}

/* ── Footer ── */
.app-footer {
    margin-top: 3rem;
    padding: 1.2rem 0;
    border-top: 1px solid #c8b99a;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #7a7060;
    letter-spacing: 0.06em;
    text-align: center;
}

/* ── Dialog / modal ── */
div[data-testid="stDialog"] div[role="dialog"] {
    background: #f5f0e8 !important;
    border: 2px solid #1a1209 !important;
    border-radius: 2px !important;
    box-shadow: 8px 8px 0 #1a1209 !important;
}
</style>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# ▌ PAGE CONFIG (must be first Streamlit call)
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DataNexus AI",
    layout="wide",
    page_icon="◈",
    initial_sidebar_state="expanded",
)
st.markdown(THEME_CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ▌ SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
def init_session() -> None:
    """Initialise all session-state keys from SESSION_DEFAULTS."""
    for k, v in SESSION_DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session()
os.makedirs(CHARTS_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ▌ SERVICE LAYER  (pure functions — testable without Streamlit)
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_gemini_model():
    """Return a singleton Gemini GenerativeModel."""
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION,
    )


def extract_python_code(text: str) -> str | None:
    """Return the first Python fenced code block content, or None."""
    match = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None


def execute_code(code: str, df: pd.DataFrame) -> tuple[str, pd.DataFrame, object | None]:
    """
    Execute `code` with `df` in scope.
    Returns (stdout, updated_df, plotly_fig_or_None).
    """
    ns = {
        "df": df.copy(), "pd": pd, "np": np,
        "plt": plt, "sns": sns, "px": px, "go": go, "pio": pio,
        "BytesIO": BytesIO, "json": json,
    }
    try:
        import sklearn; ns["sklearn"] = sklearn
    except ImportError:
        pass

    buf = StringIO()
    try:
        with redirect_stdout(buf):
            exec(code, {"__builtins__": __builtins__}, ns)
    except Exception:
        buf.write(traceback.format_exc())

    # Resolve Plotly figure: check namespace first, then temp file
    plotly_fig = next(
        (ns[k] for k in ("fig", "figure", "chart") if isinstance(ns.get(k), go.Figure)),
        None,
    )
    if plotly_fig is None and os.path.exists(CHART_JSON_PATH):
        try:
            plotly_fig = pio.read_json(CHART_JSON_PATH)
        finally:
            _silent_remove(CHART_JSON_PATH)

    return buf.getvalue(), ns.get("df", df), plotly_fig


def gndec_answer(question: str) -> str:
    """Return a GNDEC knowledge-base answer for `question`."""
    q = question.lower().strip()
    for keywords, answer in GNDEC_KB.items():
        if any(kw in q for kw in keywords):
            return answer
    return GNDEC_FALLBACK


def build_context_prompt(user_query: str, df: pd.DataFrame) -> str:
    """Build the full prompt to send to Gemini, including DataFrame context."""
    return (
        f"DataFrame info:\n"
        f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n\n"
        f"Columns & types:\n{df.dtypes.to_string()}\n\n"
        f"Sample (first 5 rows):\n{df.head(5).to_string()}\n\n"
        f"User request: {user_query}"
    )


def ask_gemini(
    user_query: str, df: pd.DataFrame
) -> tuple[str, str, pd.DataFrame, object | None, str | None]:
    """
    Send `user_query` to Gemini with DataFrame context.
    Returns (answer_md, exec_stdout, updated_df, plotly_fig, mpl_chart_path).
    """
    context_prompt = build_context_prompt(user_query, df)
    model = get_gemini_model()

    # Rebuild history slice for Gemini chat
    history = [
        {"role": m["role"], "parts": [m["text"]]}
        for m in st.session_state.chat_history[-CHAT_HISTORY_WINDOW:]
    ]
    chat = model.start_chat(history=history)
    response = chat.send_message(context_prompt)
    answer = response.text

    # Persist to session history
    st.session_state.chat_history.append({"role": "user",  "text": context_prompt})
    st.session_state.chat_history.append({"role": "model", "text": answer})

    # Execute any embedded code
    exec_output, new_df, plotly_fig = "", df, None
    code = extract_python_code(answer)
    if code:
        exec_output, new_df, plotly_fig = execute_code(code, df)

    # Fallback: matplotlib PNG
    mpl_chart = None
    if os.path.exists("temp_chart.png"):
        st.session_state.message_count += 1
        dest = os.path.join(CHARTS_DIR, f"chart_{st.session_state.message_count}.png")
        shutil.move("temp_chart.png", dest)
        mpl_chart = dest

    return answer, exec_output, new_df, plotly_fig, mpl_chart


def serialize_df(df: pd.DataFrame, fmt: str) -> BytesIO:
    """Serialise `df` to the requested format and return a BytesIO buffer."""
    buf = BytesIO()
    if fmt == "CSV":
        df.to_csv(buf, index=False)
    elif fmt == "Excel (.xlsx)":
        df.to_excel(buf, index=False, engine="openpyxl")
    elif fmt == "Parquet":
        df.to_parquet(buf, index=False, engine="pyarrow")
    elif fmt == "JSON":
        buf.write(df.to_json(orient="records", indent=2).encode())
    buf.seek(0)
    return buf


# ═══════════════════════════════════════════════════════════════════════════════
# ▌ UI HELPERS  (reusable markup / component builders)
# ═══════════════════════════════════════════════════════════════════════════════

def _silent_remove(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        pass


def render_plotly(fig: go.Figure, key: str) -> None:
    """Apply consistent dark-transparent theme and render a Plotly chart."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#1a1209",
    )
    st.plotly_chart(fig, use_container_width=True, key=key)


def render_chat_message(msg: dict, index: int) -> None:
    """Render a single stored chat message (user or assistant)."""
    avatar = "◈" if msg["role"] == "assistant" else "◉"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("plotly_fig_json"):
            try:
                render_plotly(pio.from_json(msg["plotly_fig_json"]), f"hist_{index}")
            except Exception:
                pass
        if msg.get("mpl_chart") and os.path.exists(msg["mpl_chart"]):
            st.image(msg["mpl_chart"], use_container_width=True)
        if msg["role"] == "assistant":
            if st.button("⌘ Copy response", key=f"copy_{index}"):
                st.toast("Use Ctrl+V to paste", icon="⌘")


def _col_info_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return a summary DataFrame of column metadata."""
    return pd.DataFrame({
        "Column":   df.columns,
        "Type":     df.dtypes.astype(str).values,
        "Non-Null": df.notnull().sum().values,
        "Null":     df.isnull().sum().values,
        "Unique":   df.nunique().values,
    })


def render_dataset_metrics(df: pd.DataFrame) -> None:
    """Render the four summary metric tiles for a loaded DataFrame."""
    c1, c2, c3, c4 = st.columns(4)
    mem_kb = df.memory_usage(deep=True).sum() / 1024
    mem_label = f"{mem_kb:.0f} KB" if mem_kb < 1024 else f"{mem_kb / 1024:.1f} MB"
    with c1: st.metric("Rows",   f"{df.shape[0]:,}")
    with c2: st.metric("Columns", f"{df.shape[1]:,}")
    with c3: st.metric("Memory", mem_label)
    with c4: st.metric("Missing", f"{int(df.isnull().sum().sum()):,}")


# ═══════════════════════════════════════════════════════════════════════════════
# ▌ DIALOGS
# ═══════════════════════════════════════════════════════════════════════════════

@st.dialog("GNDEC — College Info")
def show_gndec_dialog() -> None:
    st.markdown(
        '<p style="font-family:\'Playfair Display\',serif;font-size:1.3rem;'
        'font-weight:700;margin:0 0 0.25rem;">Ask about GNDEC</p>',
        unsafe_allow_html=True,
    )
    st.caption("Admissions · Courses · Location · Placements")
    st.divider()
    question = st.text_input(
        "Your question",
        placeholder="e.g. What courses are offered at GNDEC?",
        key="gndec_q",
        label_visibility="collapsed",
    )
    if question:
        st.info(gndec_answer(question))
    st.markdown(
        '<p style="font-family:\'IBM Plex Mono\',monospace;font-size:0.68rem;'
        'color:#7a7060;margin-top:1rem;">Official site: '
        '<a href="https://www.gndec.ac.in/" target="_blank">gndec.ac.in</a></p>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ▌ SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(
        '<h2 style="font-family:\'Playfair Display\',serif;color:#f5f0e8 !important;'
        'font-size:1.25rem;margin:0.5rem 0 0.15rem;">DataNexus <em style="color:#c8860a;">AI</em></h2>',
        unsafe_allow_html=True,
    )
    st.caption("Natural language CSV analyst")
    st.divider()

    # Data status
    if st.session_state.current_df is not None:
        df_ref = st.session_state.current_df
        st.markdown('<span class="badge badge-live">● Live</span>', unsafe_allow_html=True)
        st.caption(
            f"{df_ref.shape[0]:,} rows · {df_ref.shape[1]} cols\n{st.session_state.uploaded_name}"
        )
    else:
        st.markdown('<span class="badge badge-empty">○ No data</span>', unsafe_allow_html=True)

    st.divider()

    with st.expander("QUICK ACTIONS", expanded=True):
        ca, cb = st.columns(2)
        with ca:
            if st.button("Reset data", use_container_width=True, key="btn_reset"):
                if st.session_state.original_df is not None:
                    st.session_state.current_df    = st.session_state.original_df.copy()
                    st.session_state.messages      = []
                    st.session_state.chat_history  = []
                    st.session_state.message_count = 0
                    st.toast("Data reset to original")
                    st.rerun()
                else:
                    st.toast("No data loaded yet")
        with cb:
            if st.button("Clear chat", use_container_width=True, key="btn_clear"):
                st.session_state.messages      = []
                st.session_state.chat_history  = []
                st.session_state.message_count = 0
                st.toast("Chat cleared")
                st.rerun()

    with st.expander("SAMPLE PROMPTS", expanded=False):
        for p in SAMPLE_PROMPTS:
            st.markdown(f'<div class="prompt-chip">→ {p}</div>', unsafe_allow_html=True)

    st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
# ▌ HERO HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero-wrap">
    <h1 class="hero-logotype">Data<em>Nexus</em></h1>
    <span class="hero-descriptor">Natural language<br>CSV analyst · Gemini</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ▌ TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab_upload, tab_chat, tab_download = st.tabs([
    "01 — Upload & Preview",
    "02 — Chat Analysis",
    "03 — Export",
])


# ───────────────────────────────────────────────────────────────────────────────
# TAB 1 — UPLOAD & PREVIEW
# ───────────────────────────────────────────────────────────────────────────────
with tab_upload:
    uploaded_file = st.file_uploader(
        "Drop a CSV here, or click to browse",
        type=["csv"],
        help="Max 200 MB · data stays in your session only",
    )

    if uploaded_file is not None:
        # Only re-load if the file has changed
        if (
            st.session_state.original_df is None
            or st.session_state.uploaded_name != uploaded_file.name
        ):
            with st.spinner("Reading dataset…"):
                try:
                    df = pd.read_csv(uploaded_file)
                    st.session_state.original_df   = df.copy()
                    st.session_state.current_df    = df.copy()
                    st.session_state.messages      = []
                    st.session_state.chat_history  = []
                    st.session_state.message_count = 0
                    st.session_state.uploaded_name = uploaded_file.name
                    st.toast(f"Loaded: {uploaded_file.name}")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Failed to read CSV: {exc}")
                    st.stop()

    if st.session_state.current_df is not None:
        cdf = st.session_state.current_df
        render_dataset_metrics(cdf)
        st.divider()

        with st.expander("DATA PREVIEW — first 1 000 rows", expanded=True):
            st.dataframe(cdf.head(1000), use_container_width=True, height=380)

        with st.expander("COLUMN INFO", expanded=False):
            st.dataframe(_col_info_table(cdf), use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;border:1px dashed #c8b99a;border-radius:2px;margin-top:2rem;">
            <p style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#4a4030;margin:0 0 0.5rem;">
                No dataset loaded
            </p>
            <p style="font-family:'IBM Plex Mono',monospace;font-size:0.76rem;color:#7a7060;margin:0;">
                Upload a CSV file above, then open the Chat Analysis tab.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# TAB 2 — CHAT ANALYSIS
# ───────────────────────────────────────────────────────────────────────────────
with tab_chat:
    if st.session_state.current_df is None:
        st.info("Upload a CSV file in the Upload & Preview tab before chatting.")
    else:
        # Render history
        for i, msg in enumerate(st.session_state.messages):
            render_chat_message(msg, i)

        # New input
        user_query = st.chat_input("Ask anything about your data…")

        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user", avatar="◉"):
                st.markdown(user_query)

            with st.chat_message("assistant", avatar="◈"):
                with st.spinner("Analysing…"):
                    try:
                        answer, exec_out, new_df, plotly_fig, mpl_chart = ask_gemini(
                            user_query, st.session_state.current_df
                        )
                        display_md = answer
                        if exec_out and exec_out.strip():
                            display_md += f"\n\n**Execution output:**\n```\n{exec_out.strip()}\n```"
                        if DF_UPDATE_SENTINEL in answer:
                            st.session_state.current_df = new_df
                            st.toast("DataFrame updated")
                    except Exception as exc:
                        display_md = f"Error: {exc}"
                        plotly_fig = mpl_chart = None

                st.markdown(display_md)
                if plotly_fig is not None:
                    render_plotly(plotly_fig, f"new_{st.session_state.message_count}")
                if mpl_chart and os.path.exists(mpl_chart):
                    st.image(mpl_chart, use_container_width=True)

            asst = {"role": "assistant", "content": display_md}
            if plotly_fig is not None:
                asst["plotly_fig_json"] = plotly_fig.to_json()
            if mpl_chart:
                asst["mpl_chart"] = mpl_chart
            st.session_state.messages.append(asst)
            st.rerun()


# ───────────────────────────────────────────────────────────────────────────────
# TAB 3 — EXPORT
# ───────────────────────────────────────────────────────────────────────────────
with tab_download:
    if st.session_state.current_df is None:
        st.info("Upload a CSV file first to enable export.")
    else:
        cdf = st.session_state.current_df
        st.markdown(
            f'<p style="font-family:\'IBM Plex Mono\',monospace;font-size:0.76rem;color:#7a7060;">'
            f'Current dataset — {cdf.shape[0]:,} rows × {cdf.shape[1]} columns</p>',
            unsafe_allow_html=True,
        )
        st.divider()

        fmt = st.radio("Format", list(DOWNLOAD_FORMATS), horizontal=True, key="dl_fmt")
        fname, mime = DOWNLOAD_FORMATS[fmt]
        buf = serialize_df(cdf, fmt)

        st.download_button(
            label=f"Download as {fmt}",
            data=buf,
            file_name=fname,
            mime=mime,
            use_container_width=True,
        )

        st.divider()
        with st.expander("DATASET SUMMARY STATISTICS"):
            st.dataframe(cdf.describe(include="all").T, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ▌ FOOTER + FAB
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="app-footer">'
    "Major Project&nbsp;·&nbsp;Powered by Google Gemini&nbsp;·&nbsp;"
    "Data is session-local and never stored"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown('<div class="fab-outer">', unsafe_allow_html=True)
if st.button("GNDEC", key="fab_gndec"):
    show_gndec_dialog()
st.markdown("</div>", unsafe_allow_html=True)
