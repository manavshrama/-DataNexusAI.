import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import uuid
import time
from modules.data_loader import DataLoader
from modules.eda import EDAModule
from modules.visualization import VisualizationModule
from modules.ml_models import MLModule
from modules.chatbot import ChatbotModule
from modules.exporter import ExporterModule

def render_upload_tab(doc_collection, embedder):
    st.header("Step 1: Upload & Initial stats")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx', 'xls'])
    
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
                            start += (chunk_size - overlap)
                        
                        for i, chunk in enumerate(chunks):
                            vector = embedder.encode(chunk).tolist()
                            chunk_id = f"{uploaded_file.name}_chunk_{i}_{uuid.uuid4().hex[:8]}"
                            doc_collection.add(
                                embeddings=[vector],
                                documents=[chunk],
                                metadatas=[{"file_name": uploaded_file.name, "chunk_id": i}],
                                ids=[chunk_id]
                            )
                    except Exception:
                        pass
                        
                st.rerun()
                
    if st.session_state.df is not None:
        stats = DataLoader.get_stats(st.session_state.df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", stats['rows'])
        c2.metric("Cols", stats['cols'])
        c3.metric("Nulls", stats['nulls'], f"{stats['null_pct']:.1f}%", delta_color="inverse")
        c4.metric("Duplicates", stats['duplicates'])
        
        st.subheader("Data Preview")
        rows = st.slider("Preview Rows", 5, 100, 10)
        st.dataframe(st.session_state.df.head(rows), use_container_width=True)
        
        st.subheader("Data Cleaning")
        cc1, cc2, cc3 = st.columns(3)
        if cc1.button("Drop Duplicates"):
            st.session_state.df = DataLoader.clean_data(st.session_state.df, "drop_duplicates")
            st.success("Duplicates dropped!")
        if cc2.button("Fill Nulls (Mean)"):
            st.session_state.df = DataLoader.clean_data(st.session_state.df, "fill_nulls_mean")
            st.success("Numeric nulls filled!")
        if cc3.button("Drop Any Nulls"):
            st.session_state.df = DataLoader.clean_data(st.session_state.df, "drop_any_nulls")
            st.success("Rows with nulls removed!")

def render_eda_tab():
    if st.session_state.df is not None:
        eda = EDAModule()
        st.header("Exploratory Data Analysis")
        
        with st.expander("Statistical Summary", expanded=True):
            summary = eda.statistical_summary(st.session_state.df)
            if 'numeric' in summary:
                st.write("**Numerical Features**")
                st.dataframe(summary['numeric'])
            if 'categorical' in summary:
                st.write("**Categorical Features**")
                st.dataframe(summary['categorical'])
                
        with st.expander("Correlation Analysis"):
            corr, pairs = eda.correlation_analysis(st.session_state.df)
            if corr is not None:
                fig = px.imshow(corr, text_auto=True, template="plotly_dark", color_continuous_scale="Viridis")
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
        st.header("Data Visualization Studio")
        viz = VisualizationModule()
        
        col1, col2 = st.columns([1, 3])
        with col1:
            chart_type = st.selectbox("Select Chart Type", [
                "Bar Chart", "Line Chart", "Scatter Plot", "Pie / Donut Chart", 
                "Box Plot", "Violin Plot", "Heatmap", "Histogram", "Bubble Chart",
                "Treemap", "Sunburst", "3D Scatter Plot", "Radar / Spider Chart",
                "Area Chart", "Funnel Chart", "Parallel Coordinates", "Pair Plot"
            ])
            
            all_cols = st.session_state.df.columns.tolist()
            x_ax = st.selectbox("X Axis", all_cols)
            y_ax = st.selectbox("Y Axis (if applicable)", [None] + all_cols)
            color_ax = st.selectbox("Color/Group By", [None] + all_cols)
            
            agg = st.selectbox("Aggregation", [None, "Sum", "Mean", "Count", "Max", "Min", "OLS Trendline"])
            scale = st.selectbox("Color Scale", viz.get_color_scales())
            
        with col2:
            fig = viz.plot(chart_type, st.session_state.df, x=x_ax, y=y_ax, color=color_ax, aggregation=agg, color_scale=scale)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                if st.checkbox("Show chart data table"):
                    st.dataframe(st.session_state.df[[x_ax] + ([y_ax] if y_ax else [])].head(50))
            else:
                st.error("Could not generate chart. Check column types.")
    else:
        st.warning("Please upload a file first.")

def render_ml_tab():
    if st.session_state.df is not None:
        ml = MLModule()
        st.header("Machine Learning Lab")
        
        task_type = st.radio("Select ML Task", ["Classification", "Regression", "Clustering"], horizontal=True)
        
        if task_type in ["Classification", "Regression"]:
            target = st.selectbox("Select Target Column", st.session_state.df.columns)
            X, y = ml.preprocess(st.session_state.df, target, task=task_type.lower())
            
            model_list = list(ml.classification_models.keys()) if task_type == "Classification" else list(ml.regression_models.keys())
            selected_model = st.selectbox("Select Model", model_list)
            
            if st.button(f"Train {selected_model}"):
                with st.spinner("Training model..."):
                    if task_type == "Classification":
                        metrics, cm, importance = ml.train_classification(X, y, selected_model)
                        st.session_state.ml_results = {"metrics": metrics, "cm": cm, "importance": importance, "type": "class"}
                    else:
                        metrics, y_test, y_pred = ml.train_regression(X, y, selected_model)
                        st.session_state.ml_results = {"metrics": metrics, "y_test": y_test, "y_pred": y_pred, "type": "reg"}
                
        if st.session_state.ml_results:
            res = st.session_state.ml_results
            st.subheader("Performance Metrics")
            cols = st.columns(len(res['metrics']))
            for i, (k, v) in enumerate(res['metrics'].items()):
                cols[i].metric(k, f"{v:.4f}")
            
            if res.get('type') == "class":
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Confusion Matrix**")
                    fig = px.imshow(res['cm'], text_auto=True, template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    if res['importance'] is not None:
                        st.write("**Feature Importance**")
                        fig = px.bar(res['importance'].head(10), x='Importance', y='Feature', orientation='h', template="plotly_dark")
                        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please upload a file first.")

def render_chat_tab(chroma_client, embedder, chat_collection, doc_collection):
    if st.session_state.df is not None:
        st.header("💬 AI Data Analyst")
        bot = ChatbotModule(groq_key=st.session_state.groq_key, gemini_key=st.session_state.gemini_key)
        
        # Quick prompts
        quick = ["Summarize this data", "Which column has most nulls?", "Show top correlations", "Suggest ML models"]
        cp = st.columns(4)
        for i, p in enumerate(quick):
            if cp[i].button(p, use_container_width=True):
                st.session_state.chat_input = p
        
        # Chat container
        chat_container = st.container(height=500)
        for msg in st.session_state.chat_history:
            role = "user" if msg["role"] == "user" else "assistant"
            with chat_container:
                st.markdown(f'<div class="{role}-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        
        if prompt := st.chat_input("Ask about your data..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with chat_container:
                st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)
            
            with st.spinner("AI is thinking..."):
                doc_context = ""
                chat_context = ""
                
                if chroma_client and embedder:
                    try:
                        q_emb = embedder.encode(prompt).tolist()
                        if doc_collection:
                            docs_res = doc_collection.query(query_embeddings=[q_emb], n_results=5)
                            if docs_res and 'documents' in docs_res and docs_res['documents'] and len(docs_res['documents'][0]) > 0:
                                doc_context = "\nDataset Content Snippets:\n" + "\n".join(docs_res['documents'][0])
                                
                        if chat_collection:
                            chat_res = chat_collection.query(query_embeddings=[q_emb], n_results=3)
                            if chat_res and 'documents' in chat_res and chat_res['documents'] and len(chat_res['documents'][0]) > 0:
                                chat_context = "\nPast Relevant Conversational Context:\n" + "\n".join(chat_res['documents'][0])
                    except Exception:
                        pass
                
                enhanced_prompt = f"{chat_context}\n{doc_context}\nUser Instruction: {prompt}" if doc_context or chat_context else prompt
                response = bot.ask(enhanced_prompt, st.session_state.df, st.session_state.chat_history)
                reply = response.get('answer', 'Error')
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                
                if chat_collection and embedder:
                    try:
                        for role, content in [("user", prompt), ("assistant", reply)]:
                            vector = embedder.encode(content).tolist()
                            chat_collection.add(
                                embeddings=[vector],
                                documents=[content],
                                metadatas=[{"role": role, "timestamp": time.time(), "session_id": st.session_state.session_id}],
                                ids=[f"chat_{uuid.uuid4().hex}"]
                            )
                    except Exception:
                        pass
                
                with chat_container:
                    st.markdown(f'<div class="ai-bubble">{reply}</div>', unsafe_allow_html=True)
                    if 'chart' in response and response['chart']:
                        c = response['chart']
                        viz = VisualizationModule()
                        fig = viz.plot(c.get('type','Bar Chart'), st.session_state.df, x=c.get('x'), y=c.get('y'), aggregation=c.get('agg'))
                        if fig: st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please upload a file first.")

def render_export_tab():
    if st.session_state.df is not None:
        st.header("Export Cleaned Data")
        exp = ExporterModule()
        fname = st.text_input("Filename", value=f"data_nexus_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}")
        
        ec1, ec2, ec3, ec4 = st.columns(4)
        ec1.download_button("Download CSV", exp.to_csv(st.session_state.df), f"{fname}.csv", "text/csv")
        ec2.download_button("Download Excel", exp.to_excel(st.session_state.df), f"{fname}.xlsx")
        ec3.download_button("Download JSON", exp.to_json(st.session_state.df), f"{fname}.json")
        ec4.download_button("Download PDF", exp.to_pdf(st.session_state.df), f"{fname}.pdf")
        
        ec5, ec6, ec7, ec8 = st.columns(4)
        ec5.download_button("Download SQL", exp.to_sql(st.session_state.df), f"{fname}.sql")
        ec6.download_button("Download Word", exp.to_word(st.session_state.df), f"{fname}.docx")
        ec7.download_button("Download Markdown", exp.to_markdown(st.session_state.df), f"{fname}.md")
        ec8.download_button("Download HTML", exp.to_html(st.session_state.df), f"{fname}.html")
    else:
        st.warning("Please upload a file first.")
