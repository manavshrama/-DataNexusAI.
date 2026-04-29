import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
import re

def extract_python_code(text: str) -> str | None:
    """Extracts python code block from a markdown string."""
    pattern = r"```python\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None

def execute_code(code: str, df: pd.DataFrame):
    """
    Executes Python code in a controlled environment.
    Returns: (stdout_str, updated_df, figure)
    """
    # Redirect stdout
    stdout_buf = io.StringIO()
    
    # Execution context
    exec_globals = {
        'pd': pd,
        'np': np,
        'plt': plt,
        'sns': sns,
        'px': px,
        'st': st,
        'df': df,
        'io': io
    }
    
    try:
        # We need to capture the state of df after execution
        exec(code, exec_globals)
        updated_df = exec_globals.get('df', df)
        
        # Check for matplotlib figures
        fig = plt.gcf() if plt.get_fignums() else None
        
        return stdout_buf.getvalue(), updated_df, fig
    except Exception as e:
        return f"Error: {str(e)}", df, None

def execute_code_blocks(text: str, df: pd.DataFrame):
    """Parses and executes all python code blocks found in the text."""
    code_blocks = re.findall(r'```python\n(.*?)\n```', text, re.DOTALL)
    for code in code_blocks:
        with st.expander("🛠️ Executing Generated Code", expanded=False):
            st.code(code, language='python')
            try:
                # Execution context
                exec_globals = {
                    'pd': pd,
                    'np': np,
                    'plt': plt,
                    'sns': sns,
                    'px': px,
                    'st': st,
                    'df': df,
                    'io': io
                }
                exec(code, exec_globals)
                # Note: df update in session state should be handled by caller if needed
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
