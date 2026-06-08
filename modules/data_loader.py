import pandas as pd
import numpy as np
import io

class DataLoader:
    """Handles loading CSV and Excel files with smart encoding detection and stats extraction."""
    
    @staticmethod
    def load_file(uploaded_file):
        """Loads a file (CSV or Excel) and returns a DataFrame and an error message if any."""
        df = None
        error = None
        
        try:
            filename = getattr(uploaded_file, 'name', '') or ''
            filename_lower = filename.lower()
            
            if filename_lower.endswith('.csv'):
                # Try common encodings
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                for encoding in encodings:
                    try:
                        df = pd.read_csv(uploaded_file, encoding=encoding)
                        break
                    except (UnicodeDecodeError, pd.errors.ParserError):
                        if hasattr(uploaded_file, 'seek'):
                            uploaded_file.seek(0)
                        continue
                
                if df is None:
                    error = "Could not decode CSV file with common encodings."
            
            elif filename_lower.endswith(('.xlsx', '.xlsm', '.xltx', '.xltm', '.xls', '.xlsb', '.ods')):
                try:
                    if filename_lower.endswith(('.xlsx', '.xlsm', '.xltx', '.xltm')):
                        df = pd.read_excel(uploaded_file, engine='openpyxl')
                    elif filename_lower.endswith('.xls'):
                        df = pd.read_excel(uploaded_file, engine='xlrd')
                    elif filename_lower.endswith('.xlsb'):
                        df = pd.read_excel(uploaded_file, engine='pyxlsb')
                    elif filename_lower.endswith('.ods'):
                        df = pd.read_excel(uploaded_file, engine='odf')
                except Exception as engine_err:
                    # Fallback to standard read_excel without specifying engine
                    try:
                        if hasattr(uploaded_file, 'seek'):
                            uploaded_file.seek(0)
                        df = pd.read_excel(uploaded_file)
                    except Exception as fallback_err:
                        raise engine_err
            
            else:
                error = f"Unsupported file format: {filename}"
                
        except Exception as e:
            error = f"Error loading file: {str(e)}"
            
        return df, error

    @staticmethod
    def get_stats(df):
        """Returns basic statistics for the dataframe."""
        if df is None:
            return {}
        
        return {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "nulls": df.isnull().sum().sum(),
            "duplicates": df.duplicated().sum(),
            "null_pct": (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100 if df.size > 0 else 0,
            "dtypes": df.dtypes.to_dict()
        }

    @staticmethod
    def clean_data(df, action):
        """Performs data cleaning based on the requested action."""
        if df is None:
            return None
        
        df_cleaned = df.copy()
        
        if action == "drop_duplicates":
            df_cleaned = df_cleaned.drop_duplicates()
        elif action == "fill_nulls_mean":
            numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
            df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].mean())
        elif action == "drop_any_nulls":
            df_cleaned = df_cleaned.dropna()
        
        return df_cleaned
