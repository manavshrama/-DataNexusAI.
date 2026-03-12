import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

class EDAModule:
    """Exploratory Data Analysis module with specialized statistical methods."""
    
    @staticmethod
    def statistical_summary(df):
        """Returns a dict of summary statistics for numeric and categorical columns."""
        res = {}
        # Numeric Summary
        num_df = df.select_dtypes(include=[np.number])
        if not num_df.empty:
            summary = num_df.describe().T
            summary['CV%'] = (summary['std'] / summary['mean']) * 100
            summary['Range'] = summary['max'] - summary['min']
            summary['Skewness'] = num_df.skew()
            summary['Kurtosis'] = num_df.kurt()
            res['numeric'] = summary
            
        # Categorical Summary
        cat_df = df.select_dtypes(exclude=[np.number])
        if not cat_df.empty:
            cat_summary = []
            for col in cat_df.columns:
                mode_val = cat_df[col].mode()
                mode_str = mode_val[0] if not mode_val.empty else "N/A"
                freq = cat_df[col].value_counts().iloc[0] if not cat_df[col].empty else 0
                cat_summary.append({
                    "Column": col,
                    "Unique": cat_df[col].nunique(),
                    "Mode": mode_str,
                    "Frequency": freq
                })
            res['categorical'] = pd.DataFrame(cat_summary)
            
        return res

    @staticmethod
    def correlation_analysis(df):
        """Returns the correlation matrix and top correlated pairs."""
        num_df = df.select_dtypes(include=[np.number])
        if num_df.empty:
            return None, None
            
        corr_matrix = num_df.corr()
        
        # Melt to get pairs
        pairs = corr_matrix.stack().reset_index()
        pairs.columns = ['V1', 'V2', 'Corr']
        # Remove self-correlation and duplicates
        pairs = pairs[pairs['V1'] != pairs['V2']]
        # Sort by absolute correlation
        pairs['AbsCorr'] = pairs['Corr'].abs()
        top_pairs = pairs.sort_values(by='AbsCorr', ascending=False).drop_duplicates(subset=['AbsCorr']).head(10)
        
        return corr_matrix, top_pairs

    @staticmethod
    def plot_distributions(df, col):
        """Returns a histogram with box marginal and a QQ plot (conceptually)."""
        if col not in df.columns:
            return None
        
        fig = px.histogram(df, x=col, marginal="box", title=f"Distribution of {col}", 
                           template="plotly_dark", color_discrete_sequence=['#667eea'])
        return fig

    @staticmethod
    def detect_outliers(df, col):
        """Detects outliers using IQR and Z-score."""
        if col not in df.columns or not np.issubdtype(df[col].dtype, np.number):
            return None
        
        data = df[col].dropna()
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        iqr_outliers = data[(data < (q1 - 1.5 * iqr)) | (data > (q3 + 1.5 * iqr))]
        
        z_scores = np.abs(stats.zscore(data))
        z_outliers = data[z_scores > 3]
        
        return {
            "iqr_count": len(iqr_outliers),
            "z_count": len(z_outliers),
            "total_rows": len(data)
        }

    @staticmethod
    def missing_value_analysis(df):
        """Returns missing value percentages per column."""
        missing = df.isnull().sum()
        pct = (missing / len(df)) * 100
        missing_df = pd.DataFrame({"Missing Values": missing, "Percentage": pct})
        missing_df = missing_df[missing_df["Missing Values"] > 0].sort_values(by="Percentage", ascending=False)
        return missing_df

    @staticmethod
    def categorical_distribution(df, col, top_n=10):
        """Returns bar and pie charts for a categorical column."""
        counts = df[col].value_counts().head(top_n).reset_index()
        counts.columns = [col, 'Count']
        
        bar = px.bar(counts, x=col, y='Count', title=f"Top {top_n} {col}", 
                     template="plotly_dark", color_discrete_sequence=['#764ba2'])
        pie = px.pie(counts, names=col, values='Count', hole=0.4, title=f"{col} Distribution", 
                     template="plotly_dark")
        return bar, pie
