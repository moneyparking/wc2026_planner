from __future__ import annotations

from models.specs import RenderManifest
from registries.fixture_registry import validate_fixture_registry


EXPECTED_GROUP_PAGE_NUMBERS = set(range(10, 22))
EXPECTED_MATCH_INDEX_PAGES = {22, 23, 24}
EXPECTED_TOURNAMENT_TEMPLATES = {
    10: "group_tracker",
    11: "group_tracker",
    12: "group_tracker",
    13: "group_tracker",
    14: "group_tracker",
    15: "group_tracker",
    16: "group_tracker",
    17: "group_tracker",
    18: "group_tracker",
    19: "group_tracker",
    20: "group_tracker",
    21: "group_tracker",
    22: "match_index",
    23: "match_index",
    24: "match_index",
    25: "bracket_prediction",
    26: "knockout_tracker",
}


def run_tournament_page_checks(manifest: RenderManifest) -> None:
    validate_fixture_registry()

    group_pages = [page for page in manifest.pages if page.template_id == "group_tracker"]
    if len(group_pages) < 12:
        raise AssertionError(f"Expected at least 12 group tracker pages, found {len(group_pages)}")

    premium_group_numbers = {
        page.page_number
        for page in manifest.pages
        if page.template_id == "group_tracker" and 10 <= page.page_number <= 21
    }
    if manifest.sku == "premium" and premium_group_numbers != EXPECTED_GROUP_PAGE_NUMBERS:
        raise AssertionError(f"Group page number mismatch: expected={EXPECTED_GROUP_PAGE_NUMBERS}, actual={premium_group_numbers}")

    match_index_pages = [page for page in manifest.pages if page.template_id == "match_index"]
    if len(match_index_pages) < 2:
        raise AssertionError(f"Expected match index pages, found {len(match_index_pages)}")

    if manifest.sku == "premium":
        match_index_numbers = {page.page_number for page in match_index_pages}
        if match_index_numbers != EXPECTED_MATCH_INDEX_PAGES:
            raise AssertionError(f"Match index page mismatch: expected={EXPECTED_MATCH_INDEX_PAGES}, actual={match_index_numbers}")

        index_links = [link for link in manifest.links if link.link_id.startswith("match_index_")]
        if len(index_links) != 104:
            raise AssertionError(f"Expected 104 match index links, found {len(index_links)}")

        group_fixture_links = [link for link in manifest.links if ".match_" in link.link_id and link.link_id.startswith("group_")]
        if len(group_fixture_links) != 72:
            raise AssertionError(f"Expected 72 group fixture links, found {len(group_fixture_links)}")

        for page_number, expected_template in EXPECTED_TOURNAMENT_TEMPLATES.items():
            actual = manifest.pages[page_number - 1].template_id
            if actual != expected_template:
                raise AssertionError(
                    f"Tournament template mismatch: page={page_number}, expected={expected_template}, actual={actual}"
                )
