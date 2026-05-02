# DeepResearchEngine Crew

A production-grade multi-agent AI research system built on [crewAI](https://crewai.com), designed for deep technical research, fact-checking, and content synthesis. This system leverages a sophisticated content ingestion pipeline, vector embeddings, and hierarchical reasoning to deliver accurate, grounded research outputs.

## Features

### Core Capabilities
- **Deep Technical Research** - Systematic analysis bypassing marketing rhetoric to extract technical reality
- **SIFT Fact-Checking** - Rigorous evidence verification using SIFT evaluation protocols
- **Hierarchical Content Ingestion** - Multi-stage processing with parent-child chunking and two-pass LLM contextualization
- **Vector Embeddings** - Semantic search with txtai, supporting Ollama and Sentence-Transformers
- **Checkpoint & Resume** - Save and restore execution state for long-running research tasks
- **Fallback LLM Support** - Automatic failover to backup models when primary fails

### Content Ingestion Pipeline
The `ContentIngestionTool` implements a robust 6-stage processing pipeline:
1. **Cache Check** - Redis-based caching for previously processed content
2. **Content Extraction** - Web (trafilatura) and local file (Kreuzberg) extraction
3. **Noise Removal** - spaCy-based text cleaning with custom pipeline components
4. **Hierarchical Recursive Chunking** - Parent-child separator strategy (2000 token parents → 500 token children)
5. **Two-Pass Contextualization** - Parent summary generation followed by context injection into children
6. **Vector Indexing** - Automatic embedding and indexing with dimensionality guards

### Vector Store
- **Multi-Provider Support** - Ollama (nomic-embed-text), Sentence-Transformers (all-MiniLM-L6-v2), Mistral
- **Dimensionality Guards** - Automatic backup of existing index when model dimensions don't match
- **Graphify Integration** - Exports processed chunks to `graphify-out/` for downstream visualization
- **Metadata Preservation** - Stores source hashes and provenance with each chunk

## Installation

### Prerequisites
- Python >=3.10, <3.14
- [UV](https://docs.astral.sh/uv/) (recommended) or pip

### Quick Install

```bash
# Install UV if not already present
pip install uv

# Install dependencies
uv sync

# Or use crewai CLI
crewai install
```

### Manual Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install spaCy model (required for content ingestion)
python -m spacy download en_core_web_sm
```

## Configuration

### API Keys
Add your provider API keys to `.env`:

```bash
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
MISTRAL_API_KEY=your_mistral_key
OPENROUTER_API_KEY=your_openrouter_key

# Optional: Redis configuration for caching
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Optional: Embedding provider (default: ollama)
EMBEDDING_PROVIDER=ollama

# Optional: Summary model for ingestion pipeline
SUMMARY_MODEL=openrouter/google/gemini-2.0-flash-001
```

### Interactive Configuration (Recommended)
Launch the visual configuration dashboard to manage agents, tasks, and run parameters:

```bash
uv run configure_crew
```

The TUI provides:
- **Agent Editor** - Configure role, goal, backstory, LLM provider/model, and capability requirements
- **Task Editor** - Define task descriptions, expected outputs, and agent assignments
- **Input Parameters** - Set grounding context, primary topic, sub-nodes, and target audience
- **API Key Validation** - Real-time checking of provider API keys
- **Model Capability Matching** - Validates that selected models support required capabilities (vision, reasoning, tool calling, structured output)
- **Fallback LLM Configuration** - Set primary and fallback models with automatic failover

### Manual Configuration Files
- `src/deep_research_engine/config/agents.yaml` - Agent definitions
- `src/deep_research_engine/config/tasks.yaml` - Task definitions
- `src/deep_research_engine/config/inputs.yaml` - Run parameters

## Usage

### Basic Research Run

```bash
# Run with default inputs
uv run deep_research_engine run

# Or using crewai CLI
crewai run
```

### Advanced Usage

```bash
# Run with custom document ingestion
uv run deep_research_engine run --doc-path ./research_paper.pdf --embedding-provider ollama

# Resume from checkpoint
uv run deep_research_engine run --resume

# Train the crew
uv run deep_research_engine train <iterations> <filename>

# Replay from specific task
uv run deep_research_engine replay <task_id>

# Test execution
uv run deep_research_engine test <iterations> <openai_model_name>
```

### Input Parameters
Create or modify `src/deep_research_engine/config/inputs.yaml`:

```yaml
grounding_context: ""  # Optional: Pre-loaded context for grounding
primary_topic: "AI Research Methodologies"
sub_nodes: 
  - "Large Language Models"
  - "Evaluation Metrics"
  - "Ethical Considerations"
target_audience: "Senior Engineers"
```

## Architecture

### Agents
The system includes five specialized agents, each with distinct capabilities:

| Agent | Role | Default Model | Tools | Specialization |
|-------|------|---------------|-------|----------------|
| `senior_research_strategist` | Strategy Formulation | glm-4.7-flash | SerperDev, EXA Search, Content Ingestion, FileWriter | Identifies research gaps, audience analysis |
| `other_steve_deep_research_mode` | Deep Technical Research | mistral-medium-latest | SerperDev, EXA Search, Content Ingestion, Arxiv, FileWriter | Architecture analysis, trade-off evaluation |
| `other_steve_sift_fact_checker` | SIFT Fact-Checker | glm-4.7 | SerperDev, EXA Search, Content Ingestion, FileWriter | Evidence verification, source reliability |
| `other_steve_pragmatic_editor` | Pragmatic Editor | magistral-medium-latest | FileWriter | Precision filtering, conciseness |
| `other_steve_tree_of_thoughts_evaluator` | Tree of Thoughts Evaluator | glm-4.7 | FileWriter | Multi-path analysis, failure mode identification |

All agents support:
- Custom LLM configuration (temperature, top_p, top_k, max_tokens)
- Fallback LLM models
- Capability requirement validation (vision, reasoning, tool calling, structured output)

### Workflow
```
Strategy Formulation → Deep Technical Research → SIFT Fact-Checking → 
Research Methodology Evaluation → Technical Content Synthesis
```

### Tools
- **SerperDevTool** - Web search
- **EXASearchTool** - Enhanced search
- **ArxivPaperTool** - Academic paper retrieval
- **FileWriterTool** - Output generation
- **ContentIngestionTool** - Multi-stage content processing

## Development

### Running Tests

```bash
# Run vector store tests
uv run pytest tests/test_vector_store.py

# Or with pytest directly
pytest tests/test_vector_store.py
```

### Project Structure
```
deep_research_engine_v1_crewai-project/
├── src/
│   └── deep_research_engine/
│       ├── __init__.py
│       ├── crew.py              # Agent and task definitions
│       ├── main.py              # CLI entry points
│       ├── tui_config.py        # Textual-based configuration TUI
│       ├── utils.py             # Redis cache, config helpers
│       ├── models_fetcher.py    # Dynamic model loading
│       ├── vector_store.py      # txtai-based vector embeddings
│       └── tools/
│           ├── __init__.py
│           └── ingestion_tools.py # Content ingestion pipeline
│       └── config/
│           ├── agents.yaml      # Agent configurations
│           ├── tasks.yaml       # Task definitions
│           └── inputs.yaml      # Run parameters
├── tests/
│   └── test_vector_store.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Advanced Configuration

### Custom Embedding Providers
Set `EMBEDDING_PROVIDER` in `.env`:
- `ollama` - Uses Ollama's nomic-embed-text (default)
- `mistral` - Uses Mistral embeddings
- `local` - Uses Sentence-Transformers (all-MiniLM-L6-v2)

### Redis Configuration
For distributed caching:

```bash
REDIS_HOST=your_redis_host
REDIS_PORT=6379
REDIS_DB=0
```

### Model Fallback Configuration
Each agent can have a primary and fallback LLM:

```yaml
senior_research_strategist:
  llm: openrouter/z-ai/glm-4.7-flash
  fallback_llm: openai/gpt-4o-mini
  llm_config:
    temperature: 0.2
    top_p: 0.9
    top_k: null
    max_tokens: 8192
```

### Checkpoint Management
Checkpoints are automatically saved to `.checkpoints/` directory. To resume:

```bash
uv run deep_research_engine run --resume
```

The system will automatically find the latest checkpoint and restore execution state.

## Dependencies

### Core Dependencies
- crewai[file-processing,litellm,tools]==1.14.4
- exa-py
- pydantic
- python-dotenv

### Content Ingestion
- trafilatura - Web content extraction
- spacy - NLP processing
- spacy-llm - LLM integration for spaCy
- kreuzberg - Local file extraction

### Vector Store
- txtai[ann,pipeline,similarity] - Embeddings and semantic search
- redis - Distributed caching

### Development
- pytest>=9.0.3

## Support

For support, questions, or feedback regarding DeepResearchEngine:
- Visit our [documentation](https://docs.crewai.com)
- Reach out through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

---

**Built with crewAI** - Let's create wonders together with the power and simplicity of multi-agent AI systems.
