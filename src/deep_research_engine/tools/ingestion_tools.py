import json
import asyncio
import hashlib
from typing import List, Dict, Optional, Any, Type
from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools import BaseTool
import trafilatura
import spacy
from spacy.language import Language
from deep_research_engine.utils import RedisCache, logger, get_env_var
from deep_research_engine.vector_store import VectorStoreManager
from crewai import LLM

# Load spacy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If not present, download it or handle gracefully
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

@Language.component("noise_remover")
def noise_remover(doc):
    """Custom spaCy component to remove noise tokens."""
    # Logic to filter out tokens that are likely boilerplate or non-semantic
    # For now, just a placeholder that could be expanded
    return doc

if "noise_remover" not in nlp.pipe_names:
    nlp.add_pipe("noise_remover", last=True)

class IngestionInput(BaseModel):
    """Input for ContentIngestionTool."""
    source: str = Field(..., description="The URL or local file path to ingest.")

class ContentIngestionTool(BaseTool):
    name: str = "Content Ingestion Tool"
    description: str = (
        "Ingests content from a URL or local file, performs clean extraction, "
        "hierarchical recursive chunking, and two-pass LLM contextualization "
        "to prevent context drift and reduce token bloat."
    )
    # Don't override args_schema with a type hint here to preserve BaseTool's serializer
    _cache: RedisCache = PrivateAttr()
    embedding_provider: str = Field(
        default_factory=lambda: get_env_var("EMBEDDING_PROVIDER") or "ollama", 
        description="The provider for embeddings."
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        self._cache = RedisCache()
        self.args_schema = IngestionInput

    def _run(self, source: str) -> str:
        """Synchronous wrapper for the async ingestion process."""
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                # If we're already in a loop, we can't use asyncio.run
                # We should ideally be using _arun, but as a fallback:
                import threading
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.run_ingestion(source, provider=self.embedding_provider))
                    return future.result()
            return asyncio.run(self.run_ingestion(source, provider=self.embedding_provider))
        except RuntimeError:
            # No running loop, safe to use asyncio.run
            return asyncio.run(self.run_ingestion(source, provider=self.embedding_provider))

    async def _arun(self, source: str) -> str:
        """Asynchronous version of the tool."""
        return await self.run_ingestion(source, provider=self.embedding_provider)

    async def run_ingestion(self, source: str, provider: str = "ollama") -> str:
        # 1. Cache Check (Raw)
        cached_raw = self._cache.get(f"raw:{source}")
        if cached_raw:
            logger.info(f"Cache hit for raw extraction: {source}")
            raw_text = cached_raw
        else:
            # 2. Extraction
            raw_text = await self._extract(source)
            if raw_text:
                self._cache.set(f"raw:{source}", raw_text)
        
        if not raw_text:
            return f"Failed to extract content from {source}"

        # 3. Noise Removal (spaCy)
        doc = nlp(raw_text)
        clean_text = doc.text # In a real impl, we'd rebuild from filtered tokens

        # 4. Hierarchical Recursive Chunking (Parent-Child)
        parents = self._recursive_chunk(clean_text, max_size=2000)
        
        # 5. Two-Pass Contextualization
        enriched_chunks = []
        for parent_content in parents:
            # Pass 1: Parent Summary
            parent_cache_key = f"summary:{hashlib.sha256(parent_content.encode()).hexdigest()}"
            parent_summary = self._cache.get(parent_cache_key)
            
            if not parent_summary:
                parent_summary = await self._summarize(parent_content)
                self._cache.set(parent_cache_key, parent_summary)
            
            # Sub-chunk into children
            children = self._recursive_chunk(parent_content, max_size=500)
            
            # Pass 2: Context Injection
            for child_content in children:
                enriched = f"[Context: {parent_summary}]\n\n{child_content}"
                enriched_chunks.append(enriched)

        # 6. Indexing & Graphify Hook (Phase 4)
        vstore = VectorStoreManager(provider=provider)
        source_hash = hashlib.sha256(source.encode()).hexdigest()
        vstore.add_documents(enriched_chunks, {"source": source, "source_hash": source_hash})

        return json.dumps({
            "source": source,
            "chunks": enriched_chunks
        })

    async def _extract(self, source: str) -> Optional[str]:
        if source.startswith(("http://", "https://")):
            downloaded = trafilatura.fetch_url(source)
            if downloaded:
                return trafilatura.extract(downloaded)
        else:
            # Placeholder for Kreuzberg local file extraction (Phase 3)
            try:
                from kreuzberg import extract_file
                result = await extract_file(source)
                return result.content
            except Exception as e:
                logger.error(f"Kreuzberg extraction failed for {source}: {e}")
        return None

    def _recursive_chunk(self, text: str, max_size: int) -> List[str]:
        """Implements the hierarchical separator strategy."""
        separators = ["\n\n", "\n", ". ", "? ", "! ", " ", ""]
        
        def split_recursive(content: str, sep_idx: int) -> List[str]:
            if len(content) <= max_size or sep_idx >= len(separators):
                return [content]
            
            sep = separators[sep_idx]
            if sep == "": # Character split
                return [content[i:i+max_size] for i in range(0, len(content), max_size)]
            
            # Try splitting by current separator
            parts = content.split(sep)
            chunks = []
            current_chunk = ""
            
            for part in parts:
                potential_chunk = (current_chunk + sep + part) if current_chunk else part
                if len(potential_chunk) <= max_size:
                    current_chunk = potential_chunk
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    
                    # If the part itself is bigger than max_size, recurse
                    if len(part) > max_size:
                        sub_parts = split_recursive(part, sep_idx + 1)
                        chunks.extend(sub_parts)
                        current_chunk = ""
                    else:
                        current_chunk = part
            
            if current_chunk:
                chunks.append(current_chunk)
            
            return chunks

        return split_recursive(text, 0)

    async def _summarize(self, content: str) -> str:
        """Summarizes a chunk using an LLM (Pass 1)."""
        # Using a default fast model for summaries
        llm = LLM(model=get_env_var("SUMMARY_MODEL") or "openrouter/google/gemini-2.0-flash-001")
        prompt = f"Provide a extremely concise one-sentence summary of the following text to serve as context for sub-chunks:\n\n{content[:5000]}"
        try:
            # CrewAI LLM call (assuming sync-like or simple async)
            response = llm.call([{"role": "user", "content": prompt}])
            return str(response).strip()
        except Exception as e:
            logger.warning(f"Summarization failed: {e}")
            return "General context"
