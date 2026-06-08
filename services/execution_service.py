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

class StreamlitProxy:
    """A proxy wrapper for Streamlit to intercept visual/tabular commands in executed code."""
    def __init__(self, original_st):
        self._st = original_st
        self.plotly_figs = []
        self.matplotlib_figs = []
        self.dataframes = []
        self.writes = []
        
    def plotly_chart(self, fig, *args, **kwargs):
        self.plotly_figs.append(fig)
        
    def pyplot(self, fig=None, *args, **kwargs):
        if fig is None:
            fig = plt.gcf()
        self.matplotlib_figs.append(fig)
        
    def dataframe(self, df, *args, **kwargs):
        self.dataframes.append(df)
        
    def write(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, pd.DataFrame):
                self.dataframes.append(arg)
            elif type(arg).__name__ == "Figure" and "plotly" in type(arg).__module__:
                self.plotly_figs.append(arg)
            else:
                self.writes.append(str(arg))
                
    def __getattr__(self, name):
        return getattr(self._st, name)

def execute_code_blocks(text: str, df: pd.DataFrame, key_suffix: str = "default"):
    """Parses, displays, and executes all python code blocks in text interactively."""
    code_blocks = re.findall(r'```python\s*\n(.*?)\n```', text, re.DOTALL)
    if not code_blocks:
        # Fallback to handle code blocks without explicit newline
        code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)
        
    if not code_blocks:
        return

    from utils.state_manager import get_working_df, set_working_df, add_audit_entry, add_vault_asset
    import hashlib

    # Compute a hash-based key suffix if default is specified
    if key_suffix == "default":
        key_suffix = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]

    for block_idx, code in enumerate(code_blocks):
        clean_code = code.strip()
        block_suffix = f"{key_suffix}_{block_idx}"
        
        st.markdown(
            """
            <style>
            .execution-card {
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 1rem;
                margin-top: 1rem;
                margin-bottom: 1rem;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        with st.expander("🛠️ Neural Engine Execution Guardrail", expanded=True):
            st.caption("🔒 **Human-in-the-Loop:** You can verify and edit the generated python code below before running it.")
            
            # 1. Edit code (Option C: Human-in-the-Loop)
            edited_code = st.text_area(
                "Verify/Edit Python Code:",
                value=clean_code,
                key=f"edit_{block_suffix}",
                height=180
            )
            
            # Action buttons
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                run_btn = st.button("⚡ Approve & Run", key=f"run_btn_{block_suffix}", use_container_width=True)
            with col_btn2:
                reset_btn = st.button("🔄 Reset Code", key=f"reset_btn_{block_suffix}", use_container_width=True)
                if reset_btn:
                    if f"edit_{block_suffix}" in st.session_state:
                        st.session_state[f"edit_{block_suffix}"] = clean_code
                    st.rerun()

            # Result storage key
            res_key = f"result_{block_suffix}"
            if res_key not in st.session_state:
                st.session_state[res_key] = {
                    "executed": False,
                    "stdout": "",
                    "error": None,
                    "plotly_figs": [],
                    "matplotlib_figs": [],
                    "dataframes": [],
                    "writes": [],
                    "df_changed": False,
                    "new_shape": None,
                    "temp_df": None
                }

            # 2. Execution Logic
            if run_btn:
                import sys
                from io import StringIO
                stdout_buf = StringIO()
                old_stdout = sys.stdout
                sys.stdout = stdout_buf
                
                df_before = get_working_df()
                # Create a local copy so changes don't automatically leak to global state until committed
                df_local = df_before.copy() if df_before is not None else None
                
                proxy = StreamlitProxy(st)
                
                exec_globals = {
                    'pd': pd,
                    'np': np,
                    'plt': plt,
                    'sns': sns,
                    'px': px,
                    'st': proxy,
                    'df': df_local,
                    'io': io
                }
                
                error = None
                try:
                    # Execute the user's/AI's code
                    exec(edited_code, exec_globals)
                except Exception as e:
                    error = str(e)
                finally:
                    sys.stdout = old_stdout
                
                stdout_val = stdout_buf.getvalue()
                
                # Matplotlib check
                if plt.get_fignums():
                    proxy.matplotlib_figs.append(plt.gcf())
                    plt.close('all')
                
                # Fallback: check if any plotly figures were created in globals but not explicitly plotted
                if not proxy.plotly_figs:
                    for val in list(exec_globals.values()):
                        if type(val).__name__ == "Figure" and "plotly" in type(val).__module__:
                            proxy.plotly_figs.append(val)
                            break
                
                # Check if DataFrame was modified
                df_after = exec_globals.get('df')
                df_changed = False
                new_shape = None
                if df_before is not None and df_after is not None:
                    if not df_before.equals(df_after):
                        df_changed = True
                        new_shape = df_after.shape
                
                st.session_state[res_key] = {
                    "executed": True,
                    "stdout": stdout_val,
                    "error": error,
                    "plotly_figs": proxy.plotly_figs,
                    "matplotlib_figs": proxy.matplotlib_figs,
                    "dataframes": proxy.dataframes,
                    "writes": proxy.writes,
                    "df_changed": df_changed,
                    "new_shape": new_shape,
                    "temp_df": df_after
                }

            # 3. Persistent rendering of results
            res = st.session_state[res_key]
            if res["executed"]:
                st.write("---")
                st.markdown("### 📊 Execution Output")
                
                # Show error if any
                if res["error"]:
                    st.error(f"❌ Execution Error: {res['error']}")
                else:
                    st.success("✅ Run successful!")
                
                # Show printed outputs (stdout) if any
                if res["stdout"]:
                    st.text_area("Console Output (stdout):", value=res["stdout"], height=100, disabled=True)
                
                # Show writes if any
                for write_item in res.get("writes", []):
                    st.write(write_item)
                
                # Show dataframes if any
                for df_item in res.get("dataframes", []):
                    st.dataframe(df_item, use_container_width=True)
                
                # Show plotly figures if any (Option B: Save to Vault)
                for f_idx, fig in enumerate(res.get("plotly_figs", [])):
                    st.plotly_chart(fig, use_container_width=True, key=f"plotly_render_{block_suffix}_{f_idx}")
                    
                    if st.button(f"⭐ Save Chart {f_idx+1} to Vault", key=f"vault_btn_{block_suffix}_{f_idx}", use_container_width=True):
                        # Construct clean metadata
                        meta = {
                            "chart_type": "Chatbot Visualization",
                            "code": edited_code,
                            "x": getattr(fig, "layout", {}).get("xaxis", {}).get("title", {}).get("text", "X"),
                            "y": getattr(fig, "layout", {}).get("yaxis", {}).get("title", {}).get("text", "Y")
                        }
                        add_vault_asset('visualization', fig, meta)
                        st.toast("Chart saved to Vault successfully! Check the Export tab.", icon="⭐")
                
                # Show matplotlib figures if any
                for f_idx, fig in enumerate(res.get("matplotlib_figs", [])):
                    st.pyplot(fig)
                    
                # Option A: Commit modified DataFrame to state
                if res["df_changed"] and res["temp_df"] is not None:
                    st.warning(f"⚠️ DataFrame shape modified: {get_working_df().shape if get_working_df() is not None else 'N/A'} ➡️ {res['new_shape']}")
                    if st.button("💾 Commit DataFrame to Workspace", key=f"commit_btn_{block_suffix}", use_container_width=True):
                        set_working_df(res["temp_df"])
                        add_audit_entry('clean_data', {
                            'action': 'chatbot_transformation',
                            'code': edited_code,
                            'new_shape': res['new_shape']
                        })
                        st.toast("DataFrame committed to workspace successfully!", icon="💾")
                        st.rerun()

