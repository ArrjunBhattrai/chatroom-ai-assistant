from chroma.vector_store import search_similar_messages
from langchain.schema import Document

def find_similar_messages(query: str, k: int = 8) -> list[Document]:
    """
    Wrapper to fetch top-k semantically similar messages for a given query.
    """
    try:
        results = search_similar_messages(query, k=k)
        return results
    except Exception as e:
        print("[Semantic Search] Error:", e)
        return []
