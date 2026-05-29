from __future__ import annotations
from models.specs import RenderManifest


def run_party_bingo_page_checks(manifest: RenderManifest) -> None:
    if len([page for page in manifest.pages if 45 <= page.page_number <= 58]) != 14:
        raise AssertionError("Expected 14 party/bingo pages")
    if len([page for page in manifest.pages if page.template_id == "bingo_card" and 51 <= page.page_number <= 58]) != 8:
        raise AssertionError("Expected 8 bingo cards")
