# Model Fetching & Provider Logic

> 21 nodes · cohesion 0.13

## Key Concepts

- **get_models_by_provider()** (6 connections) — `models_fetcher.py`
- **update_primary_models()** (6 connections) — `tui_config.py`
- **validate_api_key()** (6 connections) — `utils.py`
- **fetch_latest_models()** (5 connections) — `models_fetcher.py`
- **._check_capabilities()** (5 connections) — `tui_config.py`
- **update_fallback_models()** (5 connections) — `tui_config.py`
- **.set()** (5 connections) — `utils.py`
- **models_fetcher.py** (5 connections) — `models_fetcher.py`
- **get_all_providers()** (4 connections) — `models_fetcher.py`
- **get_model_capabilities()** (4 connections) — `models_fetcher.py`
- **.on_mount()** (3 connections) — `tui_config.py`
- **on_fallback_provider_changed()** (2 connections) — `tui_config.py`
- **on_model_changed()** (2 connections) — `tui_config.py`
- **on_provider_changed()** (2 connections) — `tui_config.py`
- **Fetch the latest model data from LiteLLM's GitHub repository.** (1 connections) — `models_fetcher.py`
- **Get a list of model names for a specific provider.** (1 connections) — `models_fetcher.py`
- **Get a list of all unique providers from the model data.** (1 connections) — `models_fetcher.py`
- **Get capability flags for a specific model.          Returns dict with keys:** (1 connections) — `models_fetcher.py`
- **Check model capabilities against agent requirements and update warning.** (1 connections) — `tui_config.py`
- **Store a value in the cache. Fails open if Redis is down.** (1 connections) — `utils.py`
- **Check if the API key for a given provider exists in .env.** (1 connections) — `utils.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `models_fetcher.py`
- `tui_config.py`
- `utils.py`

## Audit Trail

- EXTRACTED: 53 (79%)
- INFERRED: 14 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*