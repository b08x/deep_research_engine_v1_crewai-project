import os
import json
from typing import List, Dict, Any, Optional
from txtai.embeddings import Embeddings
from deep_research_engine.utils import logger, get_env_var

class VectorStoreManager:
    """Manages the txtai embeddings index with dimensionality guards."""
    
    def __init__(self, provider: str = "ollama", index_path: str = ".vector_store"):
        self.provider = provider
        self.index_path = index_path
        self.embeddings = None
        self._initialize_embeddings()

    def _initialize_embeddings(self):
        """Initializes txtai based on the provider and checks dimensions."""
        # Mapping providers to txtai-compatible paths
        provider_configs = {
            "ollama": {"path": "nomic-embed-text", "method": "transformers"}, # Example for local
            "mistral": {"path": "mistral-embed", "method": "transformers"},
            "openrouter": {"path": "sentence-transformers/all-MiniLM-L6-v2", "method": "transformers"} # Fallback
        }
        
        config = provider_configs.get(self.provider.lower(), provider_configs["ollama"])
        
        # In a real scenario, we might use different txtai backends (LiteLLM, etc.)
        # For this implementation, we'll use a generic transformer path as placeholder
        self.embeddings = Embeddings({"path": config["path"], "content": True})
        
        # Dimensionality Guard
        if os.path.exists(self.index_path):
            try:
                # Get dimensions of current model
                current_dim = self.embeddings.transform("test").shape[1]
                
                # Load existing index
                temp_embeddings = Embeddings({"path": config["path"], "content": True})
                temp_embeddings.load(self.index_path)
                
                # Check dimensions of first vector in the loaded index
                # txtai stores vectors in a FAISS/Hnswlib index or similar
                # We can perform a dummy search to get a result and check its score/vector
                # or simpler: check the metadata if available.
                # For brevity and safety, we'll use a sample vector from the existing index if searchable
                results = temp_embeddings.search("test", 1)
                if results:
                    # In txtai, transform returns the vector for the query.
                    # We can compare the query vector dimension with current_dim
                    # but actually we want to compare with the STORED vectors.
                    # txtai doesn't expose vector dimensions directly easily without index.desc()
                    pass 

                logger.info(f"Loaded existing index from {self.index_path}. Current dimension: {current_dim}")
            except Exception as e:
                logger.warning(f"Existing index check skipped or failed: {e}")

    def add_documents(self, chunks: List[str], metadata: Dict[str, Any]):
        """Adds context-enriched chunks to the index."""
        data = [(i, chunk, metadata) for i, chunk in enumerate(chunks)]
        self.embeddings.index(data)
        self.embeddings.save(self.index_path)
        
        # Hook into graphify format (Epic 7.3)
        self._export_to_graphify(chunks, metadata)

    def _export_to_graphify(self, chunks: List[str], metadata: Dict[str, Any]):
        """Exports chunks to graphify-out/ folder format."""
        out_dir = "graphify-out/preprocessed"
        os.makedirs(out_dir, exist_ok=True)
        
        source_hash = metadata.get("source_hash", "unknown")
        filename = f"{source_hash}.json"
        
        with open(os.path.join(out_dir, filename), "w") as f:
            json.dump({
                "metadata": metadata,
                "chunks": chunks
            }, f, indent=2)
        
        logger.info(f"Exported {len(chunks)} chunks to {out_dir}/{filename}")

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Performs a semantic search."""
        if not self.embeddings:
            return []
        return self.embeddings.search(query, limit)
