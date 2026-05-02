# VectorStoreManager

> God node · 18 connections · `vector_store.py`

## Connections by Relation

### calls
- [[.run_ingestion()]] `INFERRED`

### contains
- [[vector_store.py]] `EXTRACTED`

### method
- [[._check_dimensionality()]] `EXTRACTED`
- [[._initialize_embeddings()]] `EXTRACTED`
- [[._backup_index()]] `EXTRACTED`
- [[.add_documents()]] `EXTRACTED`
- [[._export_to_graphify()]] `EXTRACTED`
- [[.search()]] `EXTRACTED`
- [[.__init__()]] `EXTRACTED`

### rationale_for
- [[Manages the txtai embeddings index with dimensionality guards and fallbacks.]] `EXTRACTED`

### uses
- [[ContentIngestionTool]] `INFERRED`
- [[IngestionInput]] `INFERRED`
- [[Custom spaCy component to remove noise tokens.]] `INFERRED`
- [[Input for ContentIngestionTool.]] `INFERRED`
- [[Synchronous wrapper for the async ingestion process.]] `INFERRED`
- [[Asynchronous version of the tool.]] `INFERRED`
- [[Implements the hierarchical separator strategy.]] `INFERRED`
- [[Summarizes a chunk using an LLM (Pass 1).]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*