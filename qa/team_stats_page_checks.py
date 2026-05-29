from __future__ import annotations
from models.specs import RenderManifest


def run_team_stats_page_checks(manifest: RenderManifest) -> None:
    if len([page for page in manifest.pages if 27 <= page.page_number <= 34]) != 8:
        raise AssertionError("Expected 8 team pages")
    if len([page for page in manifest.pages if 35 <= page.page_number <= 44]) != 10:
        raise AssertionError("Expected 10 stats pages")
