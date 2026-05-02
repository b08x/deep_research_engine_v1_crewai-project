# Integrated Toolchain

> 6 nodes · cohesion 0.33

## Key Concepts

- **Content Ingestion Tool** (4 connections) — `src/deep_research_engine/tools/ingestion_tools.py`
- **LiteLLM Model Fetcher** (2 connections) — `src/deep_research_engine/models_fetcher.py`
- **Run Command** (1 connections) — `src/deep_research_engine/main.py`
- **Crew Configuration TUI** (1 connections) — `src/deep_research_engine/tui_config.py`
- **Redis Cache Utility** (1 connections) — `src/deep_research_engine/utils.py`
- **Vector Store Manager** (1 connections) — `src/deep_research_engine/vector_store.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `src/deep_research_engine/main.py`
- `src/deep_research_engine/models_fetcher.py`
- `src/deep_research_engine/tools/ingestion_tools.py`
- `src/deep_research_engine/tui_config.py`
- `src/deep_research_engine/utils.py`
- `src/deep_research_engine/vector_store.py`

## Audit Trail

- EXTRACTED: 6 (60%)
- INFERRED: 4 (40%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*