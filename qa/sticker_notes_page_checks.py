from __future__ import annotations
from models.specs import RenderManifest

EXPECTED_STICKER_TEMPLATES = {
    59: "sticker_catalog_grid",
    60: "sticker_catalog_grid",
    61: "sticker_catalog_grid",
    62: "sticker_catalog_grid",
    63: "sticker_catalog_grid",
    64: "sticker_catalog_grid",
    65: "usage_examples",
}

EXPECTED_NOTES_TEMPLATES = {
    66: "watchlist",
    67: "memory_log",
    68: "final_recap",
    69: "support_cta",
    70: "legal_disclaimer",
}


def run_sticker_notes_page_checks(manifest: RenderManifest) -> None:
    sticker_pages = [page for page in manifest.pages if 59 <= page.page_number <= 65]
    notes_pages = [page for page in manifest.pages if 66 <= page.page_number <= 70]
    dark_notes_pages = [page for page in manifest.pages if 175 <= page.page_number <= 184]
    if len(sticker_pages) != 7:
        raise AssertionError("Expected 7 sticker pages")
    if len(notes_pages) != 5:
        raise AssertionError("Expected 5 notes/legal pages")
    if len(dark_notes_pages) != 10:
        raise AssertionError("Expected 10 dark notes pages")
    for page_number, template_id in EXPECTED_STICKER_TEMPLATES.items():
        actual = manifest.pages[page_number - 1].template_id
        if actual != template_id:
            raise AssertionError(f"Sticker page {page_number} template mismatch: expected={template_id}, actual={actual}")
    for page_number, template_id in EXPECTED_NOTES_TEMPLATES.items():
        actual = manifest.pages[page_number - 1].template_id
        if actual != template_id:
            raise AssertionError(f"Notes page {page_number} template mismatch: expected={template_id}, actual={actual}")
    for page in dark_notes_pages:
        if page.template_id != "dark_notes":
            raise AssertionError(f"Dark notes page template mismatch: page={page.page_number}, template={page.template_id}")
