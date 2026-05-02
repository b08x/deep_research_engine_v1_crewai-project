# Vector Store Management

> 16 nodes · cohesion 0.17

## Key Concepts

- **VectorStoreManager** (18 connections) — `vector_store.py`
- **._check_dimensionality()** (5 connections) — `vector_store.py`
- **._initialize_embeddings()** (4 connections) — `vector_store.py`
- **.add_documents()** (3 connections) — `vector_store.py`
- **._backup_index()** (3 connections) — `vector_store.py`
- **._export_to_graphify()** (3 connections) — `vector_store.py`
- **.search()** (3 connections) — `vector_store.py`
- **.__init__()** (2 connections) — `vector_store.py`
- **Adds context-enriched chunks to the index.** (1 connections) — `vector_store.py`
- **Exports chunks to graphify-out/ folder format.** (1 connections) — `vector_store.py`
- **Performs a semantic search.** (1 connections) — `vector_store.py`
- **Initializes txtai with fallback from Ollama to local Transformers.** (1 connections) — `vector_store.py`
- **Checks if the new model's dimensions match the existing index.** (1 connections) — `vector_store.py`
- **Manages the txtai embeddings index with dimensionality guards and fallbacks.** (1 connections) — `vector_store.py`
- **Backs up the existing index to avoid crashes.** (1 connections) — `vector_store.py`
- **vector_store.py** (1 connections) — `vector_store.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `vector_store.py`

## Audit Trail

- EXTRACTED: 40 (82%)
- INFERRED: 9 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*