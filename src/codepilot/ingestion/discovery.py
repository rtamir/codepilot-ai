from __future__ import annotations

from pathlib import Path

CPP_SUFFIXES = {".h", ".hh", ".hpp", ".hxx", ".c", ".cc", ".cpp", ".cxx", ".c++"}


def discover_source_files(root: str | Path) -> list[Path]:
    root_path = Path(root).resolve()
    if not root_path.exists():
        raise FileNotFoundError(f"Source root not found: {root_path}")

    discovered: list[Path] = []
    for path in sorted(root_path.rglob("*"), key=lambda p: str(p.relative_to(root_path))):
        if path.is_file() and path.suffix.lower() in CPP_SUFFIXES:
            discovered.append(path)
    return discovered
