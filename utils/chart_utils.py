import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Premium Dark Theme configuration for Plotly
DARK_THEME_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "#FFFFFF", "family": "Inter"},
    "xaxis": {"gridcolor": "rgba(255,255,255,0.1)", "zerolinecolor": "rgba(255,255,255,0.1)"},
    "yaxis": {"gridcolor": "rgba(255,255,255,0.1)", "zerolinecolor": "rgba(255,255,255,0.1)"},
    "colorway": ["#6C63FF", "#00C9A7", "#845EC2", "#FF7171", "#FFDE69", "#4BADE8", "#FF9671"]
}

def apply_theme(fig):
    fig.update_layout(DARK_THEME_LAYOUT)
    return fig

# --- 1. Distribution Charts ---
def create_histogram(df, x):
    return apply_theme(px.histogram(df, x=x, marginal="box"))

def create_box_plot(df, y, x=None):
    return apply_theme(px.box(df, x=x, y=y, points="all"))

def create_violin_plot(df, y, x=None):
    return apply_theme(px.violin(df, x=x, y=y, box=True, points="all"))

def create_strip_plot(df, y, x=None):
    return apply_theme(px.strip(df, x=x, y=y))

def create_ecdf_plot(df, x):
    return apply_theme(px.ecdf(df, x=x))

# --- 2. Composition / Part-to-Whole ---
def create_pie_chart(df, names, values=None):
    if values:
        return apply_theme(px.pie(df, names=names, values=values, hole=0.4))
    counts = df[names].value_counts().reset_index()
    return apply_theme(px.pie(counts, names=names, values='count', hole=0.4))

def create_sunburst(df, path, values=None):
    return apply_theme(px.sunburst(df, path=path, values=values))

def create_treemap(df, path, values=None):
    return apply_theme(px.treemap(df, path=path, values=values))

def create_funnel(df, x, y):
    return apply_theme(px.funnel(df, x=x, y=y))

# --- 3. Relationship Charts ---
def create_scatter_plot(df, x, y, color=None, size=None, trendline=None):
    return apply_theme(px.scatter(df, x=x, y=y, color=color, size=size, trendline=trendline))

def create_scatter_matrix(df, dimensions, color=None):
    return apply_theme(px.scatter_matrix(df, dimensions=dimensions, color=color))

def create_density_contour(df, x, y):
    return apply_theme(px.density_contour(df, x=x, y=y))

def create_density_heatmap(df, x, y):
    return apply_theme(px.density_heatmap(df, x=x, y=y))

# --- 4. Trend / Time Series ---
def create_line_chart(df, x, y, color=None):
    return apply_theme(px.line(df, x=x, y=y, color=color))

def create_area_chart(df, x, y, color=None):
    return apply_theme(px.area(df, x=x, y=y, color=color))

# --- 5. 3D Charts ---
def create_3d_scatter(df, x, y, z, color=None):
    return apply_theme(px.scatter_3d(df, x=x, y=y, z=z, color=color))

# --- 6. Specialized ---
def create_parallel_categories(df, dimensions, color=None):
    return apply_theme(px.parallel_categories(df, dimensions=dimensions, color=color))

def create_parallel_coordinates(df, dimensions, color=None):
    return apply_theme(px.parallel_coordinates(df, dimensions=dimensions, color=color))

def create_heatmap(df):
    corr = df.select_dtypes(include=['number']).corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="Viridis")
    return apply_theme(fig)
