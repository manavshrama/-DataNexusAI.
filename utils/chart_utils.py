import plotly.express as px

# Premium Dark Theme configuration for Plotly
DART_THEME = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#FFFFFF", "family": "Inter"},
        "xaxis": {"gridcolor": "rgba(255,255,255,0.1)", "zerolinecolor": "rgba(255,255,255,0.1)"},
        "yaxis": {"gridcolor": "rgba(255,255,255,0.1)", "zerolinecolor": "rgba(255,255,255,0.1)"},
        "colorway": ["#6C63FF", "#00C9A7", "#845EC2", "#FF7171", "#FFDE69"]
    }
}

def create_histogram(df, column):
    fig = px.histogram(df, x=column, color_discrete_sequence=["#6C63FF"])
    fig.update_layout(DART_THEME["layout"])
    return fig

def create_bar_chart(df, column):
    counts = df[column].value_counts().reset_index()
    fig = px.bar(counts, x=column, y='count', color_discrete_sequence=["#00C9A7"])
    fig.update_layout(DART_THEME["layout"])
    return fig

def create_line_chart(df, x_col, y_col):
    fig = px.line(df, x=x_col, y=y_col, color_discrete_sequence=["#845EC2"])
    fig.update_layout(DART_THEME["layout"])
    return fig

def create_heatmap(df):
    corr = df.select_dtypes(include=['number']).corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="Viridis")
    fig.update_layout(DART_THEME["layout"])
    return fig
