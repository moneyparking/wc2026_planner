from __future__ import annotations

from pathlib import Path

from build_manifest import build_all_manifests
from models.enums import SKU
from qa.final_export_checks import run_final_export_checks
from rendering.full_skeleton_renderer import FullSkeletonPDFRenderer


OUTPUT_FILENAMES = {
    SKU.PREMIUM: "premium_production_skeleton.pdf",
    SKU.STANDARD: "standard_production_skeleton.pdf",
    SKU.MINIMAL: "minimal_production_skeleton.pdf",
}


def render_all_skus() -> None:
    manifests = build_all_manifests()
    renderer = FullSkeletonPDFRenderer()

    for sku, manifest in manifests.items():
        output_dir = Path("output") / sku.value
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAMES[sku]
        renderer.render_skeleton_pdf(manifest, output_path)
        print(f"Rendered {sku.value}: {output_path}")


def run() -> None:
    render_all_skus()
    report = run_final_export_checks()
    print("Production export complete.")
    for sku, data in report["manifests"].items():
        print(f"{sku}: pages={data['pages']} links={data['links']} icons={data['icons']} match_logs={data['match_logs']}")


if __name__ == "__main__":
    run()
