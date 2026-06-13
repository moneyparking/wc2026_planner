from __future__ import annotations

import json
import os
from html import unescape
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ["LIVE_SCORE_PROVIDER"] = "verified_cache"
os.environ.setdefault("GOOGLE_SHEET_ENABLED", "false")

FORBIDDEN_TERMS = ("od" + "ds", "bet" + "ting", "wager", "sports" + "book", "parlay", "payout")
EXPECTED_TABS = (
    "🏟 Match Center",
    "📊 Groups",
    "📊 3RD-PLACE RANKING",
    "🧩 Bracket",
    "🏆 Friends League",
    "🧠 AI Scout",
    "📄 Google Sheet",
    "Judge QA / Debug",
)
EXPECTED_BUTTONS = (
    "Refresh Runtime",
    "Recalculate Impact / War Room",
    "Open Friends League",
    "Ask AI Scout",
    "Pull Google Sheet",
    "View full 104-match table",
    "View full standings",
    "View bracket",
    "Score Friends League",
    "Select / inspect match",
    "Load Demo Scenario",
    "Generate Random Outcomes",
    "Clear Local Edits",
)


def main() -> None:
    import app

    app_text = (REPO_ROOT / "app.py").read_text(encoding="utf-8")
    css_text = (REPO_ROOT / "layout" / "css_styles.py").read_text(encoding="utf-8")
    state = app.initial_load()[0]
    active = unescape(
        "\n".join(
            [
                app._command_header_html(),
                app._appstore_first_screen_html(state),
                app._visible_runtime_match_planner_html(state["runtime_matches"]),
                app._selected_match_detail_html(state, "M001 Mexico 2–0 South Africa · FT"),
                app._visible_group_tracker_html(app.initial_load()[2]),
                app._visible_third_place_html(app.initial_load()[3]),
                app._visible_bracket_war_room_html(app.initial_load()[4], app.initial_load()[2]),
                app._visible_friends_league_html(app.initial_load()[6], state["runtime_matches"]),
                app.build_ai_scout_output(app.initial_load()[1], state["runtime_matches"], app.initial_load()[6]),
                app.google_sheet_control_html(state),
            ]
        )
    )

    assert "PHASE 1.34 — Fully Clickable Fan App" in active, "Phase 1.34 marker missing"
    for tab in EXPECTED_TABS:
        assert tab in app_text, f"Expected tab missing: {tab}"
    for button in EXPECTED_BUTTONS:
        assert button in app_text, f"Expected button missing: {button}"

    for callback_name in (
        "refresh_live_button.click",
        "recalc_button.click",
        "open_friends_button.click",
        "ask_ai_scout_button.click",
        "pull_sheet_button.click",
        "view_full_table_button.click",
        "view_full_standings_button.click",
        "view_bracket_button.click",
        "score_friends_button.click",
        "inspect_match_button.click",
        "load_demo_button.click",
        "random_outcomes_button.click",
        "clear_edits_button.click",
    ):
        assert callback_name in app_text, f"Button callback missing: {callback_name}"

    for forbidden in (
        "MATCH_PLANNER — editable full 104-match scenario input",
        "M001 Mexico 2-1 South Africa",
        "M001 Mexico 2–1 South Africa",
        "0 completed match(es)",
    ):
        assert forbidden not in active, f"Old active UI string visible: {forbidden}"

    for required in (
        "M001 Mexico 2–0 South Africa",
        "M002 Korea Republic 2–1 Czechia",
        "M003 Canada 1–1 Bosnia & Herzegovina",
        "M004 United States 4–1 Paraguay",
        "Completed matches",
        "4",
        "Google Sheet: OFF — ready to connect",
        "Google Sheet is not connected. Add GOOGLE_SHEET_ENABLED=true, GOOGLE_SHEET_ID, and GOOGLE_SERVICE_ACCOUNT_JSON to enable.",
        "Result Source Truth",
        "Third-place ranking is not active yet.",
        "Round of 32",
        "Final",
        "Scored rows count",
        "AI Scout — Match Control Panel",
    ):
        assert required in active, f"Active UI missing: {required}"

    verified = json.loads((REPO_ROOT / "data" / "worldcup_results_verified.json").read_text(encoding="utf-8"))
    expected_scores = {1: (2, 0), 2: (2, 1), 3: (1, 1), 4: (4, 1)}
    for row in verified:
        match_no = int(row["match_no"])
        if match_no in expected_scores:
            assert (int(row["home_score"]), int(row["away_score"])) == expected_scores[match_no]

    for css_required in ("#07111F", "#F8FAFC", "#FFFFFF", "#CBD5E1", "#10B981", "border-radius: 16px", ".app-card", ".card-shell"):
        assert css_required in css_text, f"CSS requirement missing: {css_required}"

    lowered = active.lower()
    for term in FORBIDDEN_TERMS:
        assert term not in lowered, f"Forbidden language visible: {term}"

    print("phase_134_marker=PASS")
    print("tabs=PASS")
    print("buttons_bound=PASS")
    print("verified_results=PASS")
    print("active_ui_copy=PASS")
    print("visual_shell=PASS")
    print("forbidden_language=PASS")
    print("PHASE_1_34_FULL_APP_STATIC_QA_PASS")


if __name__ == "__main__":
    main()
