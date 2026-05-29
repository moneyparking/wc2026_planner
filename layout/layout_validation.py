from __future__ import annotations
from models.specs import LinkSpec, RenderManifest
from layout.constants import LETTER_LANDSCAPE
from layout.hotspot_resolver import HotspotResolver


def assert_rect_inside_page(rect) -> None:
    if rect.x < 0 or rect.y < 0 or rect.x + rect.width > LETTER_LANDSCAPE.width or rect.y + rect.height > LETTER_LANDSCAPE.height:
        raise AssertionError(f"Rect outside page: {rect}")


def assert_link_rect_valid(link: LinkSpec, resolver: HotspotResolver) -> None:
    rect = resolver.resolve(link)
    assert_rect_inside_page(rect)
    if link.required:
        rect.validate_min_touch_target(LETTER_LANDSCAPE.min_touch_target)


def validate_manifest_geometry(manifest: RenderManifest) -> None:
    resolver = HotspotResolver()
    for link in manifest.links:
        assert_link_rect_valid(link, resolver)
