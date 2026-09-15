from __future__ import annotations

import hashlib
from pathlib import Path

from .models import ChunkRecord, SymbolRecord


def _chunk_id(relative_path: str, start_line: int, end_line: int, symbol_name: str | None) -> str:
    seed = f"{relative_path}:{start_line}:{end_line}:{symbol_name or 'section'}"
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]


def chunk_symbols(file_path: str | Path, symbols: list[SymbolRecord], source_text: str) -> list[ChunkRecord]:
    path = Path(file_path)
    relative_path = str(path)
    lines = source_text.splitlines()
    chunks: list[ChunkRecord] = []

    for symbol in symbols:
        start_index = max(0, symbol.start_line - 1)
        end_index = min(len(lines), symbol.end_line)
        chunk_lines = lines[start_index:end_index]
        chunk_text = "\n".join(chunk_lines)

        chunks.append(
            ChunkRecord(
                id=_chunk_id(relative_path, symbol.start_line, symbol.end_line, symbol.name),
                file_path=str(path),
                relative_path=relative_path,
                symbol_name=symbol.name,
                chunk_type=symbol.kind,
                start_line=symbol.start_line,
                end_line=symbol.end_line,
                text=chunk_text,
                language="cpp",
                metadata={
                    "relative_path": relative_path,
                    "symbol_name": symbol.name,
                    "kind": symbol.kind,
                },
            )
        )

    return chunks
