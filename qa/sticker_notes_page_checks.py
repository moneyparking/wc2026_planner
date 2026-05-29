from __future__ import annotations
from models.specs import RenderManifest


def run_sticker_notes_page_checks(manifest: RenderManifest) -> None:
    if len([page for page in manifest.pages if 59 <= page.page_number <= 65]) != 7:
        raise AssertionError("Expected 7 sticker pages")
    if len([page for page in manifest.pages if 66 <= page.page_number <= 70]) != 5:
        raise AssertionError("Expected 5 notes/legal pages")
    if len([page for page in manifest.pages if 175 <= page.page_number <= 184]) != 10:
        raise AssertionError("Expected 10 dark notes pages")
