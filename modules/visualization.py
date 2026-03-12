import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class VisualizationModule:
    """Module for generating 17 different interactive Plotly charts."""
    
    @staticmethod
    def get_color_scales():
        return ["Viridis", "Plasma", "Inferno", "Magma", "Cividis", "Blues", "Reds", "Greens", "Purples", "RdBu_r"]

    @staticmethod
    def plot(chart_type, df, x=None, y=None, color=None, size=None, hover=None, anim=None, aggregation=None, color_scale="Viridis"):
        """Dispatches to specific plot methods based on chart_type."""
        
        # Prepare data for aggregation if needed
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

        # Define common layout parameters
        layout_args = {
            "template": "plotly_dark",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
        }

        try:
            if chart_type == "Bar Chart":
                fig = px.bar(plot_df, x=x, y=y, color=color, barmode='group', template="plotly_dark", color_continuous_scale=color_scale)
            
            elif chart_type == "Line Chart":
                fig = px.line(plot_df, x=x, y=y, color=color, template="plotly_dark", markers=True)
            
            elif chart_type == "Scatter Plot":
                fig = px.scatter(plot_df, x=x, y=y, color=color, size=size, hover_name=hover, 
                                 trendline="ols" if aggregation == "OLS Trendline" else None, template="plotly_dark")
            
            elif chart_type == "Pie / Donut Chart":
                fig = px.pie(plot_df, names=x, values=y, hole=0.4 if "Donut" in chart_type else 0, template="plotly_dark")
            
            elif chart_type == "Box Plot":
                fig = px.box(plot_df, x=x, y=y, color=color, points="all", template="plotly_dark")
            
            elif chart_type == "Violin Plot":
                fig = px.violin(plot_df, x=x, y=y, color=color, box=True, points="all", template="plotly_dark")
            
            elif chart_type == "Heatmap":
                corr = df.select_dtypes(include=[np.number]).corr()
                fig = px.imshow(corr, text_auto=True, color_continuous_scale=color_scale, template="plotly_dark")
            
            elif chart_type == "Histogram":
                fig = px.histogram(plot_df, x=x, color=color, marginal="box", template="plotly_dark")
            
            elif chart_type == "Bubble Chart":
                fig = px.scatter(plot_df, x=x, y=y, size=size, color=color, hover_name=hover, size_max=60, template="plotly_dark")
            
            elif chart_type == "Treemap":
                fig = px.treemap(plot_df, path=x if isinstance(x, list) else [x], values=y, color=color, template="plotly_dark")
            
            elif chart_type == "Sunburst":
                fig = px.sunburst(plot_df, path=x if isinstance(x, list) else [x], values=y, color=color, template="plotly_dark")
            
            elif chart_type == "3D Scatter Plot":
                # Expecting y to be a list [y, z]
                z_col = y[1] if isinstance(y, list) and len(y) > 1 else x
                y_col = y[0] if isinstance(y, list) else y
                fig = px.scatter_3d(plot_df, x=x, y=y_col, z=z_col, color=color, size=size, template="plotly_dark")
            
            elif chart_type == "Radar / Spider Chart":
                # Using mean values per category
                radar_df = df.select_dtypes(include=[np.number]).mean().reset_index()
                radar_df.columns = ['theta', 'r']
                fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, template="plotly_dark")
                fig.update_traces(fill='toself')
            
            elif chart_type == "Area Chart":
                fig = px.area(plot_df, x=x, y=y, color=color, template="plotly_dark")
            
            elif chart_type == "Funnel Chart":
                fig = px.funnel(plot_df, x=x, y=y, color=color, template="plotly_dark")
            
            elif chart_type == "Parallel Coordinates":
                cols = df.select_dtypes(include=[np.number]).columns.tolist()
                fig = px.parallel_coordinates(df, columns=cols, color=color, color_continuous_scale=color_scale, template="plotly_dark")
            
            elif chart_type == "Pair Plot (Scatter Matrix)":
                cols = df.select_dtypes(include=[np.number]).columns.tolist()
                fig = px.scatter_matrix(df, dimensions=cols, color=color, template="plotly_dark")
            
            else:
                return None
            
            fig.update_layout(**layout_args)
            return fig
            
        except Exception as e:
            print(f"Viz Error: {e}")
            return None
