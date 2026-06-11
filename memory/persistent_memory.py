import json
import time
from datetime import datetime
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

class MemoryManager:
    """
    Persistent memory system using ChromaDB.
    Stores: user queries, agent outputs, reports, critiques.
    """
    
    MEMORY_DB_PATH = "memory/memory_db"
    
    def __init__(self):
        """Initialize memory manager with ChromaDB"""
        # Create memory directory if it doesn't exist
        Path(self.MEMORY_DB_PATH).mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize ChromaDB vector store
        self.vector_store = Chroma(
            persist_directory=self.MEMORY_DB_PATH,
            embedding_function=self.embeddings,
            collection_name="ai_os_memory"
        )
        
        # Local file-based index for metadata
        self.index_file = Path(self.MEMORY_DB_PATH) / "memory_index.json"
        self._load_index()
    
    def _load_index(self):
        """Load memory index from disk"""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {
                "total_memories": 0,
                "by_type": {
                    "queries": [],
                    "reports": [],
                    "critiques": [],
                    "plans": []
                },
                "created_at": datetime.now().isoformat()
            }
    
    def _save_index(self):
        """Save memory index to disk"""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def save_memory(self, query: str, data: str, data_type: str = "reports"):
        """
        Save data to persistent memory.
        
        Args:
            query: The business goal/query
            data: The data to remember (agent output)
            data_type: Type of data (reports, critiques, plans, queries)
        """
        
        # Create metadata
        timestamp = datetime.now().isoformat()
        memory_id = f"{data_type}_{int(time.time()*1000)}"
        
        metadata = {
            "type": data_type,
            "query": query,
            "timestamp": timestamp,
            "memory_id": memory_id,
            "length": len(data)
        }
        
        # Create document
        doc = Document(
            page_content=f"Query: {query}\n\nOutput:\n{data}",
            metadata=metadata
        )
        
        # Store in ChromaDB
        self.vector_store.add_documents([doc])
        
        # Update index
        self.index["total_memories"] += 1
        if data_type in self.index["by_type"]:
            self.index["by_type"][data_type].append({
                "memory_id": memory_id,
                "timestamp": timestamp,
                "query": query[:100]  # Store first 100 chars of query
            })
        
        self._save_index()
        
        print(f"Memory saved: {memory_id} ({data_type})")
        return memory_id
    
    def search_memory(self, query: str, limit: int = 3, search_type: str = None):
        """
        Search memory for relevant past outputs.
        
        Args:
            query: Query string to search for
            limit: Number of results to return
            search_type: Filter by type (reports, critiques, plans, queries)
            
        Returns:
            Formatted string of relevant memories
        """
        
        try:
            # Search in vector store
            if search_type:
                where_filter = {"type": {"$eq": search_type}}
                results = self.vector_store.similarity_search_with_score(
                    query,
                    k=limit,
                    where=where_filter
                )
            else:
                results = self.vector_store.similarity_search_with_score(
                    query,
                    k=limit
                )
            
            if not results:
                return ""
            
            # Format results
            memory_text = "## Past Similar Outputs (for context):\n\n"
            for doc, score in results:
                memory_text += f"[Relevance: {score:.2f}]\n"
                memory_text += f"[Type: {doc.metadata.get('type', 'unknown')}]\n"
                memory_text += f"[Date: {doc.metadata.get('timestamp', 'unknown')[:10]}]\n"
                memory_text += f"{doc.page_content[:500]}...\n\n"
            
            return memory_text
            
        except Exception as e:
            print(f"Memory search error: {e}")
            return ""
    
    def retrieve_memory(self, memory_id: str):
        """
        Retrieve specific memory by ID.
        
        Args:
            memory_id: The memory ID to retrieve
            
        Returns:
            Memory content or None
        """
        
        try:
            results = self.vector_store.get(ids=[memory_id])
            if results and results.get("documents"):
                return results["documents"][0]
            return None
        except Exception as e:
            print(f"Error retrieving memory {memory_id}: {e}")
            return None
    
    def get_memory_stats(self):
        """Get statistics about stored memories"""
        return {
            "total_memories": self.index.get("total_memories", 0),
            "by_type": self.index.get("by_type", {}),
            "created_at": self.index.get("created_at", "unknown")
        }
    
    def get_recent_memories(self, data_type: str = None, limit: int = 5):
        """
        Get recent memories of a specific type.
        
        Args:
            data_type: Filter by type
            limit: Number to retrieve
            
        Returns:
            List of recent memories
        """
        
        if data_type and data_type in self.index["by_type"]:
            items = self.index["by_type"][data_type]
            return items[-limit:]
        
        return []
    
    def get_all_memories_by_type(self, data_type: str):
        """Get all memories of a specific type"""
        return self.index["by_type"].get(data_type, [])
    
    def clear_memory(self, data_type: str = None):
        """
        Clear memories (careful!)
        
        Args:
            data_type: Clear specific type, or all if None
        """
        
        if data_type and data_type in self.index["by_type"]:
            self.index["by_type"][data_type] = []
            print(f"Cleared all {data_type} memories")
        else:
            for key in self.index["by_type"]:
                self.index["by_type"][key] = []
            self.index["total_memories"] = 0
            print("Cleared all memories")
        
        self._save_index()
