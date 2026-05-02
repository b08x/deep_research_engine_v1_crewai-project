# Caching & Tool Infrastructure

> 16 nodes · cohesion 0.16

## Key Concepts

- **RedisCache** (16 connections) — `utils.py`
- **IngestionInput** (5 connections) — `tools/ingestion_tools.py`
- **.get()** (4 connections) — `utils.py`
- **._get_key()** (4 connections) — `utils.py`
- **ingestion_tools.py** (4 connections) — `tools/ingestion_tools.py`
- **.__init__()** (3 connections) — `utils.py`
- **Custom spaCy component to remove noise tokens.** (3 connections) — `tools/ingestion_tools.py`
- **Input for ContentIngestionTool.** (3 connections) — `tools/ingestion_tools.py`
- **._try_connect()** (2 connections) — `utils.py`
- **.__init__()** (2 connections) — `tools/ingestion_tools.py`
- **noise_remover()** (2 connections) — `tools/ingestion_tools.py`
- **BaseModel** (1 connections)
- **A Redis-based caching utility with fail-open logic.** (1 connections) — `utils.py`
- **Generate a hashed key: search:cache:<sha256(identifier)>** (1 connections) — `utils.py`
- **Retrieve a value from the cache. Fails open (returns None) if Redis is down.** (1 connections) — `utils.py`
- **__init__.py** (1 connections) — `tools/__init__.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `tools/__init__.py`
- `tools/ingestion_tools.py`
- `utils.py`

## Audit Trail

- EXTRACTED: 37 (70%)
- INFERRED: 16 (30%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*