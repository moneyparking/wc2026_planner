from __future__ import annotations

from models.specs import RenderManifest


EXPECTED_TEAM_TEMPLATES = {
    27: "team_hub",
    28: "rating_sheet",
    29: "sports_cards",
    30: "sports_cards",
    31: "watchlist",
    32: "path_tracker",
    33: "rival_watch",
    34: "dark_horse_board",
}

EXPECTED_STATS_TEMPLATES = {
    35: "stats_dashboard",
    36: "leaderboard_tracker",
    37: "leaderboard_tracker",
    38: "prediction_log",
    39: "accuracy_tracker",
    40: "upset_tracker",
    41: "moment_log",
    42: "best_goals",
    43: "mvp_race",
    44: "prediction_review",
}


def run_team_stats_page_checks(manifest: RenderManifest) -> None:
    if manifest.sku != "premium":
        return

    team_pages = [page for page in manifest.pages if 27 <= page.page_number <= 34]
    stats_pages = [page for page in manifest.pages if 35 <= page.page_number <= 44]

    if len(team_pages) != 8:
        raise AssertionError(f"Expected 8 team pages, found {len(team_pages)}")

    if len(stats_pages) != 10:
        raise AssertionError(f"Expected 10 stats pages, found {len(stats_pages)}")

    for page_number, expected_template in EXPECTED_TEAM_TEMPLATES.items():
        actual_template = manifest.pages[page_number - 1].template_id
        if actual_template != expected_template:
            raise AssertionError(
                f"Team page template mismatch: page={page_number}, expected={expected_template}, actual={actual_template}"
            )

    for page_number, expected_template in EXPECTED_STATS_TEMPLATES.items():
        actual_template = manifest.pages[page_number - 1].template_id
        if actual_template != expected_template:
            raise AssertionError(
                f"Stats page template mismatch: page={page_number}, expected={expected_template}, actual={actual_template}"
            )
