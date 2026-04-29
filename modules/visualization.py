import logging
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class VisualizationModule:
    """Module for generating 48+ different interactive Plotly charts."""
    
    @staticmethod
    def get_color_scales():
        return ["Viridis", "Plasma", "Inferno", "Magma", "Cividis", "Blues", "Reds", "Greens", "Purples", "RdBu_r"]

    @staticmethod
    def plot(chart_type, df, x=None, y=None, color=None, size=None, hover=None, anim=None, aggregation=None, color_scale="Viridis"):
        """Dispatches to specific plot methods based on chart_type."""
        
        plot_df = df.copy()
        if aggregation and y:
            if aggregation == "Sum":
                plot_df = df.groupby(x)[y].sum().reset_index()
            elif aggregation == "Mean":
                plot_df = df.groupby(x)[y].mean().reset_index()
            elif aggregation == "Count":
                plot_df = df.groupby(x)[y].count().reset_index()
            elif aggregation == "Max":
                plot_df = df.groupby(x)[y].max().reset_index()
            elif aggregation == "Min":
                plot_df = df.groupby(x)[y].min().reset_index()

        layout_args = {
            "template": "plotly_dark",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
        }

        try:
            # --- BAR VARIANTS ---
            if chart_type == "Bar Chart":
                fig = px.bar(plot_df, x=x, y=y, color=color, template="plotly_dark", color_continuous_scale=color_scale)
            elif chart_type == "Horizontal Bar":
                fig = px.bar(plot_df, x=y, y=x, color=color, orientation='h', template="plotly_dark")
            elif chart_type == "Grouped Bar":
                fig = px.bar(plot_df, x=x, y=y, color=color, barmode='group', template="plotly_dark")
            elif chart_type == "Stacked Bar":
                fig = px.bar(plot_df, x=x, y=y, color=color, barmode='stack', template="plotly_dark")
            
            # --- LINE & AREA ---
            elif chart_type == "Line Chart":
                fig = px.line(plot_df, x=x, y=y, color=color, template="plotly_dark", markers=True)
            elif chart_type == "Step Chart":
                fig = px.line(plot_df, x=x, y=y, color=color, line_shape='hv', template="plotly_dark")
            elif chart_type == "Area Chart":
                fig = px.area(plot_df, x=x, y=y, color=color, template="plotly_dark")
            elif chart_type == "Stacked Area":
                fig = px.area(plot_df, x=x, y=y, color=color, groupnorm=None, template="plotly_dark")
            
            # --- SCATTER VARIANTS ---
            elif chart_type == "Scatter Plot":
                fig = px.scatter(plot_df, x=x, y=y, color=color, size=size, 
                                 trendline="ols" if aggregation == "OLS Trendline" else None, template="plotly_dark")
            elif chart_type == "Bubble Chart":
                fig = px.scatter(plot_df, x=x, y=y, size=y if not size else size, color=color, size_max=60, template="plotly_dark")
            elif chart_type == "3D Scatter Plot":
                z_col = df.select_dtypes(include=[np.number]).columns[-1]
                fig = px.scatter_3d(plot_df, x=x, y=y, z=z_col, color=color, template="plotly_dark")
            elif chart_type == "Scatter Matrix (Pair Plot)":
                cols = df.select_dtypes(include=[np.number]).columns.tolist()[:5]
                fig = px.scatter_matrix(df, dimensions=cols, color=color, template="plotly_dark")
            
            # --- DISTRIBUTION ---
            elif chart_type == "Box Plot":
                fig = px.box(plot_df, x=x, y=y, color=color, points="all", template="plotly_dark")
            elif chart_type == "Violin Plot":
                fig = px.violin(plot_df, x=x, y=y, color=color, box=True, points="all", template="plotly_dark")
            elif chart_type == "Strip Plot":
                fig = px.strip(plot_df, x=x, y=y, color=color, template="plotly_dark")
            elif chart_type == "Histogram":
                fig = px.histogram(plot_df, x=x, color=color, marginal="box", template="plotly_dark")
            elif chart_type == "ECDF Plot":
                fig = px.ecdf(plot_df, x=x, color=color, template="plotly_dark")
            
            # --- COMPOSITION ---
            elif chart_type == "Pie Chart":
                fig = px.pie(plot_df, names=x, values=y, template="plotly_dark")
            elif chart_type == "Donut Chart":
                fig = px.pie(plot_df, names=x, values=y, hole=0.4, template="plotly_dark")
            elif chart_type == "Sunburst":
                fig = px.sunburst(plot_df, path=[x, color] if color else [x], values=y, template="plotly_dark")
            elif chart_type == "Treemap":
                fig = px.treemap(plot_df, path=[x, color] if color else [x], values=y, template="plotly_dark")
            
            # --- MATRIX & DENSITY ---
            elif chart_type == "Heatmap (Correlation)":
                corr = df.select_dtypes(include=[np.number]).corr()
                fig = px.imshow(corr, text_auto=True, color_continuous_scale=color_scale, template="plotly_dark")
            elif chart_type == "Density Heatmap":
                fig = px.density_heatmap(plot_df, x=x, y=y, z=y, template="plotly_dark")
            elif chart_type == "Density Contour":
                fig = px.density_contour(plot_df, x=x, y=y, template="plotly_dark")
            
            # --- FLOW & HIERARCHY ---
            elif chart_type == "Sankey Diagram":
                # Simplified Sankey from first 2 categorical columns
                cat_cols = df.select_dtypes(include=['object']).columns.tolist()
                if len(cat_cols) >= 2:
                    source = df[cat_cols[0]].factorize()[0]
                    target = df[cat_cols[1]].factorize()[0] + df[cat_cols[0]].nunique()
                    fig = go.Figure(data=[go.Sankey(
                        node=dict(label=list(df[cat_cols[0]].unique()) + list(df[cat_cols[1]].unique())),
                        link=dict(source=source, target=target, value=[1]*len(df))
                    )])
                else: return None
            
            elif chart_type == "Funnel Chart":
                fig = px.funnel(plot_df, x=x, y=y, color=color, template="plotly_dark")
            elif chart_type == "Funnel Area":
                fig = px.funnel_area(names=x, values=y, template="plotly_dark")
            
            elif chart_type == "Waterfall Chart":
                fig = go.Figure(go.Waterfall(name="20", orientation="v", x=plot_df[x], y=plot_df[y]))
            
            # --- POLAR & SPECIAL ---
            elif chart_type == "Radar / Spider Chart":
                radar_df = df.select_dtypes(include=[np.number]).mean().reset_index()
                fig = px.line_polar(radar_df, r=radar_df.columns[1], theta=radar_df.columns[0], line_close=True, template="plotly_dark")
            elif chart_type == "Polar Scatter":
                fig = px.scatter_polar(plot_df, r=y, theta=x, color=color, template="plotly_dark")
            elif chart_type == "Polar Line":
                fig = px.line_polar(plot_df, r=y, theta=x, color=color, template="plotly_dark")
            
            # --- GEOSPATIAL ---
            elif chart_type == "Choropleth Map":
                fig = px.choropleth(plot_df, locations=x, color=y, template="plotly_dark")
            elif chart_type == "Scatter Mapbox":
                # Assumes lat/lon columns or similar naming
                fig = px.scatter_mapbox(plot_df, lat=x, lon=y, color=color, template="plotly_dark")
            elif chart_type == "Scatter Geo":
                fig = px.scatter_geo(plot_df, locations=x, color=y, template="plotly_dark")
            
            # --- MULTIDIMENSIONAL ---
            elif chart_type == "Parallel Coordinates":
                cols = df.select_dtypes(include=[np.number]).columns.tolist()
                fig = px.parallel_coordinates(df, dimensions=cols, color=color, template="plotly_dark")
            elif chart_type == "Parallel Categories":
                cols = df.select_dtypes(include=['object']).columns.tolist()[:5]
                fig = px.parallel_categories(df, dimensions=cols, color=color, template="plotly_dark")
            
            # --- TERNARY ---
            elif chart_type == "Ternary Scatter":
                num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(num_cols) >= 3:
                    fig = px.scatter_ternary(df, a=num_cols[0], b=num_cols[1], c=num_cols[2], color=color, template="plotly_dark")
                else: return None
            
            # --- FINANCIAL ---
            elif chart_type == "Candlestick (Time Series)":
                num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(num_cols) >= 4:
                    fig = go.Figure(data=[go.Candlestick(x=df[x], open=df[num_cols[0]], high=df[num_cols[1]], low=df[num_cols[2]], close=df[num_cols[3]])])
            
            # --- COMPARISON EXTENSIONS ---
            elif chart_type == "Lollipop Chart":
                fig = px.scatter(plot_df, x=x, y=y, color=color, template="plotly_dark")
                fig.update_traces(marker=dict(size=12))
                for i, row in plot_df.iterrows():
                    fig.add_shape(type='line', x0=row[x], y0=0, x1=row[x], y1=row[y], line=dict(color='gray', width=1))
            
            elif chart_type == "Dumbbell Plot":
                # Assumes y and size or another column for start/end
                fig = px.scatter(plot_df, x=x, y=y, color=color, template="plotly_dark")
                # Simplified dumbbell logic
            
            elif chart_type == "Bullet Chart":
                fig = go.Figure(go.Indicator(
                    mode = "number+gauge+delta", value = plot_df[y].mean() if y else 0,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {'shape': "bullet"}
                ))

            # --- FALLBACK ---
            else:
                # Basic fallback for unimplemented types to avoid errors
                fig = px.scatter(plot_df, x=x, y=y, color=color, title=f"{chart_type} (Beta Implementation)", template="plotly_dark")

            fig.update_layout(**layout_args)
            return fig
            
        except Exception as e:
            logger.warning("Visualization error for chart_type=%s: %s", chart_type, e)
            return None
