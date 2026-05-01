import os
import yaml
import hashlib
import redis
import logging
from pathlib import Path
from typing import Optional, Any
from dotenv import load_dotenv, set_key

logger = logging.getLogger(__name__)

class RedisCache:
    """A Redis-based caching utility with fail-open logic."""
    
    def __init__(self, host: str = None, port: int = 6379, db: int = 0):
        self.host = host or get_env_var("REDIS_HOST") or "localhost"
        self.port = int(get_env_var("REDIS_PORT") or port)
        self.db = int(get_env_var("REDIS_DB") or db)
        self.client: Optional[redis.Redis] = None
        self._connected = False
        self._try_connect()

    def _try_connect(self):
        try:
            self.client = redis.Redis(
                host=self.host, 
                port=self.port, 
                db=self.db, 
                socket_timeout=2.0,
                socket_connect_timeout=2.0,
                decode_responses=True
            )
            self.client.ping()
            self._connected = True
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning(f"Redis cache unavailable at {self.host}:{self.port}. Failing open. Error: {e}")
            self._connected = False
            self.client = None

    def _get_key(self, identifier: str) -> str:
        """Generate a hashed key: search:cache:<sha256(identifier)>"""
        hashed = hashlib.sha256(identifier.encode()).hexdigest()
        return f"search:cache:{hashed}"

    def get(self, identifier: str) -> Optional[str]:
        """Retrieve a value from the cache. Fails open (returns None) if Redis is down."""
        if not self._connected:
            return None
        try:
            return self.client.get(self._get_key(identifier))
        except Exception as e:
            logger.warning(f"Redis get failed: {e}")
            return None

    def set(self, identifier: str, value: str, ttl: int = 3600):
        """Store a value in the cache. Fails open if Redis is down."""
        if not self._connected:
            return
        try:
            self.client.set(self._get_key(identifier), value, ex=ttl)
        except Exception as e:
            logger.warning(f"Redis set failed: {e}")

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
