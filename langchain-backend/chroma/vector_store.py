from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings  
import os

# Create embedding model
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  

# Persistent directory for Chroma vector db
CHROMA_DIR = "chroma_store"

# Create or load the vector store
vector_store = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embedding_function
)

def add_message_to_vector_store(text: str, metadata: dict):
    """Adds a new message to the Chroma vector store"""
    doc = Document(page_content=text, metadata=metadata)
    vector_store.add_documents([doc])
    vector_store.persist()

def search_similar_messages(query: str, k: int):
    """Performs semantic search over stored messages"""
    return vector_store.similarity_search(query, k=k)
