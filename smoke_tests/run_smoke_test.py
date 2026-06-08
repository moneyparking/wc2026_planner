from __future__ import annotations
from pathlib import Path
from build_manifest import build_render_manifest
from models.enums import SKU
from qa.manifest_checks import run_manifest_checks
from qa.smoke_pdf_checks import assert_smoke_pdf_exists, assert_smoke_pdf_size_reasonable
from rendering.smoke_renderer import PlannerPDFSmokeRenderer


def run() -> None:
    manifest = build_render_manifest(SKU.PREMIUM)
    run_manifest_checks(manifest)
    output_path = Path("output/premium/smoke_phase_1_5.pdf")
    PlannerPDFSmokeRenderer().render_smoke_pdf(manifest, output_path, (1, 3, 10, 22, 25, 45, 59, 66))
    assert_smoke_pdf_exists(output_path)
    assert_smoke_pdf_size_reasonable(output_path)
    print(f"Phase 1.5 smoke test complete: {output_path}")


if __name__ == "__main__":
    run()
