import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
import re
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def extract_python_code(text: str) -> Optional[str]:
    """Extracts python code block from a markdown string."""
    pattern = r"```python\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None

def execute_code(code: str, df: pd.DataFrame) -> Tuple[str, pd.DataFrame, Optional[plt.Figure]]:
    """
    Executes Python code in a controlled environment.
    Returns: (stdout_str, updated_df, figure)
    """
    stdout_buf = io.StringIO()
    
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
        # CodeRabbit: Using a more controlled execution scope
        exec(code, exec_globals)
        updated_df = exec_globals.get('df', df)
        
        # Check for matplotlib figures
        fig = plt.gcf() if plt.get_fignums() else None
        if fig:
            plt.close('all') # Cleanup to avoid memory leaks
        
        return stdout_buf.getvalue(), updated_df, fig
    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}")
        return f"Execution Error: {str(e)}", df, None

def execute_code_blocks(text: str, df: pd.DataFrame):
    """Parses and executes all python code blocks found in the text."""
    code_blocks = re.findall(r'```python\n(.*?)\n```', text, re.DOTALL)
    for code in code_blocks:
        with st.expander("🛠️ Neural Engine Execution", expanded=False):
            st.code(code, language='python')
            try:
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
            except Exception as e:
                logger.error(f"Failed to execute code block: {e}")
                st.error(f"Neural Engine Error: {str(e)}")
