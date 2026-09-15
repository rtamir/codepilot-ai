"""
Phase 1 sanity check: confirm we can call the local LLM from Python
and get a real, non-empty response back.
"""

import sys
import os

# Allow running this script directly without installing the package yet.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from codepilot.llm.ollama_client import chat


def main():
    prompt = "In one sentence, what does a fuel dispenser controller in a gas station system typically do?"

    print(f"Sending prompt: {prompt!r}\n")
    result = chat(prompt)

    print("--- Response ---")
    print(result.text)
    print("\n--- Stats ---")
    print(f"Model:              {result.model}")
    print(f"Latency:            {result.latency_seconds:.2f}s")
    print(f"Prompt tokens:      {result.prompt_tokens}")
    print(f"Completion tokens:  {result.completion_tokens}")


if __name__ == "__main__":
    main()