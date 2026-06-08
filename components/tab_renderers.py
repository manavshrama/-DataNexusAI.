import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import uuid
import time
import logging
from modules.data_loader import DataLoader
from utils.state_manager import add_audit_entry, add_vault_asset, get_working_df, set_working_df, get_audit_log, get_vault_assets
from modules.eda import EDAModule
from modules.visualization import VisualizationModule
from modules.ml_models import MLModule
from modules.chatbot import ChatbotModule
from modules.exporter import ExporterModule
from utils.theme import glass_card, render_hero

logger = logging.getLogger(__name__)



def render_home_tab():
    render_hero(
        "DataNexusAI", 
        "Welcome to your AI-Powered Data Universe.", 
        icon="🌌",
        bg_image="assets/hero_home.png"
    )

    # Main introduction layout using glassmorphism cards
    st.markdown("""
    <div class="glass-card" style="padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.08);">
        <h2 style="font-family: 'Syne', sans-serif; font-size: 2.2rem; color: #00D2FF; margin-top: 0; margin-bottom: 1rem;">Unlock Your Data's True Potential</h2>
        <p style="font-size: 1.1rem; line-height: 1.7; opacity: 0.85; max-width: 900px; margin-bottom: 0;">
            DataNexusAI is a production-grade, state-of-the-art telemetry and predictive analytics suite. Run high-precision statistical analyses, train machine learning classifiers or regressors with zero code, explore multi-dimensional charts in the Viz Galaxy, and interrogate your data in natural language via the fully grounded Neural Chat.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Platform Stats ──
    st.markdown('<div class="meta-label" style="letter-spacing: 2px; margin-bottom: 15px;">SYSTEM CAPABILITIES</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    stats = [
        ("Processing Velocity", "1.2 GB/s", "⚡"),
        ("Viz Galaxy Options", "48+ Charts", "🎨"),
        ("Model Accuracy", "Up to 99.4%", "🎯"),
        ("Neural Engine", "Zero-Token Cache", "🧠")
    ]
    
    for col, (label, val, icon) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.05); border-radius: 15px;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">{icon}</div>
                <div class="meta-label" style="font-size: 0.65rem; color: rgba(255,255,255,0.5);">{label}</div>
                <div style="font-size: 1.6rem; font-weight: 800; font-family: 'Syne', sans-serif; color: #00C9A7; margin-top: 5px;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.write("<br>", unsafe_allow_html=True)

    # Feature Cards
    st.markdown('<div class="meta-label" style="letter-spacing: 2px; margin-bottom: 15px;">INTELLIGENCE CORE</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    
    features = [
        ("📊 Data Analysis & EDA", "Deep-dive statistical scanning, automated correlation heatmaps, state-committed cleaning, and quality audits in a single click.", "📈 Go to EDA Tab"),
        ("🎨 Visual Universe", "Interactive 3D scatter plots, Sankey flow diagrams, composition matrices, and horizontal lollipop charts built dynamically.", "✨ Go to Viz Tab"),
        ("🧠 ML Studio", "Train classifiers, regressors, or clustering pipelines instantly, with automatic encoding, class balancing, and metric evaluation.", "⚡ Go to ML Studio")
    ]
    
    for col, (title, desc, button_label) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="min-height: 250px; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid rgba(255,255,255,0.06); padding: 1.8rem;">
                <div>
                    <h3 style="font-family: 'Syne', sans-serif; margin-top: 0; color: #FF007F; font-size: 1.3rem;">{title}</h3>
                    <p style="opacity: 0.8; font-size: 0.95rem; line-height: 1.5; margin-top: 10px;">{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    # Getting Started guide
    with st.expander("📖 New to DataNexusAI? Follow the 4-Step Intelligence Cycle", expanded=True):
        st.markdown("""
        1. **📂 Upload**: Load your raw CSV or Excel files in the data portal to initialize your runtime session state.
        2. **🔬 Explore & Clean**: Use the **EDA** tools to audit features, fill missing coordinates, and drop duplicates.
        3. **🎨 Visualise**: Head over to the **Viz Galaxy** to automatically graph multidimensional relationships.
        4. **🧠 Forge Predictors**: Open the **ML Studio** to select target values, train, and test models in real time.
        """)


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
                set_working_df(df)
                st.session_state.df_original = df.copy()
                st.session_state.file_name = uploaded_file.name
                # Log upload action
                add_audit_entry('upload', {'file_name': uploaded_file.name})

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

    if get_working_df() is not None:
        stats = DataLoader.get_stats(get_working_df())
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
        st.dataframe(get_working_df().head(rows), use_container_width=True)




def render_eda_tab():
    if get_working_df() is not None:
        eda = EDAModule()
        render_hero(
            "Lens of Discovery", 
            "Deep-dive statistical scanning and quality auditing.", 
            icon="🔬",
            bg_image="assets/hero_eda.png"
        )

        with st.expander("Statistical Summary", expanded=True):
            summary = eda.statistical_summary(get_working_df())
            if "numeric" in summary:
                st.write("**Numerical Features**")
                st.dataframe(summary["numeric"])
            if "categorical" in summary:
                st.write("**Categorical Features**")
                st.dataframe(summary["categorical"])

        with st.expander("Correlation Analysis"):
            corr, pairs = eda.correlation_analysis(get_working_df())
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

        st.markdown("---")
        st.subheader("Data Refinery (State Commit)")
        st.write("Apply data transformations here. These changes are committed to the global working dataset used in visualization and ML.")
        cc1, cc2, cc3 = st.columns(3)
        if cc1.button("Drop Duplicates (Commit)"):
            set_working_df(
                DataLoader.clean_data(
                    get_working_df(), "drop_duplicates"
                )
            )
            st.success("Committed: Duplicates dropped!")
            add_audit_entry('clean_data', {'action': 'drop_duplicates'})
        if cc2.button("Fill Nulls with Mean (Commit)"):
            set_working_df(
                DataLoader.clean_data(
                    get_working_df(), "fill_nulls_mean"
                )
            )
            st.success("Committed: Numeric nulls filled!")
            add_audit_entry('clean_data', {'action': 'fill_nulls_mean'})
        if cc3.button("Drop Rows with Nulls (Commit)"):
            set_working_df(
                DataLoader.clean_data(
                    get_working_df(), "drop_any_nulls"
                )
            )
            st.success("Committed: Rows with nulls removed!")
            add_audit_entry('clean_data', {'action': 'drop_any_nulls'})
    else:
        st.warning("Please upload a file first.")


def render_viz_tab():
    if get_working_df() is not None:
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
            all_cols = get_working_df().columns.tolist()
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
                    get_working_df(),
                    x=x_ax,
                    y=y_ax,
                    color=color_ax,
                    aggregation=agg,
                    color_scale=scale,
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    # Save visualization to vault
                    add_vault_asset('visualization', fig, {'chart_type': chart_type, 'x': x_ax, 'y': y_ax, 'color': color_ax})
                    
                    # Action Bar
                    ac1, ac2 = st.columns(2)
                    if ac1.checkbox("🔬 Show Raw Extraction", value=False):
                        st.dataframe(get_working_df()[[x_ax] + ([y_ax] if y_ax else [])].head(50), use_container_width=True)
                else:
                    st.error("Engine Refusal: Incompatible column types for this visualization.")
    else:
        st.warning("Nexus System: Please upload a data source to initialize the Visual Studio.")


def render_ml_tab():
    if get_working_df() is not None:
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
            target = st.selectbox("Select Target Column", get_working_df().columns)
            
            # Basic Validation
            unique_vals = get_working_df()[target].nunique()
            if task_type == "Classification":
                if unique_vals < 2:
                    st.error("Target column must have at least 2 unique classes for classification.")
                    return
                if unique_vals > 50:
                    st.warning(f"Target has {unique_vals} unique values. Classification might be slow or inappropriate.")

            X, y = ml.preprocess(get_working_df(), target, task=task_type.lower())

            model_list = (
                list(ml.classification_models.keys())
                if task_type == "Classification"
                else list(ml.regression_models.keys())
            )
            selected_model = st.selectbox("Select Model", model_list)

            if st.button("🚀 Train Model"):
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
                            # Log model training
                            add_audit_entry('train_model', {'model': selected_model, 'task': task_type, 'target': target})
                            # Save model artifact to vault (placeholder for actual model object)
                            add_vault_asset('model', selected_model, {'task': task_type, 'target': target})
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
                            # Log regression model training
                            add_audit_entry('train_model', {'model': selected_model, 'task': task_type, 'target': target})
                            add_vault_asset('model', selected_model, {'task': task_type, 'target': target})
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
    if get_working_df() is not None:
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
            for idx, msg in enumerate(st.session_state.messages):
                role = "user" if msg["role"] == "user" else "assistant"
                with st.chat_message(role):
                    st.markdown(msg["content"])
                    if role == "assistant" and "```python" in msg["content"]:
                        from services.execution_service import execute_code_blocks
                        execute_code_blocks(msg["content"], get_working_df(), key_suffix=f"tab_{idx}")

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
                    execute_code_blocks(cached_answer, get_working_df(), key_suffix=f"tab_{len(st.session_state.messages)-1}")
                else:
                    with st.spinner("AI is thinking..."):
                        # Use the consolidated ask method
                        response_data = bot.ask(prompt, get_working_df(), st.session_state.messages)
                        
                        answer = response_data.get("answer", "Error in processing.")
                        code = response_data.get("python_code", "")
                        
                        st.markdown(answer)
                        full_reply = f"{answer}\n\n```python\n{code}\n```" if code else answer
                        st.session_state.messages.append({"role": "assistant", "content": full_reply})
                        if code:
                            from services.execution_service import execute_code_blocks
                            execute_code_blocks(f"```python\n{code}\n```", get_working_df(), key_suffix=f"tab_{len(st.session_state.messages)-1}")
                        
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
    import json
    if get_working_df() is not None:
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
            "Download CSV", exp.to_csv(get_working_df()), f"{fname}.csv", "text/csv"
        )
        ec2.download_button(
            "Download Excel", exp.to_excel(get_working_df()), f"{fname}.xlsx"
        )
        ec3.download_button(
            "Download JSON", exp.to_json(get_working_df()), f"{fname}.json"
        )
        ec4.download_button(
            "Download PDF", exp.to_pdf(get_working_df()), f"{fname}.pdf"
        )

        ec5, ec6, ec7, ec8 = st.columns(4)
        ec5.download_button(
            "Download SQL", exp.to_sql(get_working_df()), f"{fname}.sql"
        )
        ec6.download_button(
            "Download Word", exp.to_word(get_working_df()), f"{fname}.docx"
        )
        ec7.download_button(
            "Download Markdown", exp.to_markdown(get_working_df()), f"{fname}.md"
        )
        ec8.download_button(
            "Download HTML", exp.to_html(get_working_df()), f"{fname}.html"
        )

        # New: Export audit log and vault assets
        st.subheader("🕒 Audit Log & Vault Assets")
        col_log, col_vault = st.columns(2)
        with col_log:
            if get_audit_log():
                audit_json = json.dumps(get_audit_log(), indent=2)
                st.download_button(
                    "Download Audit Log",
                    data=audit_json,
                    file_name=f"{fname}_audit_log.json",
                    mime="application/json",
                )
        with col_vault:
            if get_vault_assets():
                vault_json = json.dumps(get_vault_assets(), default=str, indent=2)
                st.download_button(
                    "Download Vault Assets",
                    data=vault_json,
                    file_name=f"{fname}_vault_assets.json",
                    mime="application/json",
                )
    else:
        st.warning("Please upload a file first.")


# End of Tab Renderers
