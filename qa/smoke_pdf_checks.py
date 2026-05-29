from __future__ import annotations
from pathlib import Path


def assert_smoke_pdf_exists(path: str | Path) -> None:
    pdf_path = Path(path)
    if not pdf_path.exists() or pdf_path.stat().st_size <= 0:
        raise AssertionError(f"Smoke PDF missing or empty: {pdf_path}")


def assert_smoke_pdf_size_reasonable(path: str | Path, max_mb: float = 2.0) -> None:
    size = Path(path).stat().st_size / (1024 * 1024)
    if size > max_mb:
        raise AssertionError(f"Smoke PDF too large: {size:.2f} MB")
