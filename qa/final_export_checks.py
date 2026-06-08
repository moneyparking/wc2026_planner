from __future__ import annotations

from pathlib import Path
from typing import Any

from build_manifest import build_all_manifests
from models.enums import SKU
from qa.manifest_checks import assert_page_coverage, assert_sticky_nav_links
from qa.pdf_structure_checks import get_pdf_structure_summary
from qa.skeleton_report import write_skeleton_report


EXPECTED_PAGE_COUNTS = {
    SKU.PREMIUM: 184,
    SKU.STANDARD: 144,
    SKU.MINIMAL: 84,
}

EXPECTED_MATCH_LOG_COUNTS = {
    SKU.PREMIUM: 104,
    SKU.STANDARD: 104,
    SKU.MINIMAL: 52,
}


def run_manifest_export_checks() -> dict[str, Any]:
    manifests = build_all_manifests()
    report: dict[str, Any] = {"manifests": {}}

    for sku, manifest in manifests.items():
        if manifest.total_pages != EXPECTED_PAGE_COUNTS[sku]:
            raise AssertionError(f"{sku.value}: expected {EXPECTED_PAGE_COUNTS[sku]} pages, found {manifest.total_pages}")

        assert_page_coverage(manifest)
        assert_sticky_nav_links(manifest)

        match_pages = [page for page in manifest.pages if "match_log" in page.qa_tags]
        if len(match_pages) != EXPECTED_MATCH_LOG_COUNTS[sku]:
            raise AssertionError(f"{sku.value}: expected {EXPECTED_MATCH_LOG_COUNTS[sku]} match logs, found {len(match_pages)}")

        if len(manifest.links) < manifest.total_pages * 9:
            raise AssertionError(f"{sku.value}: missing sticky nav links")

        report["manifests"][sku.value] = {
            "pages": manifest.total_pages,
            "page_specs": len(manifest.pages),
            "links": len(manifest.links),
            "icons": len(manifest.icons),
            "match_logs": len(match_pages),
            "price_usd": manifest.price_usd,
        }

    return report


def validate_pdf_outputs(output_root: str | Path = "output") -> dict[str, Any]:
    output_path = Path(output_root)
    pdf_report: dict[str, Any] = {"pdfs": {}}

    for sku in ("premium", "standard", "minimal"):
        pdf_path = output_path / sku / f"{sku}_production_skeleton.pdf"
        if not pdf_path.exists():
            continue
        summary = get_pdf_structure_summary(pdf_path)
        if summary["pages"] != EXPECTED_PAGE_COUNTS[SKU(sku)]:
            raise AssertionError(f"{sku}: rendered PDF page count mismatch")
        if summary["zero_annotation_pages"]:
            raise AssertionError(f"{sku}: zero annotation pages found: {summary['zero_annotation_pages']}")
        pdf_report["pdfs"][sku] = summary

    return pdf_report


def run_final_export_checks() -> dict[str, Any]:
    report = run_manifest_export_checks()
    report.update(validate_pdf_outputs())
    write_skeleton_report(report, "output/final_export_report.json")
    return report


if __name__ == "__main__":
    result = run_final_export_checks()
    print("Final export checks complete.")
    for sku, data in result["manifests"].items():
        print(f"{sku}: pages={data['pages']} links={data['links']} match_logs={data['match_logs']}")
