# Crew Logic & Agent Roles

> 25 nodes · cohesion 0.10

## Key Concepts

- **ContentIngestionTool** (21 connections) — `tools/ingestion_tools.py`
- **crew.py** (12 connections) — `crew.py`
- **.run_ingestion()** (7 connections) — `tools/ingestion_tools.py`
- **._summarize()** (4 connections) — `tools/ingestion_tools.py`
- **._arun()** (3 connections) — `tools/ingestion_tools.py`
- **._recursive_chunk()** (3 connections) — `tools/ingestion_tools.py`
- **._run()** (3 connections) — `tools/ingestion_tools.py`
- **Implements the hierarchical separator strategy.** (3 connections) — `tools/ingestion_tools.py`
- **Summarizes a chunk using an LLM (Pass 1).** (3 connections) — `tools/ingestion_tools.py`
- **Synchronous wrapper for the async ingestion process.** (3 connections) — `tools/ingestion_tools.py`
- **Asynchronous version of the tool.** (3 connections) — `tools/ingestion_tools.py`
- **other_steve_deep_research_mode()** (2 connections) — `crew.py`
- **other_steve_sift_fact_checker()** (2 connections) — `crew.py`
- **senior_research_strategist()** (2 connections) — `crew.py`
- **._extract()** (2 connections) — `tools/ingestion_tools.py`
- **BaseTool** (1 connections)
- **crew()** (1 connections) — `crew.py`
- **deep_technical_research_execution()** (1 connections) — `crew.py`
- **other_steve_pragmatic_editor()** (1 connections) — `crew.py`
- **other_steve_tree_of_thoughts_evaluator()** (1 connections) — `crew.py`
- **Creates the DeepResearchEngine crew** (1 connections) — `crew.py`
- **research_methodology_evaluation()** (1 connections) — `crew.py`
- **sift_fact_checking_and_verification()** (1 connections) — `crew.py`
- **strategy_formulation()** (1 connections) — `crew.py`
- **technical_content_synthesis()** (1 connections) — `crew.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `crew.py`
- `tools/ingestion_tools.py`

## Audit Trail

- EXTRACTED: 57 (69%)
- INFERRED: 26 (31%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*