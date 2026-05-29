from __future__ import annotations
from models.specs import RenderManifest


def run_match_log_template_checks(manifest: RenderManifest) -> None:
    pages = [page for page in manifest.pages if page.template_id == "dedicated_match_log"]
    if len(pages) != 104:
        raise AssertionError("Expected 104 match log pages")
    back_links = [link for link in manifest.links if link.link_id.startswith("match_log_") and link.link_id.endswith(".back_to_index")]
    if len(back_links) != 104:
        raise AssertionError("Expected 104 match-log back links")
