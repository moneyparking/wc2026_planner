from __future__ import annotations
from models.specs import RenderManifest


def run_core_page_checks(manifest: RenderManifest) -> None:
    expected = {
        1: "cover_hero",
        2: "bundle_map",
        3: "dashboard",
        4: "instruction_cards",
        5: "support_guide",
        6: "sticker_preview",
        7: "print_guide",
        8: "upsell_sample",
        9: "tournament_overview",
    }
    for page_number, template_id in expected.items():
        if manifest.pages[page_number - 1].template_id != template_id:
            raise AssertionError(f"Core template mismatch on page {page_number}")
