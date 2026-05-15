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
    st.session_state.vault_assets.append(asset)
