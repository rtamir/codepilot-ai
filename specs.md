# CodePilot — Project Specification

**AI Engineering Assistant for Legacy C++ Codebases**

This document is the authoritative spec for the CodePilot project. It captures the full design, constraints, methodology, and current build status so development can continue in any IDE, with any AI coding assistant, or by a human engineer picking this up cold.

---

## 1. Project Objective

Build a production-quality, portfolio-grade AI engineering assistant that lets a developer:

1. Load/index a C++ codebase
2. Ask natural-language questions about the code
3. Perform semantic code search
4. Find classes, functions, definitions, and references
5. Understand relationships between components
6. Get RAG-generated answers with source-file/line citations
7. Explore a code dependency/call graph
8. Use an AI agent to investigate bugs
9. Generate GoogleTest test cases
10. Get AI-assisted code reviews
11. Evaluate retrieval and answer quality with real metrics
12. Run locally via Docker
13. Rely on automated CI via GitHub Actions

This is meant to be discussed in a senior/lead software engineering interview — it must demonstrate real engineering judgment, not just LLM API calls wrapped in a UI.

---

## 2. Constraints

- **No proprietary employer code.** The codebase under analysis is a **fictional but realistic** system inspired by enterprise fuel/POS/dispenser systems.
- Target: ~15–30 C++ source/header files representing a moderately complex system, with realistic classes, interfaces, inheritance, composition, function calls, error handling, configuration, logging, and unit tests.
- Example components: `FuelController`, `TransactionManager`, `PaymentProcessor`, `DispenserComm`, `FuelSession`, `Transaction`, `DeviceManager`, `ConfigurationManager`, `Logger`, `AlarmManager`, `NetworkManager`, `PriceManager`.

---

## 3. Target Architecture

```
User
  ↓
Web UI (Streamlit)
  ↓
FastAPI
  ↓
Agent Router
  ↓
  ├── Code RAG
  ├── Code Graph
  ├── Git Tools
  ├── Code Search
  └── Test Runner
  ↓
LLM (Ollama → later swappable: OpenAI / Anthropic / OpenRouter / OpenAI-compatible)
  ↓
Answer + source citations
```

**Design principle:** clean separation between domain logic, infrastructure, LLM providers, vector database, API, and UI. All external providers (LLM, embeddings, vector DB) sit behind interfaces so they're swappable — never tightly couple business logic to one vendor.

---

## 4. Technology Stack

| Layer | Choice | Notes |
|---|---|---|
| Backend | Python 3.12+ | Project is pinned to 3.12 via venv, regardless of system Python version |
| API framework | FastAPI + Pydantic | |
| LLM (local) | Ollama, `llama3.2:3b` | Chosen for CPU-only inference on constrained RAM (~16GB total, ~5GB free). Kept behind an abstraction for later swap to OpenAI/Anthropic/OpenRouter |
| Embeddings | sentence-transformers | Behind an `EmbeddingProvider` interface |
| Vector DB | ChromaDB | |
| C++ parsing | Tree-sitter (`tree-sitter-cpp` grammar) | AST-based chunking, not naive text splitting — see rationale below |
| UI | Streamlit | Clean UI/API separation from FastAPI backend |
| Python testing | pytest | |
| C++ testing (fictional codebase) | GoogleTest | |
| Containerization | Docker + docker-compose | Ollama may run outside the app container — document both local and Docker setups |
| CI | GitHub Actions | Mocked/deterministic LLM interfaces in CI — no dependency on downloading a large local LLM in CI |

### Why Tree-sitter (not a full compiler frontend)

- Full compiler frontends (e.g. Clang libclang AST) give the most accurate semantics but require the code to actually compile with correct include paths/flags — fragile for arbitrary legacy repos that may not build cleanly outside their original environment.
- Tree-sitter parses **syntax**, not full semantics. It doesn't resolve overloads or deep data flow, but doesn't need the code to compile either. It's fast, incremental, and has a mature C++ grammar.
- This trade-off (robustness/speed over full semantic precision) mirrors what tools like GitHub's code search and `nvim-treesitter` do.
- Known limitation: Tree-sitter alone won't trace calls made through member pointers set elsewhere — that kind of deep call-graph reasoning is handled separately in Phase 7, built on top of Tree-sitter's structural output.

---

## 5. Repository Structure

```
codepilot-ai/
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── .gitignore
│
├── src/
│   └── codepilot/
│       ├── api/
│       ├── ingestion/
│       ├── embeddings/
│       ├── retrieval/
│       ├── parsing/
│       ├── graph/
│       ├── llm/
│       ├── agents/
│       ├── tools/
│       ├── evaluation/
│       └── config/
│
├── tests/
│
├── sample_code/
│   ├── include/
│   ├── src/
│   └── tests/
│
├── evaluation/
│
├── docs/
│   ├── architecture.md
│   ├── design-decisions.md
│   └── evaluation.md
│
├── scripts/
│
└── .github/
    └── workflows/
        └── ci.yml
```

Structure may evolve, but any major structural change should be explained before being made.

---

## 6. Development Methodology (IMPORTANT — how to work on this project)

Build **incrementally**. Never generate the entire project in one large response/commit. For every development step:

1. Explain the objective
2. Explain the architecture involved
3. State exactly what's being implemented
4. Create/update the required files
5. Show complete contents of newly created files
6. Clearly identify which files changed
7. Give exact commands to run
8. State expected output
9. Provide a small test/check to verify it works
10. Only then move to the next step

**Audience assumption:** experienced software engineer, relatively new to LLM application development. Explain AI/LLM concepts when encountered (tied to the actual implementation, not abstract theory). Do not over-explain basic programming/software engineering concepts.

**Working style expected from the assistant:** act as senior software architect / AI engineer / Python mentor / C++ expert / code reviewer / GitHub project mentor. Challenge poor design decisions, present trade-offs and recommend an approach rather than agreeing by default, prefer simple solutions first and add complexity only when justified.

---

## 7. Development Phases

| Phase | Description | Status |
|---|---|---|
| 1 | Environment + local LLM setup | ✅ **Done** |
| 2 | Code ingestion (Tree-sitter parsing → chunks with metadata) | ⏭ **Next** |
| 3 | Embeddings abstraction (`EmbeddingProvider`, sentence-transformers impl) | Not started |
| 4 | Vector database (ChromaDB integration, `search_code(query, top_k)`) | Not started |
| 5 | RAG pipeline (query → embed → retrieve → prompt → LLM → cited answer) | Not started |
| 6 | Code intelligence (`find_definition`, `find_references`, `find_callers`, `find_implementations`, `get_class_hierarchy`) | Not started |
| 7 | Dependency / call graph | Not started |
| 8 | Engineering agent (tool-using, observable/logged tool calls) | Not started |
| 9 | GoogleTest generation (`generate_tests(function_name)`) | Not started |
| 10 | AI code review workflow (diff → analysis → severity-rated report) | Not started |
| 11 | Evaluation (retrieval accuracy, citation accuracy, answer correctness, hallucination rate, latency — real measured numbers only) | Not started |
| 12 | FastAPI endpoints (`/index`, `/query`, `/search`, `/agent/investigate`, `/generate-tests`, `/review`, `/health`) | Not started |
| 13 | Streamlit UI (Chat, Search, Architecture, Bug Investigation, Test Generation, Code Review) | Not started |
| 14 | Docker containerization (careful handling of Ollama running outside the app container) | Not started |
| 15 | GitHub Actions CI (install, lint, unit tests, integration tests where practical, Docker build; mocked LLM for determinism) | Not started |

---

## 8. Engineering Principles

- **Clean architecture:** separate domain logic, infrastructure, LLM providers, vector database, API, UI.
- **Dependency inversion:** LLM/vector/embedding providers must be replaceable behind interfaces.
- **Configuration:** environment variables/config, never hard-coded credentials or model names.
- **Security:** never commit API keys; never execute arbitrary user-supplied shell commands; treat generated code as untrusted; sandbox test execution where appropriate.
- **Observability:** log request ID, retrieval latency, LLM latency, number of retrieved chunks, tool calls, and errors — without logging sensitive source code unnecessarily.

## 9. Code Quality Expectations

Type hints, docstrings where useful, meaningful names, small focused functions, interfaces/protocols where appropriate, dependency injection where useful, structured logging, unit tests, proper error handling. Avoid unnecessary abstractions and frameworks adopted just because they're popular.

---

## 10. LLM/AI Concepts to Cover While Building

Explain these when encountered, tied to the actual implementation: tokens, context window, embeddings, vector search, cosine similarity, RAG, chunking, metadata filtering, reranking, prompt engineering, hallucination, temperature, tool calling, agents, function calling, structured output, AST, semantic search, evaluation, inference, quantization, local LLMs, model serving.

---

## 11. Git Strategy

At the end of each meaningful phase, provide:
1. Suggested commit message (conventional-commits style, e.g. `feat: implement semantic code search`)
2. Files changed
3. What the commit demonstrates

Keep commits logically separated per phase/sub-step.

---

## 12. README Requirements (to build out over time)

Eventually produce a README containing: Problem, Solution, Architecture (ASCII diagram), Features, Technology, Demo (screenshots/GIF instructions), Example questions, RAG pipeline explanation, Agent architecture, Evaluation (real measured metrics only — no fabricated numbers), Running locally, Docker instructions, Project structure, Design decisions (link to `docs/design-decisions.md`), honest Limitations, and Future improvements (reranking, hybrid search, MCP integration, multi-agent workflows, better C++ semantic analysis, cloud deployment, authentication, enterprise codebase integration).

---

## 13. Environment (as of Phase 1)

- **OS:** Native Windows (cmd/PowerShell) — WSL2 deliberately not used for this project
- **Python:** System default is 3.14.3; project is pinned to **3.12.10** via a dedicated venv at `codepilot-ai\venv`
- **Git:** 2.53.0
- **Docker Desktop:** 28.3.0, Compose v2.38.1
- **Ollama:** 0.34.0, model pulled: `llama3.2:3b` (2.0 GB)
- **GPU:** None (NVIDIA) — CPU-only inference
- **RAM:** 16 GB total, ~5.3 GB available at setup time — model size chosen (3B) specifically to stay comfortable within this budget
- **Working directory:** `D:\GitHubContent\codepilot-ai`

---

## 14. Current Build State (Phase 1 complete)

Files created so far:

```
codepilot-ai/
├── requirements.txt          # requests==2.32.3
├── .gitignore
├── src/
│   └── codepilot/
│       ├── __init__.py
│       └── llm/
│           ├── __init__.py
│           └── ollama_client.py   # chat() -> LLMResponse (text, model, latency, token counts)
└── scripts/
    └── test_llm_call.py      # Phase 1 verification script — confirmed working
```

`ollama_client.py` implements a minimal, provider-agnostic-shaped `chat()` function that calls Ollama's local `/api/chat` endpoint and returns a structured `LLMResponse` (text, model, latency, prompt/completion token counts). This is the seed of the eventual `LLMProvider` interface referenced in Phase 3+/Phase 5 — later swaps to OpenAI/Anthropic/OpenRouter should only require a new implementation behind the same interface, not changes to calling code.

**Verified:** `python scripts\test_llm_call.py` produces a real, coherent, non-cached response from `llama3.2:3b` with real token counts (confirmed twice, with varied prompts).

**Not yet committed to git** — first commit is pending:
```
git init
git add .
git commit -m "feat: initial project scaffold with Ollama LLM client (Phase 1)"
```

---

## 15. Next Step (Phase 2 — Code Ingestion)

Pipeline to implement:

```
C++ source files
  ↓
File discovery
  ↓
Tree-sitter parsing
  ↓
Functions/classes extraction
  ↓
Metadata attachment
  ↓
Chunks
```

Each chunk needs metadata: file, relative path, symbol, class, function, start line, end line, language, chunk type. Chunking must follow syntactic boundaries (per-function/per-class), not fixed-character splitting.

This phase also requires first creating the fictional fuel/POS C++ sample codebase (`sample_code/`) described in Section 2, since there's nothing to ingest yet.

---

## 16. How to Resume This Project

If picking this up in a different tool/IDE/assistant:

1. Share this `specs.md` in full as context.
2. State which phase is current (see Section 7 status table) and paste the actual current contents of `src/codepilot/` and `sample_code/` if they've diverged from Section 14.
3. Re-state the working methodology in Section 6 explicitly if the assistant doesn't already have it — incremental steps, no giant dumps, verification before moving on.
4. Confirm the environment details in Section 13 are still accurate (model pulled, venv active, etc.) before continuing.
