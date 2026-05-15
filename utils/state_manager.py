import pandas as pd
import streamlit as st
from typing import Any, Dict, Optional

def _timestamp() -> str:
    """Return current timestamp as ISO string."""
    return pd.Timestamp.now().isoformat()

def add_audit_entry(action: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Append an audit entry to session state.

    Parameters
    ----------
    action: str
        Short description of the performed action (e.g., "clean_data", "train_model").
    details: dict, optional
        Additional context such as parameters or outcomes.
    """
    entry = {
        "timestamp": _timestamp(),
        "action": action,
        "details": details or {}
    }
    # Ensure the audit_log list exists
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []
    st.session_state.audit_log.append(entry)

def add_vault_asset(asset_type: str, data: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Store an asset (visualization, model, export) in the vault.

    Parameters
    ----------
    asset_type: str
        Type identifier, e.g., "visualization", "model", "export".
    data: Any
        The primary payload (could be a Plotly figure, DataFrame, etc.).
    metadata: dict, optional
        Additional information such as filename, description.
    """
    asset = {
        "timestamp": _timestamp(),
        "type": asset_type,
        "data": data,
        "metadata": metadata or {}
    }
    if "vault_assets" not in st.session_state:
        st.session_state.vault_assets = []
def get_audit_log() -> list:
    """Return the current audit log from session state."""
    return st.session_state.get('audit_log', [])

def get_vault_assets() -> list:
    """Return the list of stored vault assets."""
    return st.session_state.get('vault_assets', [])

def clear_state(preserve_keys: list = None) -> None:
    """Reset session state, optionally preserving specified keys.
    
    Args:
        preserve_keys (list, optional): List of session state keys to retain.
    """
    if preserve_keys is None:
        preserve_keys = []
    # Preserve values
    preserved = {k: st.session_state.get(k) for k in preserve_keys}
    st.session_state.clear()
    # Restore preserved keys
    for k, v in preserved.items():
        st.session_state[k] = v
def get_working_df() -> pd.DataFrame:
    """Return the current working DataFrame from session state.
    Alias for st.session_state.df for backward compatibility."""
    return st.session_state.get('df')

def set_working_df(df: pd.DataFrame) -> None:
    """Set the working DataFrame in session state.
    Updates both 'df' and 'working_df' keys to keep them in sync."""
    st.session_state.df = df
    st.session_state.working_df = df

# Ensure alias consistency on initialization
if 'working_df' not in st.session_state:
    st.session_state.working_df = st.session_state.get('df')
