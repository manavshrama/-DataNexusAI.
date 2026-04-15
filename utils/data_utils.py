import pandas as pd
import numpy as np

def process_data(df):
    """Basic processing and cleaning of the dataframe."""
    # Convert dates automatically
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                pass
    return df

def get_df_summary(df):
    """Returns a summary dictionary for metrics."""
    if df is None:
        return {}
    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "nulls": df.isna().sum().sum(),
        "duplicates": df.duplicated().sum(),
        "numeric_cols": len(df.select_dtypes(include=[np.number]).columns),
        "categorical_cols": len(df.select_dtypes(include=['object', 'category']).columns)
    }

def infer_column_types(df):
    """Returns lists of column names grouped by type."""
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime = df.select_dtypes(include=['datetime']).columns.tolist()
    return numeric, categorical, datetime
