from __future__ import annotations
from pathlib import Path
from build_manifest import build_render_manifest
from models.enums import SKU
from qa.core_page_checks import run_core_page_checks
from qa.manifest_checks import run_manifest_checks
from qa.match_log_template_checks import run_match_log_template_checks
from qa.party_bingo_page_checks import run_party_bingo_page_checks
from qa.pdf_structure_checks import assert_no_zero_annotation_nav_pages, assert_pdf_has_annotations, assert_pdf_page_count, get_pdf_structure_summary
from qa.skeleton_report import write_skeleton_report
from qa.sticker_notes_page_checks import run_sticker_notes_page_checks
from qa.team_stats_page_checks import run_team_stats_page_checks
from qa.tournament_page_checks import run_tournament_page_checks
from rendering.full_skeleton_renderer import FullSkeletonPDFRenderer


def run() -> None:
    manifest = build_render_manifest(SKU.PREMIUM)
    run_manifest_checks(manifest)
    run_core_page_checks(manifest)
    run_tournament_page_checks(manifest)
    run_match_log_template_checks(manifest)
    run_team_stats_page_checks(manifest)
    run_party_bingo_page_checks(manifest)
    run_sticker_notes_page_checks(manifest)
    output_pdf = Path("output/premium/phase_1_6_premium_skeleton_184_pages.pdf")
    output_report = Path("output/premium/phase_1_6_skeleton_report.json")
    FullSkeletonPDFRenderer().render_skeleton_pdf(manifest, output_pdf)
    assert_pdf_page_count(output_pdf, 184)
    assert_pdf_has_annotations(output_pdf, 1936)
    assert_no_zero_annotation_nav_pages(output_pdf)
    report = get_pdf_structure_summary(output_pdf)
    report["manifest"] = {
        "sku": manifest.sku,
        "display_name": manifest.display_name,
        "expected_pages": manifest.total_pages,
        "manifest_links": len(manifest.links),
        "manifest_icons": len(manifest.icons),
    }
    write_skeleton_report(report, output_report)
    print("Phase 1.6 skeleton render complete.")
    print(f"PDF: {output_pdf}")
    print(f"Report: {output_report}")
    print(f"Pages: {report['pages']}")
    print(f"Total annotations: {report['total_annotations']}")


if __name__ == "__main__":
    run()
