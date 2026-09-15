# codepilot-ai

A small Python project for interacting with a local Ollama-hosted LLM from a simple client module.

## Project structure

- `src/codepilot/llm/ollama_client.py` - minimal Ollama chat client
- `scripts/test_llm_call.py` - smoke test to verify the local model can respond
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.12+
- Ollama installed and running locally
- A model available in Ollama, such as `llama3.2:3b`

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Start Ollama locally and ensure the model is available. For example:

   ```powershell
   ollama pull llama3.2:3b
   ```

## Run the smoke test

From the project root:

```powershell
python scripts/test_llm_call.py
```

This script sends a sample prompt to the local Ollama server and prints the model response along with timing/token metadata.

## Example usage

```python
from codepilot.llm.ollama_client import chat

result = chat("Write a short summary of Python.")
print(result.text)
```

## Notes

This is intentionally a minimal Phase 1 implementation. The client is designed to be a thin wrapper around the local Ollama API and can be expanded later with abstraction layers, retries, and richer prompt handling.
