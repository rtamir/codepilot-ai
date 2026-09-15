"""
Minimal client for talking to a local Ollama server.

This is intentionally thin. Later (Phase 5+) this becomes one
implementation behind an LLMProvider interface, so the rest of the
app never depends on Ollama specifically.
"""

import time
import requests
from dataclasses import dataclass


OLLAMA_BASE_URL = "http://localhost:11434"


@dataclass
class LLMResponse:
    """Wraps a model response with basic timing/usage info we'll want for observability later."""
    text: str
    model: str
    latency_seconds: float
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


def chat(prompt: str, model: str = "llama3.2:3b", temperature: float = 0.7) -> LLMResponse:
    """
    Send a single prompt to the local Ollama model and return the response.

    temperature controls randomness: 0.0 is deterministic/focused,
    higher values (e.g. 0.8+) produce more varied, creative output.
    We'll want low temperature for code analysis later and can leave
    it higher for casual testing now.
    """
    start = time.monotonic()

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": temperature},
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    elapsed = time.monotonic() - start

    return LLMResponse(
        text=data["message"]["content"],
        model=model,
        latency_seconds=elapsed,
        prompt_tokens=data.get("prompt_eval_count"),
        completion_tokens=data.get("eval_count"),
    )