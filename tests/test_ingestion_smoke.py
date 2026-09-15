from pathlib import Path

from codepilot.ingestion.pipeline import ingest_codebase


def test_ingestion_smoke() -> None:
    project_root = Path(__file__).resolve().parents[1]
    sample_root = project_root / "sample_code"

    result = ingest_codebase(sample_root)

    assert result.files_seen >= 4
    assert result.symbols_found > 0
    assert result.chunks_created > 0
    assert any(
        chunk.symbol_name and "FuelController" in chunk.symbol_name for chunk in result.chunks
    )
