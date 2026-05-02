import os
import json
import time
from typing import List, Dict, Any, Optional
from txtai.embeddings import Embeddings
from deep_research_engine.utils import logger, get_env_var

class VectorStoreManager:
    """Manages the txtai embeddings index with dimensionality guards and fallbacks."""
    
    def __init__(self, provider: str = "ollama", index_path: str = ".vector_store"):
        self.provider = provider
        self.index_path = index_path
        self.embeddings = None
        self._initialize_embeddings()

    def _initialize_embeddings(self, retries: int = 3, delay: int = 2):
        """Initializes txtai with fallback from Ollama to local Transformers."""
        
        # Primary: Ollama, Fallback: Sentence-Transformers (Local)
        configs = [
            {"path": "ollama/nomic-embed-text", "method": "ollama"},
            {"path": "sentence-transformers/all-MiniLM-L6-v2", "method": "transformers"}
        ]
        
        # If user explicitly chose mistral or others, we could map them here, 
        # but following instructions to prefer local/transformers.
        if self.provider.lower() == "mistral":
            configs.insert(0, {"path": "mistral-embed", "method": "transformers"})

        last_exception = None
        for config in configs:
            attempts = retries if config["method"] == "ollama" else 1
            for i in range(attempts):
                try:
                    logger.info(f"Attempting to initialize embeddings with {config['path']} (Attempt {i+1}/{attempts})")
                    # Try initializing with 'content': True to store text and metadata
                    temp_embeddings = Embeddings({"path": config["path"], "content": True})

                    # Test if it actually works (especially for Ollama which might be down)
                    _ = temp_embeddings.transform("test connection")
                    
                    # Dimensionality Guard
                    if os.path.exists(self.index_path):
                        self._check_dimensionality(temp_embeddings, config)
                    
                    self.embeddings = temp_embeddings
                    logger.info(f"Successfully initialized embeddings using {config['path']}")
                    return
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Failed to initialize with {config['path']}: {e}")
                    if i < attempts - 1:
                        time.sleep(delay)
            
        logger.error(f"All embedding initialization attempts failed. Last error: {last_exception}")
        raise RuntimeError(f"Could not initialize any embedding provider: {last_exception}")

    def _check_dimensionality(self, new_embeddings: Embeddings, config: Dict[str, str]):
        """Checks if the new model's dimensions match the existing index."""
        if not os.path.exists(self.index_path):
            return

        try:
            # Get dimensions of current model
            test_vec = new_embeddings.transform("test")
            current_dim = test_vec.shape[1]
            
            # Load existing index to check its dimensions
            # We use a clean Embeddings instance to inspect the existing index
            temp_idx = Embeddings()
            temp_idx.load(self.index_path)
            
            info = temp_idx.info()
            if info and "dimensions" in info:
                index_dim = info["dimensions"]
                if index_dim != current_dim:
                    logger.warning(f"Dimensionality mismatch: Index has {index_dim}, but model {config['path']} has {current_dim}")
                    self._backup_index()
                else:
                    logger.info(f"Index dimensionality check passed: {index_dim} matches {config['path']}")
            elif temp_idx.count() > 0:
                # If info is missing but index has data, try a search to verify compatibility
                try:
                    temp_idx.search("test", 1)
                    logger.info("Index check passed via search test.")
                except Exception as search_err:
                    logger.warning(f"Search failed on existing index, likely dimension mismatch: {search_err}")
                    self._backup_index()
        except Exception as e:
            logger.warning(f"Could not verify existing index dimensions: {e}. Backing up and starting fresh.")
            self._backup_index()

    def _backup_index(self):
        """Backs up the existing index to avoid crashes."""
        if os.path.exists(self.index_path):
            timestamp = int(time.time())
            backup_path = f"{self.index_path}_backup_{timestamp}"
            
            counter = 1
            while os.path.exists(backup_path):
                backup_path = f"{self.index_path}_backup_{timestamp}_{counter}"
                counter += 1
                
            os.rename(self.index_path, backup_path)
            logger.info(f"Existing index backed up to {backup_path}")

    def add_documents(self, chunks: List[str], metadata: Dict[str, Any]):
        """Adds context-enriched chunks to the index."""
        if not self.embeddings:
            raise RuntimeError("Embeddings not initialized")
            
        # Use [{"id": ..., "text": ..., **metadata}] format
        # This is the most reliable way to store metadata in txtai with content=True
        # and avoids "Error binding parameter 4" by not using the tags parameter.
        data = [{"id": f"{metadata.get('source_hash', 'chunk')}_{i}", "text": chunk, **metadata} 
                for i, chunk in enumerate(chunks)]
        
        # Use upsert to avoid wiping out the index if it exists
        self.embeddings.upsert(data)
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
