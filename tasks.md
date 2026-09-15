# CodePilot Task Backlog

This file is the single project task list for incremental implementation. It is derived from `specs.md` and is intentionally organized by phase so the team can implement one milestone at a time.

## Phase 1 — Environment and local LLM setup
Status: Completed

- [x] Create Python virtual environment
- [x] Install project dependencies from `requirements.txt`
- [x] Implement minimal Ollama client in `src/codepilot/llm/ollama_client.py`
- [x] Validate a real local prompt against Ollama model `llama3.2:3b`
- [x] Confirm response structure includes text, model, latency, and token counts

## Phase 2 — Code ingestion pipeline
Status: Next

### Goal
Build an ingestion layer that can parse a realistic fictional C++ codebase without requiring a full compile.

### Tasks
- [ ] Create the fictional `sample_code/` C++ project with representative modules
- [ ] Define source file discovery rules for C++ headers and source files
- [ ] Add a parsing abstraction for C++ syntax extraction
- [ ] Integrate Tree-sitter C++ grammar for symbol discovery
- [ ] Extract classes, functions, methods, and related declarations
- [ ] Associate symbol metadata: name, kind, file path, and line numbers
- [ ] Implement chunking by semantic boundaries (function/class boundaries)
- [ ] Define normalized metadata schema for chunks
- [ ] Build a smoke test that verifies parsing and chunk creation
- [ ] Validate ingestion output on the sample codebase

### Definition of done
- A sample C++ codebase exists and is realistic enough to support analysis
- File discovery and parsing work without a build environment
- Symbol and chunk outputs are structured and usable by later retrieval logic

## Phase 3 — Embeddings abstraction
Status: Planned

- [ ] Define `EmbeddingProvider` interface
- [ ] Implement sentence-transformers provider
- [ ] Add embedding generation for code chunks
- [ ] Validate embedding output shape and metadata linkage

## Phase 4 — Vector DB and search
Status: Planned

- [ ] Add ChromaDB integration
- [ ] Store chunk metadata with embeddings
- [ ] Implement `search_code(query, top_k)` abstraction
- [ ] Test search relevance using the sample codebase

## Phase 5 — Retrieval-Augmented Generation
Status: Planned

- [ ] Build a prompt pipeline that retrieves relevant chunks
- [ ] Add answer generation with citations
- [ ] Validate grounded responses against the sample codebase
- [ ] Measure retrieval latency and answer quality

## Phase 6 — Code intelligence features
Status: Planned

- [ ] Implement `find_definition`
- [ ] Implement `find_references`
- [ ] Implement `find_callers`
- [ ] Implement `find_implementations`
- [ ] Implement class hierarchy retrieval

## Phase 7 — Dependency and call graph
Status: Planned

- [ ] Build a symbol graph for modules and call relationships
- [ ] Expose graph traversal queries for analysis
- [ ] Validate graph output on representative code paths

## Phase 8 — Engineering agent workflow
Status: Planned

- [ ] Define tool-using agent architecture
- [ ] Add logger and request tracing
- [ ] Allow investigation workflow for bug analysis
- [ ] Validate agent tool call flow and telemetry

## Phase 9 — GoogleTest generation
Status: Planned

- [ ] Design `generate_tests(function_name)` interface
- [ ] Produce valid C++ test skeletons for sample code
- [ ] Validate generated tests against the sample domain

## Phase 10 — AI code review
Status: Planned

- [ ] Build diff analysis workflow
- [ ] Rate issues by severity
- [ ] Output structured review findings
- [ ] Validate on representative code changes

## Phase 11 — Evaluation framework
Status: Planned

- [ ] Add retrieval quality evaluation
- [ ] Add citation evaluation
- [ ] Add answer correctness checks
- [ ] Add hallucination detection metrics
- [ ] Capture real latency and quality metrics

## Phase 12 — FastAPI backend
Status: Planned

- [ ] Build API app structure
- [ ] Create `/index`, `/query`, `/search` endpoints
- [ ] Create `/agent/investigate` endpoint
- [ ] Create `/generate-tests` and `/review` endpoints
- [ ] Add `/health` endpoint
- [ ] Validate endpoint behavior with tests

## Phase 13 — Streamlit UI
Status: Planned

- [ ] Create chat panel
- [ ] Create search interface
- [ ] Add architecture / graph view
- [ ] Add bug investigation dashboard
- [ ] Add test generation review view

## Phase 14 — Docker deployment
Status: Planned

- [ ] Create Dockerfile
- [ ] Configure docker-compose
- [ ] Document local Ollama setup
- [ ] Validate containerized startup flow

## Phase 15 — GitHub Actions CI
Status: Planned

- [ ] Add dependency install checks
- [ ] Add lint/test jobs
- [ ] Add smoke tests for local integration
- [ ] Add deterministic mocked LLM validation
- [ ] Validate container build path

## Execution order

1. Phase 1
2. Phase 2
3. Phase 3
4. Phase 4
5. Phase 5
6. Phase 6
7. Phase 7
8. Phase 8
9. Phase 9
10. Phase 10
11. Phase 11
12. Phase 12
13. Phase 13
14. Phase 14
15. Phase 15

Do not skip ahead to later phases before the current phase is complete and validated.
