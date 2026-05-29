from __future__ import annotations
from models.specs import RenderManifest


def assert_page_coverage(manifest: RenderManifest) -> None:
    if [page.page_number for page in manifest.pages] != list(range(1, manifest.total_pages + 1)):
        raise AssertionError("Page registry is not contiguous")


def assert_match_log_coverage(manifest: RenderManifest) -> None:
    pages = [page for page in manifest.pages if "match_log" in page.qa_tags]
    if len(pages) != 104:
        raise AssertionError(f"Expected 104 match logs, found {len(pages)}")


def assert_sticky_nav_links(manifest: RenderManifest) -> None:
    nav_links = [link for link in manifest.links if ".nav." in link.link_id]
    if len(nav_links) != manifest.total_pages * 9:
        raise AssertionError(f"Sticky nav link count mismatch: {len(nav_links)}")


def run_manifest_checks(manifest: RenderManifest) -> None:
    manifest.validate()
    assert_page_coverage(manifest)
    assert_match_log_coverage(manifest)
    assert_sticky_nav_links(manifest)
