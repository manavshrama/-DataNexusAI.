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
    render_hero("Data Nexus", "Upload your dataset and let the engine take over")
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
        st.markdown(
            '<div class="meta-label">Dataset Vitals</div>', unsafe_allow_html=True
        )
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(
                f'<div class="glass-card"><h4>Rows</h4><h2>{stats["rows"]:,}</h2></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="glass-card"><h4>Cols</h4><h2>{stats["cols"]:,}</h2></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="glass-card"><h4>Nulls</h4><h2>{stats["null_pct"]:.1f}%</h2></div>',
                unsafe_allow_html=True,
            )
        with c4:
            st.markdown(
                f'<div class="glass-card"><h4>Duplicates</h4><h2>{stats["duplicates"]:,}</h2></div>',
                unsafe_allow_html=True,
            )
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
        render_hero("Insight Engine", "Explore distributions, correlations, and data quality at a glance")

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
        render_hero("Visual Studio", "Navigate through high-precision galactic visualizations and multidimensional data structures.")
        viz = VisualizationModule()

        col1, col2 = st.columns([1, 3])
        with col1:
            chart_type = st.selectbox(
                "Select Chart Type",
                [
                    "Bar Chart",
                    "Line Chart",
                    "Scatter Plot",
                    "Pie / Donut Chart",
                    "Box Plot",
                    "Violin Plot",
                    "Heatmap",
                    "Histogram",
                    "Bubble Chart",
                    "Treemap",
                    "Sunburst",
                    "3D Scatter Plot",
                    "Radar / Spider Chart",
                    "Area Chart",
                    "Funnel Chart",
                    "Parallel Coordinates",
                    "Pair Plot",
                ],
            )

            all_cols = st.session_state.df.columns.tolist()
            x_ax = st.selectbox("X Axis", all_cols)
            y_ax = st.selectbox("Y Axis (if applicable)", [None] + all_cols)
            color_ax = st.selectbox("Color/Group By", [None] + all_cols)

            agg = st.selectbox(
                "Aggregation",
                [None, "Sum", "Mean", "Count", "Max", "Min", "OLS Trendline"],
            )
            scale = st.selectbox("Color Scale", viz.get_color_scales())

        with col2:
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
                if st.checkbox("Show chart data table"):
                    st.dataframe(
                        st.session_state.df[[x_ax] + ([y_ax] if y_ax else [])].head(50)
                    )
            else:
                st.error("Could not generate chart. Check column types.")
    else:
        st.warning("Please upload a file first.")


def render_ml_tab():
    if st.session_state.df is not None:
        ml = MLModule()
        render_hero("ML Studio", "Configure, train, and monitor your model in one workflow")

        task_type = st.radio(
            "Select ML Task",
            ["Classification", "Regression", "Clustering"],
            horizontal=True,
        )

        if task_type in ["Classification", "Regression"]:
            target = st.selectbox("Select Target Column", st.session_state.df.columns)
            X, y = ml.preprocess(st.session_state.df, target, task=task_type.lower())

            model_list = (
                list(ml.classification_models.keys())
                if task_type == "Classification"
                else list(ml.regression_models.keys())
            )
            selected_model = st.selectbox("Select Model", model_list)

            if st.button(f"Train {selected_model}"):
                with st.spinner("Training model..."):
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
        render_hero("Neural Chat", "Ask anything about your data. Get code, charts, and insights instantly.")
        bot = ChatbotModule(
            groq_key=st.session_state.groq_key, gemini_key=st.session_state.gemini_key
        )

        # Quick prompts
        quick = [
            "Summarize this data",
            "Which column has most nulls?",
            "Show top correlations",
            "Suggest ML models",
        ]
        cp = st.columns(4)
        for i, p in enumerate(quick):
            if cp[i].button(p, use_container_width=True):
                st.session_state.chat_input = p

        # Chat container
        chat_container = st.container(height=500)
        for msg in st.session_state.chat_history:
            role = "user" if msg["role"] == "user" else "assistant"
            with chat_container:
                if role == "assistant":
                    st.markdown(
                        f'<div class="{role}-bubble"><span class="sparkle-icon">✨</span>{msg["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="{role}-bubble">{msg["content"]}</div>',
                        unsafe_allow_html=True,
                    )

        if prompt := st.chat_input("Ask about your data..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with chat_container:
                st.markdown(
                    f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True
                )

            with st.spinner("AI is thinking..."):
                doc_context = ""
                chat_context = ""

                if chroma_client and embedder:
                    try:
                        q_emb = embedder.encode(prompt).tolist()
                        if doc_collection:
                            docs_res = doc_collection.query(
                                query_embeddings=[q_emb], n_results=5
                            )
                            if (
                                docs_res
                                and "documents" in docs_res
                                and docs_res["documents"]
                                and len(docs_res["documents"][0]) > 0
                            ):
                                doc_context = (
                                    "\nDataset Content Snippets:\n"
                                    + "\n".join(docs_res["documents"][0])
                                )

                        if chat_collection:
                            chat_res = chat_collection.query(
                                query_embeddings=[q_emb], n_results=3
                            )
                            if (
                                chat_res
                                and "documents" in chat_res
                                and chat_res["documents"]
                                and len(chat_res["documents"][0]) > 0
                            ):
                                chat_context = (
                                    "\nPast Relevant Conversational Context:\n"
                                    + "\n".join(chat_res["documents"][0])
                                )
                    except Exception as e:
                        logger.warning("Failed to query vector store: %s", e)

                enhanced_prompt = (
                    f"{chat_context}\n{doc_context}\nUser Instruction: {prompt}"
                    if doc_context or chat_context
                    else prompt
                )
                response = bot.ask(
                    enhanced_prompt, st.session_state.df, st.session_state.chat_history
                )
                reply = response.get("answer", "Error")
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": reply}
                )

                if chat_collection and embedder:
                    try:
                        for role, content in [("user", prompt), ("assistant", reply)]:
                            vector = embedder.encode(content).tolist()
                            chat_collection.add(
                                embeddings=[vector],
                                documents=[content],
                                metadatas=[
                                    {
                                        "role": role,
                                        "timestamp": time.time(),
                                        "session_id": st.session_state.session_id,
                                    }
                                ],
                                ids=[f"chat_{uuid.uuid4().hex}"],
                            )
                    except Exception as e:
                        logger.warning("Failed to store chat embedding: %s", e)

                with chat_container:
                    st.markdown(
                        f'<div class="ai-bubble"><span class="sparkle-icon">✨</span>{reply}</div>',
                        unsafe_allow_html=True,
                    )
                    if "chart" in response and response["chart"]:
                        c = response["chart"]
                        viz = VisualizationModule()
                        fig = viz.plot(
                            c.get("type", "Bar Chart"),
                            st.session_state.df,
                            x=c.get("x"),
                            y=c.get("y"),
                            aggregation=c.get("agg"),
                        )
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please upload a file first.")


def render_export_tab():
    if st.session_state.df is not None:
        render_hero("Export Vault", "Download your cleaned data and generated assets")
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


def render_insights_tab():
    render_hero("Intelligence Stream", "Real-time analysis and anomalies detected by the Nexus AI Core.")

    # Mock insights data (in real app, fetch from API or generate)
    insights = [
        {
            "id": 1,
            "title": "Anomalies Detected in Sales Data",
            "severity": "high",
            "dataset": "sales_2024.csv",
            "summary": "System identified unusual patterns in the Q3 revenue column suggesting potential data entry errors.",
            "time": "2 mins ago",
        },
        {
            "id": 2,
            "title": "Trend Analysis Complete",
            "severity": "medium",
            "dataset": "customer_data.xlsx",
            "summary": "Predictive model indicates 15% growth in customer acquisition for next quarter.",
            "time": "5 mins ago",
        },
        {
            "id": 3,
            "title": "Correlation Insights",
            "severity": "low",
            "dataset": "inventory.csv",
            "summary": "Strong correlation found between stock levels and seasonal demand patterns.",
            "time": "10 mins ago",
        },
    ]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("⚡ Active Intelligence Stream")

        for insight in insights:

            st.markdown(
                f"""
            <div class="glass-card" style="padding: 20px; margin-bottom: 16px;">
                <div style="display: flex; gap: 16px;">
                    <div style="width: 48px; height: 48px; border-radius: 12px; background-color: {"rgba(220, 38, 38, 0.1)" if insight["severity"] == "high" else "rgba(234, 88, 12, 0.1)" if insight["severity"] == "medium" else "rgba(0, 201, 167, 0.1)"}; display: flex; align-items: center; justify-content: center; color: {"#dc2626" if insight["severity"] == "high" else "#ea580c" if insight["severity"] == "medium" else "#00C9A7"};">
                        {"🚨" if insight["severity"] == "high" else "📈" if insight["severity"] == "medium" else "📊"}
                    </div>
                    <div style="flex: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <h4 style="color: #f8f9ff; font-size: 18px; font-weight: bold;">{insight["title"]}</h4>
                            <span style="color: rgba(248, 249, 255, 0.3); font-size: 10px; font-weight: bold; text-transform: uppercase;">{insight["time"]}</span>
                        </div>
                        <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                            <span style="background-color: rgba(108, 99, 255, 0.1); color: #6C63FF; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: 600;">{insight["dataset"]}</span>
                            <span style="color: {"#dc2626" if insight["severity"] == "high" else "rgba(248, 249, 255, 0.4)"}; font-size: 12px;">
                                Priority: {insight["severity"].upper()}
                            </span>
                        </div>
                        <p style="color: rgba(248, 249, 255, 0.6); font-size: 14px; line-height: 1.5; margin-bottom: 12px;">{insight["summary"]}</p>
                        <button style="color: #6C63FF; font-size: 12px; font-weight: bold; background: none; border: none; cursor: pointer;">View Detailed Analysis →</button>
                    </div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col2:
        st.subheader("📊 Distribution")

        # Mock confidence chart
        confidence = 84
        fig = px.pie(
            values=[confidence, 100 - confidence],
            names=["Confidence", "Uncertainty"],
            color_discrete_sequence=["#0049db", "#737687"],
            hole=0.7,
        )
        fig.update_layout(
            showlegend=False,
            annotations=[
                dict(text=f"{confidence}%", x=0.5, y=0.5, font_size=30, showarrow=False)
            ],
            margin=dict(l=0, r=0, t=0, b=0),
            height=200,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
        <div style="margin-top: 24px;">
            <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px;">
                <span>Statistical</span>
                <span>62%</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px;">
                <span>Predictive</span>
                <span>28%</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 12px;">
                <span>Anomaly</span>
                <span>10%</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div style="background: linear-gradient(135deg, #6C63FF 0%, #7B5EA7 100%); border-radius: 20px; padding: 25px; margin-top: 32px; color: white; box-shadow: 0 10px 30px rgba(108, 99, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 800; margin-bottom: 10px; font-family: 'Syne', sans-serif;">Automate Tasks</h4>
            <p style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 20px;">Let Nexus AI handle routine data cleaning and preparation automatically.</p>
            <button style="width: 100%; padding: 12px; background: white; color: #6C63FF; border: none; border-radius: 12px; font-weight: 800; cursor: pointer; font-family: 'DM Sans', sans-serif;">Enable Auto-Pilot</button>
        </div>
        """,
            unsafe_allow_html=True,
        )
