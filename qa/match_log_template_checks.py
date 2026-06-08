from __future__ import annotations

from models.specs import RenderManifest


def run_match_log_template_checks(manifest: RenderManifest) -> None:
    pages = [page for page in manifest.pages if page.template_id == "dedicated_match_log"]
    expected_count = 52 if manifest.sku == "minimal" else 104
    if len(pages) != expected_count:
        raise AssertionError(f"Expected {expected_count} match log pages, found {len(pages)}")

    if manifest.sku == "premium":
        page_numbers = [page.page_number for page in pages]
        if page_numbers != list(range(71, 175)):
            raise AssertionError(f"Match log page coverage mismatch: {page_numbers[:3]}...{page_numbers[-3:]}")

        page_ids = [page.page_id for page in pages]
        expected_ids = [f"match_log_{match_id:03d}" for match_id in range(1, 105)]
        if page_ids != expected_ids:
            raise AssertionError("Match log IDs are not contiguous from match_log_001 to match_log_104")

        data_refs = [page.data_ref for page in pages]
        expected_refs = [f"fixtures.match_{match_id:03d}" for match_id in range(1, 105)]
        if data_refs != expected_refs:
            raise AssertionError("Match log data_ref mapping is not contiguous")

        back_links = [
            link
            for link in manifest.links
            if link.link_id.startswith("match_log_") and link.link_id.endswith(".back_to_index")
        ]
        if len(back_links) != 104:
            raise AssertionError(f"Expected 104 match-log back links, found {len(back_links)}")

        for link in back_links:
            match_id = int(link.link_id.split("_")[2].split(".")[0])
            expected_target = 22 if match_id <= 36 else 23 if match_id <= 72 else 24
            if link.target_page != expected_target:
                raise AssertionError(
                    f"Match log back link target mismatch: match={match_id:03d}, expected={expected_target}, actual={link.target_page}"
                )
