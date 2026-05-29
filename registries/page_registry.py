from __future__ import annotations
from models.enums import LinkType, Scope, SectionId, SKU
from models.specs import LinkSpec, PageSpec


def _link(link_id: str, label: str, source_page: int, target_page: int, hotspot_key: str) -> LinkSpec:
    return LinkSpec(link_id, label, LinkType.INTERNAL_PAGE, source_page, target_page, None, hotspot_key, True)


def build_premium_static_pages() -> list[PageSpec]:
    rows = [
        (1, "cover", "Matchday No Chaos", "World Cup 2026 Premium Fan Command Center", SectionId.ONBOARDING, "cover_hero", Scope.SHARED_ALL, "icons_trophy_generic_001.png"),
        (2, "bundle_map", "What’s Included", "Your complete GoodNotes, printable and sticker bundle", SectionId.ONBOARDING, "bundle_map", Scope.SHARED_ALL, "icons_bundle_001.png"),
        (3, "home_dashboard", "Home Dashboard", "Tournament control room for every matchday", SectionId.ONBOARDING, "dashboard", Scope.SHARED_ALL, "icons_section_home_001.png"),
        (4, "quick_start", "Quick Start", "Setup in 60 seconds", SectionId.ONBOARDING, "instruction_cards", Scope.SHARED_ALL, "icons_rocket_001.png"),
        (5, "link_mode_guide", "Link Mode Guide", "Tap links cleanly in GoodNotes and Notability", SectionId.ONBOARDING, "support_guide", Scope.SHARED_ALL, "icons_link_001.png"),
        (6, "sticker_workflow_preview", "Sticker Workflow Preview", "Use transparent PNG stickers while watching", SectionId.ONBOARDING, "sticker_preview", Scope.SHARED_ALL, "icons_sticker_001.png"),
        (7, "printable_compatibility_guide", "Printable Compatibility Guide", "Use flattened PDF for broad app and print support", SectionId.ONBOARDING, "print_guide", Scope.SHARED_ALL, "icons_print_001.png"),
        (8, "free_sticker_sample", "Free Sticker Sample", "Preview the full 500-file sticker pack", SectionId.ONBOARDING, "upsell_sample", Scope.SHARED_ALL, "icons_gift_001.png"),
        (9, "tournament_overview", "Tournament Overview", "48 teams, 12 groups, 104 matches", SectionId.TOURNAMENT_HUB, "tournament_overview", Scope.SHARED_ALL, "icons_globe_001.png"),
    ]
    pages: list[PageSpec] = []
    for page_number, page_id, title, subtitle, section, template, scope, icon in rows:
        links: tuple[LinkSpec, ...] = tuple()
        if page_number == 1:
            links = (_link("cover.tap_to_start", "Tap to Start", 1, 3, "cta.primary"),)
        elif page_number == 2:
            links = (
                _link("bundle.quick_start", "Quick Start", 2, 4, "bundle.card.quick_start"),
                _link("bundle.stickers", "Sticker Pack", 2, 59, "bundle.card.stickers"),
                _link("bundle.bingo", "Bingo Cards", 2, 50, "bundle.card.bingo"),
            )
        elif page_number == 3:
            links = (
                _link("dashboard.groups", "Groups", 3, 10, "dashboard.card.groups"),
                _link("dashboard.match_logs", "Match Logs", 3, 22, "dashboard.card.match_logs"),
                _link("dashboard.bracket", "Bracket", 3, 25, "dashboard.card.bracket"),
                _link("dashboard.party", "Party", 3, 45, "dashboard.card.party"),
            )
        pages.append(PageSpec(page_number, page_id, title, subtitle, section, template, scope, icon, links=links, qa_tags=("sticky_nav",)))
    return pages


def build_group_pages() -> list[PageSpec]:
    pages: list[PageSpec] = []
    for index, group in enumerate("ABCDEFGHIJKL"):
        page_number = 10 + index
        first_match = 1 + index * 6
        links = tuple(_link(f"group_{group.lower()}.match_{match_id:03d}", f"Match {match_id:03d}", page_number, 70 + match_id, f"group.fixture.{match_id:03d}") for match_id in range(first_match, first_match + 6))
        pages.append(PageSpec(page_number, f"group_{group.lower()}_tracker", f"Group {group} Tracker", "Live standings without chaos", SectionId.TOURNAMENT_HUB, "group_tracker", Scope.SHARED_ALL, "icons_table_001.png", ("icons_team_badge_generic_001.png",), links, f"groups.{group}", ("group_tracker", "sticky_nav", "dark_write_plate")))
    return pages


def build_match_index_pages() -> list[PageSpec]:
    pages: list[PageSpec] = []
    for page_number, first_match, last_match in ((22, 1, 36), (23, 37, 72), (24, 73, 104)):
        links = tuple(_link(f"match_index_{first_match:03d}_{last_match:03d}.match_{match_id:03d}", f"Match {match_id:03d}", page_number, 70 + match_id, f"match_index.row.{match_id:03d}") for match_id in range(first_match, last_match + 1))
        pages.append(PageSpec(page_number, f"match_index_{first_match:03d}_{last_match:03d}", f"Match Index {first_match:03d}–{last_match:03d}", "Tap any row to jump to its dedicated match log", SectionId.TOURNAMENT_HUB, "match_index", Scope.SHARED_ALL, "icons_list_001.png", ("icons_link_001.png",), links, f"match_index.{first_match:03d}_{last_match:03d}", ("match_index", "full_row_links", "sticky_nav")))
    return pages


def _page(page_number: int, page_id: str, title: str, section: SectionId, template: str, scope: Scope, icon: str, subtitle: str = "Premium planner template") -> PageSpec:
    return PageSpec(page_number, page_id, title, subtitle, section, template, scope, icon, qa_tags=("sticky_nav",))


def build_explicit_pages_25_70() -> list[PageSpec]:
    rows = [
        (25, "bracket_prediction", "Bracket Prediction", SectionId.TOURNAMENT_HUB, "bracket_prediction", Scope.SHARED_ALL, "icons_bracket_001.png"),
        (26, "live_knockout_tracker", "Live Knockout Tracker", SectionId.TOURNAMENT_HUB, "knockout_tracker", Scope.SHARED_ALL, "icons_knockout_001.png"),
        (27, "favorite_team_hub", "Favorite Team Hub", SectionId.TEAM_FAN_IDENTITY, "team_hub", Scope.SHARED_ALL, "icons_heart_team_001.png"),
        (28, "team_rating_sheet", "Team Rating Sheet", SectionId.TEAM_FAN_IDENTITY, "rating_sheet", Scope.SHARED_PREMIUM_STANDARD, "icons_ratings_001.png"),
        (29, "squad_cards_favorites", "Squad Cards — Favorites", SectionId.TEAM_FAN_IDENTITY, "sports_cards", Scope.SHARED_PREMIUM_STANDARD, "icons_card_001.png"),
        (30, "squad_cards_dark_horses", "Squad Cards — Dark Horses", SectionId.TEAM_FAN_IDENTITY, "sports_cards", Scope.PREMIUM_ONLY, "icons_dark_horse_001.png"),
        (31, "player_watchlist", "Player Watchlist", SectionId.TEAM_FAN_IDENTITY, "watchlist", Scope.PREMIUM_ONLY, "icons_player_001.png"),
        (32, "team_path_tracker", "Team Path Tracker", SectionId.TEAM_FAN_IDENTITY, "path_tracker", Scope.PREMIUM_ONLY, "icons_path_001.png"),
        (33, "rival_watch", "Rival Watch", SectionId.TEAM_FAN_IDENTITY, "rival_watch", Scope.PREMIUM_ONLY, "icons_rival_001.png"),
        (34, "dark_horse_board", "Dark Horse Board", SectionId.TEAM_FAN_IDENTITY, "dark_horse_board", Scope.PREMIUM_ONLY, "icons_upset_001.png"),
        (35, "stats_dashboard", "Stats Dashboard", SectionId.STATS_PREDICTIONS, "stats_dashboard", Scope.SHARED_ALL, "icons_stats_001.png"),
        (36, "golden_boot_tracker", "Golden Boot Tracker", SectionId.STATS_PREDICTIONS, "leaderboard_tracker", Scope.SHARED_PREMIUM_STANDARD, "icons_boot_001.png"),
        (37, "golden_glove_tracker", "Golden Glove Tracker", SectionId.STATS_PREDICTIONS, "leaderboard_tracker", Scope.SHARED_PREMIUM_STANDARD, "icons_glove_001.png"),
        (38, "prediction_slip_log", "Prediction Slip Log", SectionId.STATS_PREDICTIONS, "prediction_log", Scope.SHARED_ALL, "icons_prediction_001.png"),
        (39, "pick_accuracy_tracker", "Pick Accuracy Tracker", SectionId.STATS_PREDICTIONS, "accuracy_tracker", Scope.SHARED_PREMIUM_STANDARD, "icons_target_001.png"),
        (40, "upset_tracker", "Upset Tracker", SectionId.STATS_PREDICTIONS, "upset_tracker", Scope.PREMIUM_ONLY, "icons_upset_001.png"),
        (41, "var_ref_log", "VAR / Ref Moment Log", SectionId.STATS_PREDICTIONS, "moment_log", Scope.PREMIUM_ONLY, "icons_var_001.png"),
        (42, "best_goals_tracker", "Best Goals Tracker", SectionId.STATS_PREDICTIONS, "best_goals", Scope.PREMIUM_ONLY, "icons_goal_001.png"),
        (43, "mvp_race", "MVP Race", SectionId.STATS_PREDICTIONS, "mvp_race", Scope.PREMIUM_ONLY, "icons_mvp_001.png"),
        (44, "knockout_prediction_review", "Knockout Prediction Review", SectionId.STATS_PREDICTIONS, "prediction_review", Scope.PREMIUM_ONLY, "icons_review_001.png"),
    ]
    pages = [_page(*row) for row in rows]
    party_titles = {45: "Watch Party Planner", 46: "Matchday Checklist", 47: "Office Pool Setup", 48: "Office Pool Scoreboard", 49: "Group Chat Prompts", 50: "Bingo Rules"}
    for page_number in range(45, 59):
        is_bingo = page_number >= 51
        pages.append(_page(page_number, f"party_page_{page_number:03d}", f"Bingo Card {page_number - 50}" if is_bingo else party_titles[page_number], SectionId.WATCH_PARTY_OFFICE_POOL, "bingo_card" if is_bingo else "party_tool", Scope.PREMIUM_ONLY if page_number in {46, 47, 48, 49, 55, 56, 57, 58} else Scope.SHARED_PREMIUM_STANDARD, "icons_bingo_card_001.png" if is_bingo else "icons_party_001.png"))
    sticker_titles = {59: "Sticker Index", 60: "Jersey + Flag Catalog", 61: "Event Sticker Catalog", 62: "Tactics Sticker Catalog", 63: "Bingo Dot Sticker Sheet", 64: "Planner Icons Catalog", 65: "Sticker Placement Examples"}
    for page_number in range(59, 66):
        pages.append(_page(page_number, f"sticker_page_{page_number:03d}", sticker_titles[page_number], SectionId.STICKER_WORKFLOW, "usage_examples" if page_number == 65 else "sticker_catalog_grid", Scope.PREMIUM_ONLY if page_number in {62, 63, 64} else Scope.SHARED_PREMIUM_STANDARD, "icons_sticker_001.png"))
    note_titles = {66: "Replay Watchlist", 67: "Favorite Moments Log", 68: "Final Recap", 69: "Review / Support CTA", 70: "License + IP Disclaimer"}
    note_templates = {66: "watchlist", 67: "memory_log", 68: "final_recap", 69: "support_cta", 70: "legal_disclaimer"}
    for page_number in range(66, 71):
        pages.append(_page(page_number, f"notes_memory_{page_number:03d}", note_titles[page_number], SectionId.NOTES_MEMORY, note_templates[page_number], Scope.PREMIUM_ONLY if page_number in {66, 67, 69} else Scope.SHARED_ALL, "icons_notes_001.png"))
    return pages


def build_match_log_pages() -> list[PageSpec]:
    pages: list[PageSpec] = []
    for match_id in range(1, 105):
        page_number = 70 + match_id
        back_target = 22 if match_id <= 36 else 23 if match_id <= 72 else 24
        links = (_link(f"match_log_{match_id:03d}.back_to_index", "Back to Match Index", page_number, back_target, "match_log.back_to_index"),)
        pages.append(PageSpec(page_number, f"match_log_{match_id:03d}", f"Match {match_id:03d}", "Score, prediction, tactics, event timeline and recap", SectionId.MATCH_LOGS, "dedicated_match_log", Scope.SHARED_PREMIUM_STANDARD, "icons_match_001.png", ("icons_goal_001.png", "icons_var_001.png", "icons_card_001.png", "icons_save_001.png"), links, f"fixtures.match_{match_id:03d}", ("match_log", "dedicated_match_log", "sticky_nav", "dark_write_plate")))
    return pages


def build_dark_note_pages() -> list[PageSpec]:
    return [PageSpec(page_number, f"dark_notes_{page_number - 174:02d}", f"Dark Notes {page_number - 174}", "High-contrast writing page", SectionId.DARK_NOTES, "dark_notes", Scope.PREMIUM_ONLY, "icons_notes_001.png", ("icons_pen_001.png",), qa_tags=("dark_notes", "sticky_nav", "dark_write_plate")) for page_number in range(175, 185)]


def build_premium_page_registry() -> tuple[PageSpec, ...]:
    pages: list[PageSpec] = []
    pages.extend(build_premium_static_pages())
    pages.extend(build_group_pages())
    pages.extend(build_match_index_pages())
    pages.extend(build_explicit_pages_25_70())
    pages.extend(build_match_log_pages())
    pages.extend(build_dark_note_pages())
    return tuple(sorted(pages, key=lambda page: page.page_number))


def build_page_registry(sku: SKU) -> tuple[PageSpec, ...]:
    if sku != SKU.PREMIUM:
        raise NotImplementedError("Premium page registry is implemented first")
    return build_premium_page_registry()
