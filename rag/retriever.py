from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CHROMA_PATH = "rag/chroma_db"

def get_retriever(collection_name: str = "documents", k: int = 4):
    """
    Get a retriever from ChromaDB.
    
    Args:
        collection_name: Name of the collection
        k: Number of documents to retrieve
        
    Returns:
        Retriever object
    """
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name=collection_name
    )
    
    return vectorstore.as_retriever(
        search_kwargs={"k": k}
    )

def retrieve_documents(query: str, k: int = 4, collection_name: str = "documents"):
    """
    Retrieve relevant documents from ChromaDB.
    
    Args:
        query: Search query
        k: Number of documents to retrieve
        collection_name: Name of the collection
        
    Returns:
        List of retrieved documents with scores
    """
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name=collection_name
    )
    
    # Similarity search with scores
    results = vectorstore.similarity_search_with_relevance_scores(
        query,
        k=k
    )
    
    return results

def get_retrieval_stats(collection_name: str = "documents"):
    """
    Get statistics about retrieval capability.
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        Statistics dict
    """
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name
        )
        
        # Get collection
        collection = vectorstore._collection
        count = collection.count()
        
        return {
            "collection_name": collection_name,
            "document_count": count,
            "ready": count > 0,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
        }
        
    except Exception as e:
        return {
            "collection_name": collection_name,
            "error": str(e),
            "ready": False
        }
