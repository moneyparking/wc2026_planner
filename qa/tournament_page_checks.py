from __future__ import annotations
from models.specs import RenderManifest
from registries.fixture_registry import validate_fixture_registry


def run_tournament_page_checks(manifest: RenderManifest) -> None:
    validate_fixture_registry()
    if len([page for page in manifest.pages if page.template_id == "group_tracker"]) != 12:
        raise AssertionError("Expected 12 group tracker pages")
    if len([page for page in manifest.pages if page.template_id == "match_index"]) != 3:
        raise AssertionError("Expected 3 match index pages")
    if len([link for link in manifest.links if link.link_id.startswith("match_index_")]) != 104:
        raise AssertionError("Expected 104 match index links")
