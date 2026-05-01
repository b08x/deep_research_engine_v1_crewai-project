import httpx
import json
import os
from pathlib import Path
from typing import Dict, List

MODELS_JSON_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
CACHE_FILE = Path.home() / ".crewai" / "model_cache.json"

def fetch_latest_models() -> Dict:
    """Fetch the latest model data from LiteLLM's GitHub repository."""
    try:
        response = httpx.get(MODELS_JSON_URL, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        # Cache the data
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        
        return data
    except Exception as e:
        print(f"Error fetching models: {e}")
        # Fallback to cache if available
        if CACHE_FILE.exists():
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

def get_models_by_provider(provider: str) -> List[str]:
    """Get a list of model names for a specific provider."""
    data = fetch_latest_models()
    models = []
    
    # Standardize provider name for LiteLLM
    provider = provider.lower()
    
    for model_name, config in data.items():
        if not isinstance(config, dict):
            continue
            
        litellm_provider = config.get("litellm_provider", "").lower()
        if litellm_provider == provider:
            models.append(model_name)
        # Handle some edge cases or sub-providers
        elif provider == "google" and litellm_provider == "gemini":
            models.append(model_name)
        elif provider == "google" and litellm_provider == "vertex_ai":
            models.append(model_name)

    return sorted(list(set(models)))

def get_all_providers() -> List[str]:
    """Get a list of all unique providers from the model data."""
    data = fetch_latest_models()
    providers = set()
    for config in data.values():
        if isinstance(config, dict):
            p = config.get("litellm_provider")
            if p:
                providers.add(p.lower())
    return sorted(list(providers))
