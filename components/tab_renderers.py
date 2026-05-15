import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import uuid
import time
import logging
from modules.data_loader import DataLoader
from modules.eda import EDAModule
from modules.visualization import VisualizationModule
from modules.ml_models import MLModule
from modules.chatbot import ChatbotModule
from modules.exporter import ExporterModule
from utils.theme import glass_card, render_hero

logger = logging.getLogger(__name__)


def render_upload_tab(doc_collection, embedder):
    render_hero(
        "Data Portal", 
        "Upload your CSV or Excel files to begin the intelligence cycle.", 
        icon="📥",
        bg_image="assets/hero_upload.png"
    )
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file", type=["csv", "xlsx", "xls"]
    )

    if uploaded_file:
        if st.session_state.file_name != uploaded_file.name:
            df, error = DataLoader.load_file(uploaded_file)
            if error:
                st.error(error)
            else:
                st.session_state.df = df
                st.session_state.df_original = df.copy()
                st.session_state.file_name = uploaded_file.name

                # Use Case B: Document RAG Chunking
                if doc_collection and embedder:
                    try:
                        text_content = df.to_csv(index=False)
                        chunks = []
                        chunk_size = 500
                        overlap = 50
                        start = 0
                        while start < len(text_content):
                            end = min(start + chunk_size, len(text_content))
                            chunks.append(text_content[start:end])
                            start += chunk_size - overlap

                        for i, chunk in enumerate(chunks):
                            vector = embedder.encode(chunk).tolist()
                            chunk_id = (
                                f"{uploaded_file.name}_chunk_{i}_{uuid.uuid4().hex[:8]}"
                            )
                            doc_collection.add(
                                embeddings=[vector],
                                documents=[chunk],
                                metadatas=[
                                    {"file_name": uploaded_file.name, "chunk_id": i}
                                ],
                                ids=[chunk_id],
                            )
                    except Exception as e:
                        logger.warning("Failed to chunk document for RAG: %s", e)

                st.rerun()

    if st.session_state.df is not None:
        stats = DataLoader.get_stats(st.session_state.df)
        st.markdown('<div class="meta-label">NEXUS TELEMETRY</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        
        metrics = [
            ("ROWS", f"{stats['rows']:,}", "📊"),
            ("COLUMNS", f"{stats['cols']:,}", "📐"),
            ("DATA VOID", f"{stats['null_pct']:.1f}%", "🕳️"),
            ("CLONES", f"{stats['duplicates']:,}", "👥")
        ]
        
        for i, (label, val, icon) in enumerate(metrics):
            cols = [c1, c2, c3, c4]
            with cols[i]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <div style="font-size: 1.5rem; margin-bottom: 5px;">{icon}</div>
                    <div class="meta-label" style="font-size: 0.6rem;">{label}</div>
                    <div style="font-size: 1.8rem; font-weight: 800; font-family: 'Syne', sans-serif; color: #00D2FF;">{val}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("Data Preview")
        rows = st.slider("Preview Rows", 5, 100, 10)
        st.dataframe(st.session_state.df.head(rows), use_container_width=True)

        st.subheader("Data Cleaning")
        cc1, cc2, cc3 = st.columns(3)
        if cc1.button("Drop Duplicates"):
            st.session_state.df = DataLoader.clean_data(
                st.session_state.df, "drop_duplicates"
            )
            st.success("Duplicates dropped!")
        if cc2.button("Fill Nulls (Mean)"):
            st.session_state.df = DataLoader.clean_data(
                st.session_state.df, "fill_nulls_mean"
            )
            st.success("Numeric nulls filled!")
        if cc3.button("Drop Any Nulls"):
            st.session_state.df = DataLoader.clean_data(
                st.session_state.df, "drop_any_nulls"
            )
            st.success("Rows with nulls removed!")


def render_eda_tab():
    if st.session_state.df is not None:
        eda = EDAModule()
        render_hero(
            "Lens of Discovery", 
            "Deep-dive statistical scanning and quality auditing.", 
            icon="🔬",
            bg_image="assets/hero_eda.png"
        )

        with st.expander("Statistical Summary", expanded=True):
            summary = eda.statistical_summary(st.session_state.df)
            if "numeric" in summary:
                st.write("**Numerical Features**")
                st.dataframe(summary["numeric"])
            if "categorical" in summary:
                st.write("**Categorical Features**")
                st.dataframe(summary["categorical"])

        with st.expander("Correlation Analysis"):
            corr, pairs = eda.correlation_analysis(st.session_state.df)
            if corr is not None:
                fig = px.imshow(
                    corr,
                    text_auto=True,
                    template="plotly_dark",
                    color_continuous_scale="Viridis",
                )
                st.plotly_chart(fig, use_container_width=True)
                st.write("**Top Correlated Pairs**")
                st.dataframe(pairs)
            else:
                st.warning("Needs numeric columns for correlation.")

        st.info("Full EDA Report runs all analytical modules on the current dataset.")
    else:
        st.warning("Please upload a file first.")


def render_viz_tab():
    if st.session_state.df is not None:
        render_hero(
            "Visual Galaxy", 
            "Transform raw dimensions into high-fidelity narratives.", 
            icon="🎨",
            bg_image="assets/hero_viz.png"
        )
        viz = VisualizationModule()

        # Categorized Visualization Engine
        viz_categories = {
            "📊 Distribution": ["Histogram", "KDE Plot", "Box Plot", "Violin Plot", "Strip Plot", "Swarm Plot", "ECDF Plot", "Rug Plot", "Ridge Plot", "Q-Q Plot"],
            "📈 Comparison": ["Bar Chart", "Horizontal Bar", "Grouped Bar", "Stacked Bar", "Lollipop Chart", "Dot Plot", "Dumbbell Plot", "Bullet Chart"],
            "🔗 Relationship": ["Scatter Plot", "Bubble Chart", "3D Scatter Plot", "Scatter Matrix (Pair Plot)", "Heatmap (Correlation)", "Density Heatmap", "Density Contour", "Joint Plot", "Hexbin Plot"],
            "🍕 Composition": ["Pie Chart", "Donut Chart", "Sunburst", "Treemap", "Waterfall Chart", "Waffle Chart", "Stacked Area"],
            "⌛ Time Series": ["Line Chart", "Area Chart", "Candlestick (Time Series)", "OHLC Chart", "Step Chart"],
            "🌊 Flow & Map": ["Sankey Diagram", "Funnel Chart", "Funnel Area", "Parallel Coordinates", "Parallel Categories", "Radar / Spider Chart", "Choropleth Map", "Scatter Mapbox", "Scatter Geo"]
        }

        col1, col2 = st.columns([1, 2.5])
        
        with col1:
            st.markdown("### 🛠️ Configuration")
            category = st.radio("Galaxy Category", list(viz_categories.keys()))
            chart_type = st.selectbox("Select Target Visualization", viz_categories[category])
            
            st.markdown("---")
            all_cols = st.session_state.df.columns.tolist()
            x_ax = st.selectbox("X Axis (Primary)", all_cols)
            y_ax = st.selectbox("Y Axis (Secondary)", [None] + all_cols)
            color_ax = st.selectbox("Color Mapping", [None] + all_cols)
            
            with st.expander("Advanced Optics"):
                agg = st.selectbox("Aggregation Engine", [None, "Sum", "Mean", "Count", "Max", "Min", "OLS Trendline"])
                scale = st.selectbox("Chromatic Scale", viz.get_color_scales())

        with col2:
            with st.container(border=True):
                fig = viz.plot(
                    chart_type,
                    st.session_state.df,
                    x=x_ax,
                    y=y_ax,
                    color=color_ax,
                    aggregation=agg,
                    color_scale=scale,
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Action Bar
                    ac1, ac2 = st.columns(2)
                    if ac1.checkbox("🔬 Show Raw Extraction", value=False):
                        st.dataframe(st.session_state.df[[x_ax] + ([y_ax] if y_ax else [])].head(50), use_container_width=True)
                else:
                    st.error("Engine Refusal: Incompatible column types for this visualization.")
    else:
        st.warning("Nexus System: Please upload a data source to initialize the Visual Studio.")


def render_ml_tab():
    if st.session_state.df is not None:
        ml = MLModule()
        render_hero(
            "ML Studio", 
            "Configure, train, and monitor your model in one workflow", 
            icon="🧠",
            bg_image="assets/hero_ml.png"
        )

        task_type = st.radio(
            "Select ML Task",
            ["Classification", "Regression", "Clustering"],
            horizontal=True,
        )

        if task_type in ["Classification", "Regression"]:
            target = st.selectbox("Select Target Column", st.session_state.df.columns)
            
            # Basic Validation
            unique_vals = st.session_state.df[target].nunique()
            if task_type == "Classification":
                if unique_vals < 2:
                    st.error("Target column must have at least 2 unique classes for classification.")
                    return
                if unique_vals > 50:
                    st.warning(f"Target has {unique_vals} unique values. Classification might be slow or inappropriate.")

            X, y = ml.preprocess(st.session_state.df, target, task=task_type.lower())

            model_list = (
                list(ml.classification_models.keys())
                if task_type == "Classification"
                else list(ml.regression_models.keys())
            )
            selected_model = st.selectbox("Select Model", model_list)

            if st.button(f"Train {selected_model}"):
                with st.spinner("Training model..."):
                    try:
                        if task_type == "Classification":
                            metrics, cm, importance = ml.train_classification(
                                X, y, selected_model
                            )
                            st.session_state.ml_results = {
                                "metrics": metrics,
                                "cm": cm,
                                "importance": importance,
                                "type": "class",
                            }
                        else:
                            metrics, y_test, y_pred = ml.train_regression(
                                X, y, selected_model
                            )
                            st.session_state.ml_results = {
                                "metrics": metrics,
                                "y_test": y_test,
                                "y_pred": y_pred,
                                "type": "reg",
                            }
                    except Exception as e:
                        st.error(f"Engine Failure: {str(e)}")
                        logger.error(f"ML Training Error: {e}", exc_info=True)

        if st.session_state.ml_results:
            res = st.session_state.ml_results
            st.subheader("Performance Metrics")
            cols = st.columns(len(res["metrics"]))
            for i, (k, v) in enumerate(res["metrics"].items()):
                cols[i].metric(k, f"{v:.4f}")

            if res.get("type") == "class":
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Confusion Matrix**")
                    fig = px.imshow(res["cm"], text_auto=True, template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    if res["importance"] is not None:
                        st.write("**Feature Importance**")
                        fig = px.bar(
                            res["importance"].head(10),
                            x="Importance",
                            y="Feature",
                            orientation="h",
                            template="plotly_dark",
                        )
                        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please upload a file first.")


def render_chat_tab(chroma_client, embedder, chat_collection, doc_collection):
    if st.session_state.df is not None:
        render_hero(
            "Neural Chat", 
            "Ask anything about your data. Get code, charts, and insights instantly.", 
            icon="💬",
            bg_image="assets/hero_chat.png"
        )
        bot = ChatbotModule(
            groq_key=st.session_state.get('groq_key'),
            gemini_key=st.session_state.get('gemini_key')
        )
        
        # Action Bar
        col_m1, col_m2 = st.columns([4, 1])
        with col_m2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        # Chat container
        chat_container = st.container(height=550)
        with chat_container:
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "assistant"
                with st.chat_message(role):
                    st.markdown(msg["content"])
                    if role == "assistant" and "```python" in msg["content"]:
                        from services.execution_service import execute_code_blocks
                        execute_code_blocks(msg["content"], st.session_state.df)

        if prompt := st.chat_input("Query the Nexus..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Neural Cache Lookup..."):
                    # --- SEMANTIC CACHE LAYER ---
                    cached_answer = None
                    if chat_collection and embedder:
                        try:
                            q_vector = embedder.encode(prompt).tolist()
                            cache_res = chat_collection.query(
                                query_embeddings=[q_vector], 
                                n_results=1,
                                where={"role": "assistant"} # Only pull AI answers
                            )
                            if cache_res and cache_res['distances'] and cache_res['distances'][0]:
                                distance = cache_res['distances'][0][0]
                                # If distance is very low (high similarity), use cache
                                if distance < 0.1: 
                                    cached_answer = cache_res['documents'][0][0]
                                    st.caption("🚀 Retrieved from Zero-Token Neural Cache")
                        except Exception as e:
                            logger.warning(f"Cache lookup failed: {e}")

                if cached_answer:
                    st.markdown(cached_answer)
                    st.session_state.messages.append({"role": "assistant", "content": cached_answer})
                    # Re-execute code if present in cache
                    from services.execution_service import execute_code_blocks
                    execute_code_blocks(cached_answer, st.session_state.df)
                else:
                    with st.spinner("AI is thinking..."):
                        # Use the consolidated ask method
                        response_data = bot.ask(prompt, st.session_state.df, st.session_state.messages)
                        
                        answer = response_data.get("answer", "Error in processing.")
                        code = response_data.get("python_code", "")
                        
                        st.markdown(answer)
                        if code:
                            from services.execution_service import execute_code_blocks
                            execute_code_blocks(f"```python\n{code}\n```", st.session_state.df)
                        
                        full_reply = f"{answer}\n\n```python\n{code}\n```" if code else answer
                        st.session_state.messages.append({"role": "assistant", "content": full_reply})
                        
                        # Store in Neural Cache
                        if chat_collection and embedder:
                            try:
                                import time, uuid
                                vector = embedder.encode(full_reply).tolist()
                                chat_collection.add(
                                    embeddings=[vector],
                                    documents=[full_reply],
                                    metadatas=[{"role": "assistant", "timestamp": time.time(), "session_id": st.session_state.session_id}],
                                    ids=[f"cache_{uuid.uuid4().hex}"]
                                )
                            except Exception as e:
                                logger.warning("Failed to store cache embedding: %s", e)
    else:
        st.warning("Nexus System: Please upload a data source to initialize the Neural Chat.")


def render_export_tab():
    if st.session_state.df is not None:
        render_hero(
            "Export Vault", 
            "Download your cleaned data and generated assets", 
            icon="🔒",
            bg_image="assets/hero_export.png"
        )
        exp = ExporterModule()
        fname = st.text_input(
            "Filename",
            value=f"data_nexus_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}",
        )

        ec1, ec2, ec3, ec4 = st.columns(4)
        ec1.download_button(
            "Download CSV", exp.to_csv(st.session_state.df), f"{fname}.csv", "text/csv"
        )
        ec2.download_button(
            "Download Excel", exp.to_excel(st.session_state.df), f"{fname}.xlsx"
        )
        ec3.download_button(
            "Download JSON", exp.to_json(st.session_state.df), f"{fname}.json"
        )
        ec4.download_button(
            "Download PDF", exp.to_pdf(st.session_state.df), f"{fname}.pdf"
        )

        ec5, ec6, ec7, ec8 = st.columns(4)
        ec5.download_button(
            "Download SQL", exp.to_sql(st.session_state.df), f"{fname}.sql"
        )
        ec6.download_button(
            "Download Word", exp.to_word(st.session_state.df), f"{fname}.docx"
        )
        ec7.download_button(
            "Download Markdown", exp.to_markdown(st.session_state.df), f"{fname}.md"
        )
        ec8.download_button(
            "Download HTML", exp.to_html(st.session_state.df), f"{fname}.html"
        )
    else:
        st.warning("Please upload a file first.")


# End of Tab Renderers

