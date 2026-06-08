from __future__ import annotations

from models.specs import RenderManifest


EXPECTED_CORE_PAGE_IDS = {
    "cover",
    "bundle_map",
    "home_dashboard",
    "quick_start",
    "link_mode_guide",
    "sticker_workflow_preview",
    "printable_compatibility_guide",
    "free_sticker_sample",
    "tournament_overview",
}

EXPECTED_CORE_TEMPLATES = {
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


def run_core_page_checks(manifest: RenderManifest) -> None:
    actual_ids = {page.page_id for page in manifest.pages if 1 <= page.page_number <= 9}
    if actual_ids != EXPECTED_CORE_PAGE_IDS:
        raise AssertionError(f"Core page ID mismatch: expected={EXPECTED_CORE_PAGE_IDS}, actual={actual_ids}")

    for page_number, expected_template in EXPECTED_CORE_TEMPLATES.items():
        actual_template = manifest.pages[page_number - 1].template_id
        if actual_template != expected_template:
            raise AssertionError(
                f"Core page template mismatch: page={page_number}, expected={expected_template}, actual={actual_template}"
            )

    core_links = [link for link in manifest.links if 1 <= link.source_page <= 9]
    if len(core_links) < 89:
        raise AssertionError(f"Core pages should include sticky nav + declared links. Found links={len(core_links)}")
