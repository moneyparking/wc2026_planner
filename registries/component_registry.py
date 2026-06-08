from __future__ import annotations

TEMPLATE_IDS: tuple[str, ...] = (
    "cover_hero", "bundle_map", "dashboard", "instruction_cards", "support_guide",
    "sticker_preview", "print_guide", "upsell_sample", "tournament_overview",
    "group_tracker", "match_index", "bracket_prediction", "knockout_tracker",
    "team_hub", "rating_sheet", "sports_cards", "watchlist", "path_tracker",
    "rival_watch", "dark_horse_board", "stats_dashboard", "leaderboard_tracker",
    "prediction_log", "accuracy_tracker", "upset_tracker", "moment_log",
    "best_goals", "mvp_race", "prediction_review", "party_tool", "bingo_card",
    "sticker_catalog_grid", "usage_examples", "memory_log", "final_recap",
    "support_cta", "legal_disclaimer", "dedicated_match_log", "dark_notes",
)

TEMPLATE_TO_RENDERER: dict[str, str] = {template_id: f"{template_id}Renderer" for template_id in TEMPLATE_IDS}

def get_renderer_name(template_id: str) -> str:
    if template_id not in TEMPLATE_TO_RENDERER:
        raise KeyError(f"Unknown template_id: {template_id}")
    return TEMPLATE_TO_RENDERER[template_id]

def validate_templates(template_ids: set[str]) -> None:
    missing = sorted(template_id for template_id in template_ids if template_id not in TEMPLATE_TO_RENDERER)
    if missing:
        raise ValueError(f"Missing renderer mappings for templates: {missing}")
