import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import os
import hashlib
from typing import List, Optional


@st.cache_resource
def load_embedding_model():
    """Load the SentenceTransformer model for embeddings."""
    return SentenceTransformer("all-MiniLM-L6-v2")


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
        except Exception as e:
            st.warning(f"Failed to connect to remote ChromaDB: {e}")

    # Fallback to local
    try:
        return chromadb.PersistentClient(path="./chroma_db")
    except Exception as e:
        st.error(f"Failed to initialize local ChromaDB: {e}")
        return None


@st.cache_data
def get_embedding_cache_key(text: str) -> str:
    """Generate a cache key for text embedding."""
    return hashlib.md5(text.encode()).hexdigest()


@st.cache_data
def compute_embeddings_batch(
    _embedder: SentenceTransformer, texts: List[str]
) -> List[List[float]]:
    """Compute embeddings for a batch of texts with caching."""
    return _embedder.encode(texts, convert_to_tensor=False).tolist()


def get_embeddings(
    embedder: SentenceTransformer, texts: List[str], batch_size: int = 32
) -> List[List[float]]:
    """Get embeddings for texts, using batching and caching for efficiency."""
    if not embedder:
        return []

    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]
        batch_embeddings = compute_embeddings_batch(embedder, batch_texts)
        embeddings.extend(batch_embeddings)

    return embeddings


def add_documents_to_collection(
    collection,
    documents: List[str],
    metadatas: Optional[List[dict]] = None,
    ids: Optional[List[str]] = None,
    embedder: Optional[SentenceTransformer] = None,
):
    """Add documents to a ChromaDB collection with batching and error handling."""
    if not collection or not embedder:
        return False

    try:
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        embeddings = get_embeddings(embedder, documents)

        if metadatas and len(metadatas) != len(documents):
            metadatas = None  # Invalidate if mismatched

        collection.add(
            documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids
        )
        return True
    except Exception as e:
        st.error(f"Failed to add documents to collection: {e}")
        return False


def query_collection(
    collection,
    query_texts: List[str],
    embedder: SentenceTransformer,
    n_results: int = 5,
):
    """Query the collection with efficient embedding computation."""
    if not collection or not embedder:
        return None

    try:
        query_embeddings = get_embeddings(embedder, query_texts)
        results = collection.query(
            query_embeddings=query_embeddings, n_results=n_results
        )
        return results
    except Exception as e:
        st.error(f"Failed to query collection: {e}")
        return None


def initialize_vector_store():
    """Initialize the embedding model and common collections."""
    try:
        embedder = load_embedding_model()
    except Exception as e:
        st.error(f"Failed to load embedding model: {e}")
        embedder = None

    chroma_client = get_chromadb_client()
    chat_collection = None
    doc_collection = None

    if chroma_client:
        try:
            chat_collection = chroma_client.get_or_create_collection("chat_memory")
            doc_collection = chroma_client.get_or_create_collection("doc_store")
        except Exception as e:
            st.error(f"Failed to create collections: {e}")

    return embedder, chroma_client, chat_collection, doc_collection
