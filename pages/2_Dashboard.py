import streamlit as st
import pandas as pd
from utils.theme import load_css, glass_card, render_hero
from utils.navigation import sidebar_nav
from utils.data_utils import get_df_summary, infer_column_types
import utils.chart_utils as charts

st.set_page_config(page_title="DataNexusAI - Visual Studio", page_icon="📊", layout="wide")
load_css()
sidebar_nav(1)

if st.session_state.get('df') is None:
    st.warning("No data universe detected. Please connect a dataset first.")
    if st.button("Go to Upload"):
        st.switch_page("pages/3_Upload.py")
    st.stop()

df = st.session_state['df']
summary = get_df_summary(df)
numeric_cols, categorical_cols, datetime_cols = infer_column_types(df)

render_hero("Platform Pulse", "Live metrics and activity overview for your ML workspace")

# --- Top Metrics Bar ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Universe Scale (Rows)", f"{summary['rows']:,}")
m2.metric("Dimensionality", summary['cols'])
m3.metric("Numeric Nodes", summary['numeric_cols'])
m4.metric("Categories", summary['categorical_cols'])

# --- Activity & Trends Row ---
st.write("")
c_feed, c_trend = st.columns([1, 1])

with c_feed:
    st.markdown("### 📡 Live Activity Feed")
    feed_items = [
        ("ML Studio", "Neural Forge initiated for 'XGBoost'", "2m ago", "🟢"),
        ("Data Nexus", "New dataset 'customer_v2.csv' linked", "15m ago", "🔵"),
        ("Neural Chat", "Analytical query: 'Show sales trend'", "1h ago", "✨")
    ]
    for source, text, time, icon in feed_items:
        st.markdown(f"""
        <div class="glass-card" style="padding: 1rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div style="flex: 1;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #6C63FF; font-size: 0.8rem;">{source.upper()}</strong>
                    <span style="opacity: 0.4; font-size: 0.7rem;">{time}</span>
                </div>
                <div style="font-size: 0.95rem; opacity: 0.8;">{text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with c_trend:
    st.markdown("### 📈 Neural Performance Trend")
    # Mock sparkline
    import numpy as np
    import plotly.graph_objects as go
    
    x = np.linspace(0, 10, 20)
    y = np.sin(x) * 0.2 + 0.8 + np.random.normal(0, 0.05, 20)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', line=dict(color='#00C9A7', width=3), fillcolor='rgba(0, 201, 167, 0.1)'))
    fig.update_layout(
        height=180, margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('<p style="text-align:center; opacity:0.5; font-size:0.8rem;">Nexus Processing Efficiency: +12.4% (Last 24h)</p>', unsafe_allow_html=True)

st.write("---")

# --- Visual Universe Studio ---
st.markdown("### 🌌 Studio Explorer")
tabs = st.tabs(["📈 Distribution", "🔗 Relationship", "🍕 Composition", "🕒 Trend", "🛰️ 3D & Advanced"])

with tabs[0]: # Distribution
    st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
    d_col1, d_col2 = st.columns([1, 3])
    with d_col1:
        st.markdown("#### Config")
        x_dist = st.selectbox("Numeric Node", numeric_cols, key="dist_x")
        chart_type = st.radio("Technique", [
            "Histogram (with Box)", "Box Plot", "Violin Plot", "Strip Plot", "ECDF Plot"
        ])
    with d_col2:
        with st.container(border=True):
            if chart_type == "Histogram (with Box)":
                st.plotly_chart(charts.create_histogram(df, x_dist), use_container_width=True)
            elif chart_type == "Box Plot":
                st.plotly_chart(charts.create_box_plot(df, y=x_dist), use_container_width=True)
            elif chart_type == "Violin Plot":
                st.plotly_chart(charts.create_violin_plot(df, y=x_dist), use_container_width=True)
            elif chart_type == "Strip Plot":
                st.plotly_chart(charts.create_strip_plot(df, y=x_dist), use_container_width=True)
            elif chart_type == "ECDF Plot":
                st.plotly_chart(charts.create_ecdf_plot(df, x=x_dist), use_container_width=True)

with tabs[1]: # Relationship
    st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
    r_col1, r_col2 = st.columns([1, 3])
    with r_col1:
        st.markdown("#### Config")
        rx = st.selectbox("Vector X", numeric_cols, key="rel_x")
        ry = st.selectbox("Vector Y", numeric_cols, key="rel_y")
        color_by = st.selectbox("Color Mapping", [None] + categorical_cols, key="rel_color")
        rel_type = st.radio("Connection Type", [
            "Scatter Plot", "Bubble Chart", "Density Contour", "Density Heatmap", "Correlation Matrix"
        ])
    with r_col2:
        with st.container(border=True):
            if rel_type == "Scatter Plot":
                st.plotly_chart(charts.create_scatter_plot(df, rx, ry, color=color_by), use_container_width=True)
            elif rel_type == "Bubble Chart":
                size_by = st.selectbox("Size Mapping", numeric_cols, key="rel_size")
                st.plotly_chart(charts.create_scatter_plot(df, rx, ry, color=color_by, size=size_by), use_container_width=True)
            elif rel_type == "Density Contour":
                st.plotly_chart(charts.create_density_contour(df, rx, ry), use_container_width=True)
            elif rel_type == "Density Heatmap":
                st.plotly_chart(charts.create_density_heatmap(df, rx, ry), use_container_width=True)
            elif rel_type == "Correlation Matrix":
                st.plotly_chart(charts.create_heatmap(df), use_container_width=True)

with tabs[2]: # Composition
    st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
    c_col1, c_col2 = st.columns([1, 3])
    with c_col1:
        st.markdown("#### Config")
        cat_col = st.selectbox("Categorical Core", categorical_cols, key="comp_cat")
        val_col = st.selectbox("Value Magnitude", [None] + numeric_cols, key="comp_val")
        comp_type = st.radio("Composition Logic", [
            "Pie Chart", "Donut Chart", "Sunburst", "Treemap", "Funnel Chart"
        ])
    with c_col2:
        with st.container(border=True):
            if comp_type in ["Pie Chart", "Donut Chart"]:
                st.plotly_chart(charts.create_pie_chart(df, cat_col, val_col), use_container_width=True)
            elif comp_type == "Sunburst":
                levels = st.multiselect("Hierarchy Levels", categorical_cols, default=[cat_col])
                if levels:
                    st.plotly_chart(charts.create_sunburst(df, levels, val_col), use_container_width=True)
            elif comp_type == "Treemap":
                levels = st.multiselect("Hierarchy Depth", categorical_cols, default=[cat_col], key="tree_levels")
                if levels:
                    st.plotly_chart(charts.create_treemap(df, levels, val_col), use_container_width=True)
            elif comp_type == "Funnel Chart":
                st.plotly_chart(charts.create_funnel(df, val_col if val_col else cat_col, cat_col), use_container_width=True)

with tabs[3]: # Trend
    st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
    t_col1, t_col2 = st.columns([1, 3])
    with t_col1:
        st.markdown("#### Config")
        time_col = st.selectbox("Timeline Axis", df.columns, key="trend_x")
        trend_y = st.selectbox("Value Vector", numeric_cols, key="trend_y")
        trend_type = st.radio("Trend Profile", ["Line Chart", "Area Chart"])
    with t_col2:
        with st.container(border=True):
            if trend_type == "Line Chart":
                st.plotly_chart(charts.create_line_chart(df, time_col, trend_y), use_container_width=True)
            else:
                st.plotly_chart(charts.create_area_chart(df, time_col, trend_y), use_container_width=True)

with tabs[4]: # 3D & Advanced
    st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
    a_col1, a_col2 = st.columns([1, 3])
    with a_col1:
        st.markdown("#### Config")
        adv_type = st.radio("Advanced Geometry", [
            "3D Scatter Plot", "Parallel Categories", "Parallel Coordinates", "Scatter Matrix"
        ])
    with a_col2:
        with st.container(border=True):
            if adv_type == "3D Scatter Plot":
                z3 = st.selectbox("Z Vector", numeric_cols, key="3d_z")
                st.plotly_chart(charts.create_3d_scatter(df, rx, ry, z3, color=color_by), use_container_width=True)
            elif adv_type == "Parallel Categories":
                dims = st.multiselect("Dimensions", categorical_cols, default=categorical_cols[:3])
                if dims: st.plotly_chart(charts.create_parallel_categories(df, dims, color=numeric_cols[0] if numeric_cols else None), use_container_width=True)
            elif adv_type == "Parallel Coordinates":
                dims = st.multiselect("Numeric Planes", numeric_cols, default=numeric_cols[:4])
                if dims: st.plotly_chart(charts.create_parallel_coordinates(df, dims), use_container_width=True)
            elif adv_type == "Scatter Matrix":
                dims = st.multiselect("Matrix Nodes", numeric_cols, default=numeric_cols[:3])
                if dims: st.plotly_chart(charts.create_scatter_matrix(df, dims, color=color_by), use_container_width=True)
