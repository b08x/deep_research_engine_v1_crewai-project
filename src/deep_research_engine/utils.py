import os
import yaml
from pathlib import Path
from dotenv import load_dotenv, set_key

def get_config_path(filename: str) -> Path:
    """Get the absolute path to a configuration file."""
    return Path(__file__).parent / "config" / filename

def load_yaml_config(filename: str) -> dict:
    """Load a YAML configuration file."""
    path = get_config_path(filename)
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def save_yaml_config(filename: str, data: dict):
    """Save a dictionary to a YAML configuration file."""
    path = get_config_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def get_env_var(key: str) -> str:
    """Get an environment variable, loading from .env if necessary."""
    load_dotenv()
    return os.getenv(key, "")

def set_env_var(key: str, value: str):
    """Set an environment variable in the .env file."""
    env_path = Path(".env")
    if not env_path.exists():
        env_path.touch()
    set_key(str(env_path), key, value)

def validate_api_key(provider: str) -> bool:
    """Check if the API key for a given provider exists in .env."""
    key_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GEMINI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    key_name = key_map.get(provider.lower())
    if not key_name:
        return True # Default to true for local/unmapped providers
    return bool(get_env_var(key_name))
