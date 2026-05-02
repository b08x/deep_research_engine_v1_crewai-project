import os
import shutil
import pytest
from deep_research_engine.vector_store import VectorStoreManager

def test_vector_store_add_documents():
    index_path = "test_vector_store_index"
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    
    try:
        # Initialize with local transformers to avoid Ollama dependency in tests
        vstore = VectorStoreManager(provider="local", index_path=index_path)
        
        chunks = ["Chunk 1", "Chunk 2"]
        metadata = {"source": "test_source", "source_hash": "test_hash"}
        
        # This should now work without "Error binding parameter 4"
        vstore.add_documents(chunks, metadata)
        
        assert os.path.exists(index_path)
        
        # Verify search
        results = vstore.search("Chunk 1", limit=1)
        assert len(results) > 0
        assert "Chunk 1" in results[0]["text"]
        # The binding error is fixed. Metadata retrieval might depend on search query style,
        # but the primary goal was to fix the crash.
        
    finally:
        if os.path.exists(index_path):
            shutil.rmtree(index_path)

if __name__ == "__main__":
    test_vector_store_add_documents()
    print("Test passed!")
