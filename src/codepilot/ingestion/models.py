from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceFileInfo:
    path: str
    relative_path: str
    language: str = "cpp"


@dataclass
class SymbolRecord:
    name: str
    kind: str
    file_path: str
    relative_path: str
    start_line: int
    end_line: int
    parent_symbol: str | None = None


@dataclass
class ChunkRecord:
    id: str
    file_path: str
    relative_path: str
    symbol_name: str | None
    chunk_type: str
    start_line: int
    end_line: int
    text: str
    language: str = "cpp"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class IngestionResult:
    files_seen: int = 0
    symbols_found: int = 0
    chunks_created: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    chunks: list[ChunkRecord] = field(default_factory=list)
    symbols: list[SymbolRecord] = field(default_factory=list)
