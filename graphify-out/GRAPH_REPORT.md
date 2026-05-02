# Graph Report - deep_research_engine_v1_crewai-project  (2026-05-02)

## Corpus Check
- 9 files · ~6,911 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 173 nodes · 236 edges · 30 communities detected
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 58 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 32|Community 32]]

## God Nodes (most connected - your core abstractions)
1. `ContentIngestionTool` - 21 edges
2. `VectorStoreManager` - 18 edges
3. `DeepResearchEngineCrew` - 16 edges
4. `RedisCache` - 16 edges
5. `CrewConfigApp` - 9 edges
6. `AgentEditor` - 8 edges
7. `load_yaml_config()` - 7 edges
8. `save_yaml_config()` - 7 edges
9. `get_env_var()` - 6 edges
10. `validate_api_key()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `DeepResearchEngine crew` --uses--> `ContentIngestionTool`  [INFERRED]
  crew.py → tools/ingestion_tools.py
- `DeepResearchEngineCrew` --uses--> `ContentIngestionTool`  [INFERRED]
  crew.py → tools/ingestion_tools.py
- `DeepResearchEngineCrew` --uses--> `Train the crew for a given number of iterations.`  [INFERRED]
  crew.py → main.py
- `DeepResearchEngineCrew` --uses--> `Replay the crew execution from a specific task.`  [INFERRED]
  crew.py → main.py
- `DeepResearchEngineCrew` --uses--> `Test the crew execution and returns the results.`  [INFERRED]
  crew.py → main.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (23): App, CrewConfigApp, main(), on_fallback_provider_changed(), on_provider_changed(), on_save_agent(), on_save_inputs(), on_save_task() (+15 more)

### Community 1 - "Community 1"
Cohesion: 0.1
Nodes (10): BaseTool, other_steve_deep_research_mode(), other_steve_sift_fact_checker(), Creates the DeepResearchEngine crew, senior_research_strategist(), ContentIngestionTool, Implements the hierarchical separator strategy., Summarizes a chunk using an LLM (Pass 1). (+2 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (11): AgentEditor, InputEditor, on_agent_selected(), on_model_changed(), on_task_selected(), Check model capabilities against agent requirements and update warning., A widget for editing a task's definition., A widget for editing run input parameters. (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.17
Nodes (15): DeepResearchEngineCrew, DeepResearchEngine crew, Train the crew for a given number of iterations., Train the crew for a given number of iterations., Replay the crew execution from a specific task., Replay the crew execution from a specific task., Test the crew execution and returns the results., Test the crew execution and returns the results. (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (8): Adds context-enriched chunks to the index., Exports chunks to graphify-out/ folder format., Performs a semantic search., Initializes txtai with fallback from Ollama to local Transformers., Checks if the new model's dimensions match the existing index., Manages the txtai embeddings index with dimensionality guards and fallbacks., Backs up the existing index to avoid crashes., VectorStoreManager

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (9): BaseModel, A Redis-based caching utility with fail-open logic., Generate a hashed key: search:cache:<sha256(identifier)>, Retrieve a value from the cache. Fails open (returns None) if Redis is down., RedisCache, IngestionInput, noise_remover(), Custom spaCy component to remove noise tokens. (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.19
Nodes (14): Other Steve (Pragmatic Editor), Other Steve (Tree of Thoughts Evaluator), Other Steve (SIFT Fact-Checker), Other Steve (Deep Research Mode), Senior Research Strategist, openai/openai/gpt-4o-mini, groq/llama-3.3-70b-versatile, openai/minimax/minimax-m1 (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.25
Nodes (9): fetch_latest_models(), get_all_providers(), get_model_capabilities(), get_models_by_provider(), Fetch the latest model data from LiteLLM's GitHub repository., Get a list of model names for a specific provider., Get a list of all unique providers from the model data., Get capability flags for a specific model.          Returns dict with keys: (+1 more)

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (2): knowledge/user_preference.txt, John Doe (AI Engineer)

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Adds context-enriched chunks to the index.

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): Exports chunks to graphify-out/ folder format.

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): Performs a semantic search.

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): DeepResearchEngine crew

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Creates the DeepResearchEngine crew

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): Get the absolute path to a configuration file.

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): Load a YAML configuration file.

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): Save a dictionary to a YAML configuration file.

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Get an environment variable, loading from .env if necessary.

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Set an environment variable in the .env file.

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Check if the API key for a given provider exists in .env.

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Check model capabilities against agent requirements and update warning.

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): A widget for editing a task's definition.

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): A widget for editing run input parameters.

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): A Textual app to configure CrewAI agents and tasks.

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): DeepResearchEngine crew

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Creates the DeepResearchEngine crew

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Input schema for MyCustomTool.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): src/deep_research_engine/config/agents.yaml

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): src/deep_research_engine/config/tasks.yaml

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): openai/google/gemini-2.5-flash

## Knowledge Gaps
- **59 isolated node(s):** `Creates the DeepResearchEngine crew`, `A Redis-based caching utility with fail-open logic.`, `Generate a hashed key: search:cache:<sha256(identifier)>`, `Retrieve a value from the cache. Fails open (returns None) if Redis is down.`, `Store a value in the cache. Fails open if Redis is down.` (+54 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 8`** (2 nodes): `knowledge/user_preference.txt`, `John Doe (AI Engineer)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `Adds context-enriched chunks to the index.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `Exports chunks to graphify-out/ folder format.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `Performs a semantic search.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `DeepResearchEngine crew`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Creates the DeepResearchEngine crew`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `Get the absolute path to a configuration file.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `Load a YAML configuration file.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `Save a dictionary to a YAML configuration file.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `Get an environment variable, loading from .env if necessary.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `Set an environment variable in the .env file.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `Check if the API key for a given provider exists in .env.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Check model capabilities against agent requirements and update warning.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `A widget for editing a task's definition.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `A widget for editing run input parameters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `A Textual app to configure CrewAI agents and tasks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `DeepResearchEngine crew`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Creates the DeepResearchEngine crew`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Input schema for MyCustomTool.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `src/deep_research_engine/config/agents.yaml`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `src/deep_research_engine/config/tasks.yaml`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `openai/google/gemini-2.5-flash`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RedisCache` connect `Community 5` to `Community 0`, `Community 1`, `Community 7`?**
  _High betweenness centrality (0.232) - this node is a cross-community bridge._
- **Why does `ContentIngestionTool` connect `Community 1` to `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.198) - this node is a cross-community bridge._
- **Why does `VectorStoreManager` connect `Community 4` to `Community 1`, `Community 5`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `ContentIngestionTool` (e.g. with `DeepResearchEngineCrew` and `DeepResearchEngine crew`) actually correct?**
  _`ContentIngestionTool` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `VectorStoreManager` (e.g. with `IngestionInput` and `ContentIngestionTool`) actually correct?**
  _`VectorStoreManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `DeepResearchEngineCrew` (e.g. with `ContentIngestionTool` and `Train the crew for a given number of iterations.`) actually correct?**
  _`DeepResearchEngineCrew` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `RedisCache` (e.g. with `IngestionInput` and `ContentIngestionTool`) actually correct?**
  _`RedisCache` has 9 INFERRED edges - model-reasoned connections that need verification._