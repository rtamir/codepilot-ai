# CodePilot Project Plan

This project plan is derived from the authoritative project specification in `specs.md` and is intended to be executed incrementally, one phase at a time.

## Goal

Build a production-quality AI engineering assistant for legacy C++ codebases that can:
- index a codebase
- answer natural-language questions with source citations
- find definitions and references
- inspect dependency/call relationships
- investigate bugs with an AI agent
- generate GoogleTest cases
- perform AI code review
- run locally with Docker
- integrate CI automation

## Source of truth

- `specs.md` defines the project scope, architecture, constraints, tech stack, and phase roadmap.
- `plan.md` describes the execution strategy.
- `tasks.md` breaks the work into incremental, reviewable steps.

We do not maintain multiple parallel feature specs. The project remains a single evolving plan with phased implementation.

## Architecture direction

The target architecture is:

User
  ↓
Streamlit UI
  ↓
FastAPI API
  ↓
Agent Router
  ↓
  ├── Code RAG
  ├── Code Graph
  ├── Git Tools
  ├── Code Search
  └── Test Runner
  ↓
LLM provider abstraction (Ollama-first, later swappable)
  ↓
Answer + source citations

## Core technical choices

- Python 3.12+
- FastAPI + Pydantic
- Streamlit UI
- Ollama as default local LLM provider
- sentence-transformers for embeddings
- ChromaDB for vector storage
- Tree-sitter with C++ grammar for syntax-aware code parsing
- pytest for Python tests
- GoogleTest for sample C++ tests
- Docker + docker-compose for deployment
- GitHub Actions for CI

## Development principles

- Clean architecture, with domain logic separated from infra and UI
- Provider abstraction for LLM, embeddings, and vector DB
- Incremental delivery; no giant all-at-once implementation
- Verification before moving to the next phase
- No fabricated metrics; all evaluation depends on real data
- Prefer simple, justified solutions over premature complexity

## Phase roadmap

### Phase 1 — Environment + local LLM setup
Status: Complete

Deliverables:
- project venv setup
- requirements install
- minimal Ollama client
- smoke test confirming model response

Validation:
- local `chat()` call succeeds
- real LLM response returned from `llama3.2:3b`

### Phase 2 — Code ingestion
Status: Next

Deliverables:
- fictional C++ sample codebase under `sample_code/`
- file discovery
- syntax-aware parsing with Tree-sitter
- symbol extraction
- semantic chunking by function/class boundary
- metadata model for file/symbol/chunk records

Validation:
- parser can extract classes/functions from representative files
- chunk metadata records are stable and useful for search

### Phase 3 — Embeddings abstraction
Deliverables:
- `EmbeddingProvider` abstraction
- sentence-transformers implementation
- embedding generation for code chunks

### Phase 4 — Vector DB integration
Deliverables:
- ChromaDB integration
- `search_code(query, top_k)` functionality
- metadata filtering and retrieval pipeline

### Phase 5 — RAG pipeline
Deliverables:
- query → embed → retrieve → prompt → model → answer
- source citations and answer grounding

### Phase 6 — Code intelligence
Deliverables:
- definition lookup
- reference lookup
- caller/implementation search
- class hierarchy introspection

### Phase 7 — Dependency and call graph
Deliverables:
- graph generation for modules and calls
- relationship visualization and analysis

### Phase 8 — Engineering agent
Deliverables:
- tool-using agent
- structured logs and observability
- investigation workflow for bug analysis

### Phase 9 — GoogleTest generation
Deliverables:
- test generation by function or class
- mockable generation workflow

### Phase 10 — AI code review
Deliverables:
- diff analysis
- severity-based review report

### Phase 11 — Evaluation framework
Deliverables:
- retrieval metrics
- citation accuracy checks
- answer correctness checks
- hallucination detection
- latency measurement

### Phase 12 — FastAPI API
Deliverables:
- `/index`
- `/query`
- `/search`
- `/agent/investigate`
- `/generate-tests`
- `/review`
- `/health`

### Phase 13 — Streamlit UI
Deliverables:
- chat interface
- search UI
- architecture view
- bug investigation view
- test generation view
- review view

### Phase 14 — Docker deployment
Deliverables:
- Dockerfile and docker-compose setup
- local Ollama integration guidance

### Phase 15 — GitHub Actions CI
Deliverables:
- install, lint, test, and smoke integration checks
- mocked LLM behavior for deterministic CI

## Execution rule

Implement one phase at a time. For each phase:
1. Explain the objective
2. Explain the architecture affected
3. State the exact implementation scope
4. Make the required code changes
5. Validate with real commands
6. Record results and decide whether to move to the next phase

## Done criteria for a phase

A phase is considered complete only when:
- the feature works in the local environment
- tests or smoke checks pass
- the implementation matches the project architecture
- the code is commit-ready and documented enough to continue

## Recommended next phase

Phase 2: Code ingestion pipeline.

This is the first substantive project feature after the initial Ollama client and should be implemented in a focused, deliberate manner before moving into retrieval or agent layers.
