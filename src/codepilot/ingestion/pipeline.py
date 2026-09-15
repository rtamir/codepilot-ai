from __future__ import annotations

from pathlib import Path

from .chunking import chunk_symbols
from .discovery import discover_source_files
from .models import IngestionResult, SymbolRecord
from .parser import parse_cpp_file


def ingest_codebase(root: str | Path) -> IngestionResult:
    root_path = Path(root).resolve()
    files = discover_source_files(root_path)

    result = IngestionResult(files_seen=len(files))
    for file_path in files:
        try:
            source_text = file_path.read_text(encoding="utf-8")
            symbols = parse_cpp_file(file_path)
            for symbol in symbols:
                symbol.relative_path = str(file_path.relative_to(root_path))
            result.symbols.extend(symbols)
            result.chunks.extend(chunk_symbols(file_path, symbols, source_text))
        except Exception as exc:  # pragma: no cover - defensive path for invalid files
            result.warnings.append(f"{file_path}: {exc}")

    result.symbols_found = len(result.symbols)
    result.chunks_created = len(result.chunks)
    return result
