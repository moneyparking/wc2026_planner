from __future__ import annotations
from pathlib import Path
from typing import Any
from pypdf import PdfReader


def read_pdf(path: str | Path) -> PdfReader:
    pdf_path = Path(path)
    if not pdf_path.exists() or pdf_path.stat().st_size <= 0:
        raise AssertionError(f"PDF missing or empty: {pdf_path}")
    return PdfReader(str(pdf_path))


def count_pdf_pages(path: str | Path) -> int:
    return read_pdf(path).get_num_pages()


def count_page_annotations(reader: PdfReader) -> list[int]:
    return [len(page.get("/Annots") or []) for page in reader.pages]


def count_total_annotations(path: str | Path) -> int:
    return sum(count_page_annotations(read_pdf(path)))


def assert_pdf_page_count(path: str | Path, expected_pages: int) -> None:
    actual = count_pdf_pages(path)
    if actual != expected_pages:
        raise AssertionError(f"PDF page count mismatch: expected={expected_pages}, actual={actual}")


def assert_pdf_has_annotations(path: str | Path, min_annotations: int) -> None:
    actual = count_total_annotations(path)
    if actual < min_annotations:
        raise AssertionError(f"Annotation count too low: expected_at_least={min_annotations}, actual={actual}")


def assert_no_zero_annotation_nav_pages(path: str | Path) -> None:
    counts = count_page_annotations(read_pdf(path))
    zero_pages = [index + 1 for index, count in enumerate(counts) if count == 0]
    if zero_pages:
        raise AssertionError(f"Pages with zero annotations: {zero_pages}")


def get_pdf_structure_summary(path: str | Path) -> dict[str, Any]:
    reader = read_pdf(path)
    counts = count_page_annotations(reader)
    pdf_path = Path(path)
    return {
        "path": str(pdf_path),
        "size_mb": round(pdf_path.stat().st_size / (1024 * 1024), 3),
        "pages": reader.get_num_pages(),
        "total_annotations": sum(counts),
        "min_annotations_on_page": min(counts) if counts else 0,
        "max_annotations_on_page": max(counts) if counts else 0,
        "zero_annotation_pages": [index + 1 for index, count in enumerate(counts) if count == 0],
    }
