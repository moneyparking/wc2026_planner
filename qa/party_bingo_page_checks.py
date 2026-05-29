from __future__ import annotations

from models.specs import RenderManifest


EXPECTED_PARTY_TEMPLATES = {
    45: "party_tool",
    46: "party_tool",
    47: "party_tool",
    48: "party_tool",
    49: "party_tool",
    50: "party_tool",
    51: "bingo_card",
    52: "bingo_card",
    53: "bingo_card",
    54: "bingo_card",
    55: "bingo_card",
    56: "bingo_card",
    57: "bingo_card",
    58: "bingo_card",
}


def run_party_bingo_page_checks(manifest: RenderManifest) -> None:
    if manifest.sku != "premium":
        return

    party_pages = [page for page in manifest.pages if 45 <= page.page_number <= 58]
    if len(party_pages) != 14:
        raise AssertionError(f"Expected 14 party/bingo pages, found {len(party_pages)}")

    bingo_pages = [page for page in manifest.pages if page.template_id == "bingo_card" and 51 <= page.page_number <= 58]
    if len(bingo_pages) != 8:
        raise AssertionError(f"Expected 8 bingo cards, found {len(bingo_pages)}")

    for page_number, expected_template in EXPECTED_PARTY_TEMPLATES.items():
        actual_template = manifest.pages[page_number - 1].template_id
        if actual_template != expected_template:
            raise AssertionError(
                f"Party/bingo template mismatch: page={page_number}, expected={expected_template}, actual={actual_template}"
            )

    premium_only_bingo = [
        page for page in bingo_pages
        if page.page_number in {55, 56, 57, 58} and page.scope.value == "premium_only"
    ]
    if len(premium_only_bingo) != 4:
        raise AssertionError(f"Expected bingo cards 5–8 to be premium-only, found {len(premium_only_bingo)}")
