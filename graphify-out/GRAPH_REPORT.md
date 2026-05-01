# Graph Report - .  (2026-04-30)

## Corpus Check
- Corpus is ~6,086 words - fits in a single context window. You may not need a graph.

## Summary
- 60 nodes · 67 edges · 7 communities detected
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Core Agent Logic and LLM Models|Core Agent Logic and LLM Models]]
- [[_COMMUNITY_Crew Execution and CLI Operations|Crew Execution and CLI Operations]]
- [[_COMMUNITY_Custom Tool Implementation and Schemas|Custom Tool Implementation and Schemas]]
- [[_COMMUNITY_Research Strategy and Search Tools|Research Strategy and Search Tools]]
- [[_COMMUNITY_Crew Configuration and Task definitions|Crew Configuration and Task definitions]]
- [[_COMMUNITY_User Preferences and Identity Metadata|User Preferences and Identity Metadata]]
- [[_COMMUNITY_Crew Creation Rationale|Crew Creation Rationale]]

## God Nodes (most connected - your core abstractions)
1. `DeepResearchEngineCrew` - 9 edges
2. `DeepResearchEngineCrew` - 7 edges
3. `Other Steve (Deep Research Mode)` - 7 edges
4. `Senior Research Strategist` - 6 edges
5. `deep_technical_research_execution` - 5 edges
6. `sift_fact_checking_and_verification` - 4 edges
7. `research_methodology_evaluation` - 4 edges
8. `technical_content_synthesis` - 4 edges
9. `train()` - 3 edges
10. `replay()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Train the crew for a given number of iterations.` --uses--> `DeepResearchEngineCrew`  [INFERRED]
  main.py → crew.py
- `Replay the crew execution from a specific task.` --uses--> `DeepResearchEngineCrew`  [INFERRED]
  main.py → crew.py
- `Test the crew execution and returns the results.` --uses--> `DeepResearchEngineCrew`  [INFERRED]
  main.py → crew.py
- `run()` --calls--> `DeepResearchEngineCrew`  [INFERRED]
  main.py → crew.py
- `Other Steve (Deep Research Mode)` --calls--> `openai/openai/gpt-4o-mini`  [EXTRACTED]
  src/deep_research_engine/config/agents.yaml → src/deep_research_engine/crew.py

## Communities

### Community 0 - "Core Agent Logic and LLM Models"
Cohesion: 0.2
Nodes (14): Other Steve (Pragmatic Editor), Other Steve (Tree of Thoughts Evaluator), Other Steve (SIFT Fact-Checker), DeepResearchEngineCrew, src/deep_research_engine/main.py, openai/google/gemini-2.5-flash, openai/openai/gpt-4o-mini, openai/minimax/minimax-m1 (+6 more)

### Community 2 - "Crew Execution and CLI Operations"
Cohesion: 0.33
Nodes (9): DeepResearchEngineCrew, DeepResearchEngine crew, Train the crew for a given number of iterations., Replay the crew execution from a specific task., Test the crew execution and returns the results., replay(), run(), test() (+1 more)

### Community 3 - "Custom Tool Implementation and Schemas"
Cohesion: 0.29
Nodes (5): BaseModel, BaseTool, MyCustomTool, MyCustomToolInput, Input schema for MyCustomTool.

### Community 4 - "Research Strategy and Search Tools"
Cohesion: 0.38
Nodes (7): Other Steve (Deep Research Mode), Senior Research Strategist, groq/llama-3.3-70b-versatile, ArxivPaperTool, EXASearchTool, ScrapeWebsiteTool, SerperDevTool

### Community 5 - "Crew Configuration and Task definitions"
Cohesion: 0.67
Nodes (3): src/deep_research_engine/config/agents.yaml, src/deep_research_engine/crew.py, src/deep_research_engine/config/tasks.yaml

### Community 6 - "User Preferences and Identity Metadata"
Cohesion: 1.0
Nodes (2): knowledge/user_preference.txt, John Doe (AI Engineer)

### Community 8 - "Crew Creation Rationale"
Cohesion: 1.0
Nodes (1): Creates the DeepResearchEngine crew

## Knowledge Gaps
- **13 isolated node(s):** `DeepResearchEngine crew`, `Creates the DeepResearchEngine crew`, `Input schema for MyCustomTool.`, `src/deep_research_engine/main.py`, `src/deep_research_engine/config/agents.yaml` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `User Preferences and Identity Metadata`** (2 nodes): `knowledge/user_preference.txt`, `John Doe (AI Engineer)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Crew Creation Rationale`** (1 nodes): `Creates the DeepResearchEngine crew`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.