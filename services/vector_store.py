import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import os

@st.cache_resource
def load_embedding_model():
    """Load the SentenceTransformer model for embeddings."""
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def get_chromadb_client():
    """Initialize and return the ChromaDB client (remote or local)."""
    chroma_host = None
    if hasattr(st, "secrets"):
        chroma_host = st.secrets.get("CHROMA_HOST", None)
    
    if chroma_host:
        try:
            # Connect to Remote/Online ChromaDB
            chroma_port = st.secrets.get("CHROMA_PORT", "8000")
            return chromadb.HttpClient(host=chroma_host, port=chroma_port)
        except Exception:
            pass

    # Fallback to local
    try:
        return chromadb.PersistentClient(path="./chroma_db")
    except Exception:
        return None

def initialize_vector_store():
    """Initialize the embedding model and common collections."""
    try:
        embedder = load_embedding_model()
    except Exception:
        embedder = None
        
    chroma_client = get_chromadb_client()
    chat_collection = None
    doc_collection = None

    if chroma_client:
        try:
            chat_collection = chroma_client.get_or_create_collection("chat_memory")
            doc_collection = chroma_client.get_or_create_collection("doc_store")
        except Exception:
            pass
            
    return embedder, chroma_client, chat_collection, doc_collection
