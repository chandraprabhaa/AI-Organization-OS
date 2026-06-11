from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import PyPDF2

CHROMA_PATH = "rag/chroma_db"

def ingest_document(file_path: str, collection_name: str = "documents"):
    """
    Ingest PDF document into ChromaDB.
    
    Args:
        file_path: Path to PDF file
        collection_name: Name of the collection in Chroma
        
    Returns:
        dict with ingestion statistics
    """
    
    try:
        # Validate file exists
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Load PDF
        print(f"Loading PDF: {file_path}")
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        if not documents:
            raise ValueError("No content extracted from PDF")
        
        print(f"Loaded {len(documents)} pages")
        
        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Create/update ChromaDB
        Path(CHROMA_PATH).mkdir(parents=True, exist_ok=True)
        
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name
        )
        
        # Add documents
        vectorstore.add_documents(chunks)
        
        stats = {
            "status": "success",
            "file": Path(file_path).name,
            "pages": len(documents),
            "chunks": len(chunks),
            "collection": collection_name
        }
        
        print(f"Successfully ingested {file_path}")
        return stats
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "file": file_path
        }

def ingest_multiple_documents(directory: str):
    """
    Ingest all PDFs from a directory.
    
    Args:
        directory: Path to directory containing PDFs
        
    Returns:
        List of ingestion results
    """
    
    results = []
    pdf_dir = Path(directory)
    
    if not pdf_dir.exists():
        return [{"error": f"Directory not found: {directory}"}]
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    for pdf_file in pdf_files:
        result = ingest_document(str(pdf_file))
        results.append(result)
    
    return results

def get_collection_stats(collection_name: str = "documents"):
    """
    Get statistics about a ChromaDB collection.
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        Collection statistics
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
        
        # Get collection info
        collection = vectorstore._collection
        count = collection.count()
        
        return {
            "collection_name": collection_name,
            "document_count": count,
            "status": "active"
        }
        
    except Exception as e:
        return {
            "collection_name": collection_name,
            "error": str(e),
            "status": "error"
        }

def clear_collection(collection_name: str = "documents"):
    """Clear a collection (use with caution)"""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name
        )
        
        # Delete the collection
        vectorstore.delete_collection()
        
        return {"status": "success", "message": f"Cleared {collection_name}"}
        
    except Exception as e:
        return {"status": "error", "error": str(e)}
