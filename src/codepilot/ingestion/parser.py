from __future__ import annotations

from pathlib import Path

from tree_sitter import Language, Parser

from .models import SymbolRecord


def _get_cpp_language():
    try:
        import tree_sitter_cpp  # type: ignore

        return Language(tree_sitter_cpp.language())
    except Exception:
        try:
            from tree_sitter_languages import get_language  # type: ignore

            return Language(get_language("cpp"))
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "Tree-sitter C++ support is not available. Install tree-sitter and tree-sitter-cpp."
            ) from exc


def _get_name(node) -> str | None:
    candidates = ["identifier", "field_identifier", "type_identifier", "destructor_name"]
    for candidate in _walk(node):
        if candidate.type in candidates:
            return candidate.text.decode("utf-8")
    return None


def _extract_kind(node) -> str | None:
    if node.type in {"class_specifier", "struct_specifier"}:
        return "class" if "class_specifier" in node.type else "struct"
    if node.type == "function_definition":
        return "function"
    if node.type == "declaration":
        for child in node.children:
            if child.type in {"function_declarator", "field_declaration"}:
                return "function"
    return None


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def parse_cpp_file(file_path: str | Path) -> list[SymbolRecord]:
    path = Path(file_path)
    source = path.read_text(encoding="utf-8")

    parser = Parser()
    parser.language = _get_cpp_language()
    tree = parser.parse(source.encode("utf-8"))

    symbols: list[SymbolRecord] = []
    for node in _walk(tree.root_node):
        kind = _extract_kind(node)
        if kind is None:
            continue

        name = _get_name(node)
        if not name:
            continue

        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1
        symbols.append(
            SymbolRecord(
                name=name,
                kind=kind,
                file_path=str(path),
                relative_path=str(path),
                start_line=start_line,
                end_line=end_line,
            )
        )
    return symbols
