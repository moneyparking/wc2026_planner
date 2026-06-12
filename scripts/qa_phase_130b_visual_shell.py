from __future__ import annotations

import os
from pathlib import Path
import sys

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ["LIVE_SCORE_PROVIDER"] = "local_json"
os.environ.setdefault("GOOGLE_SHEET_ENABLED", "false")


FORBIDDEN_TERMS = ("od" + "ds", "bet" + "ting", "wager", "sports" + "book", "parlay", "payout")


def _assert_contains(text: str, required: str, label: str) -> None:
    assert required in text, f"{label} missing required text: {required}"


def _assert_not_contains(text: str, forbidden: str, label: str) -> None:
    assert forbidden not in text, f"{label} contains forbidden text: {forbidden}"


def main() -> None:
    import app

    app_text = (REPO_ROOT / "app.py").read_text(encoding="utf-8")
    css_text = (REPO_ROOT / "layout" / "css_styles.py").read_text(encoding="utf-8")

    header = app._command_header_html()
    runtime_status = app._runtime_status_html({})
    planner_empty = app._visible_match_planner_html(pd.DataFrame(), "All 104 matches")
    groups_empty = app._visible_group_tracker_html(pd.DataFrame())
    thirds_empty = app._visible_third_place_html(pd.DataFrame())
    bracket_empty = app._visible_bracket_war_room_html({}, pd.DataFrame())
    friends_empty = app._visible_friends_league_html(pd.DataFrame())
    sheet_control = app.google_sheet_control_html()
    scout = app.build_ai_scout_output(pd.DataFrame())

    visible_html = "\n".join(
        [
            header,
            runtime_status,
            planner_empty,
            groups_empty,
            thirds_empty,
            bracket_empty,
            friends_empty,
            sheet_control,
            scout,
        ]
    )

    _assert_contains(header, "PHASE 1.30B Visual Surface + AppStore Shell", "App shell")
    _assert_contains(app_text, "PHASE_130B_MARKER", "App marker constant")
    _assert_contains(header, "ABW", "Logo text mark")
    _assert_contains(header, "AI Bracket War Room", "Logo subtitle")
    _assert_contains(header, "Runtime Status chip row", "Runtime chip row")

    for icon_label in ("🏟 Match Center", "📊 Groups", "🧩 Bracket", "🏆 Friends League", "🧠 AI Scout", "📄 Google Sheet"):
        _assert_contains(visible_html + app_text, icon_label, "Icon label")

    for stale_marker in ("PHASE_1_28", "PHASE 1.28", "Phase 1.28"):
        _assert_not_contains(header, stale_marker, "Active shell")
    _assert_not_contains(app_text, "gr.HTML(value=phase128_onboarding_html", "Active Gradio render path")

    for required_css in (
        "PHASE 1.30B Visual Surface + AppStore Shell",
        "#07111F",
        "#FFFFFF",
        "#F8FAFC",
        "#10B981",
        "#F59E0B",
        "#EF4444",
        "#0F172A",
        "#64748B",
        "#CBD5E1",
        ".abw-app-shell",
        ".table-card",
        ".runtime-skeleton",
    ):
        _assert_contains(css_text, required_css, "App shell CSS")

    for required_card in ("runtime-card", "phase130-runtime-status", "match-center-card", "groups-card", "bracket-card", "friends-league-card", "google-sheet-card"):
        _assert_contains(visible_html, required_card, "Runtime cards")

    _assert_contains(visible_html, "table-card", "Table-card wrapper")
    _assert_contains(app_text, 'elem_classes=["table-card"]', "Gradio dataframe card wrapper")
    _assert_contains(visible_html, "Loading runtime table…", "Skeleton copy")
    _assert_contains(visible_html, "Runtime data loaded from local_json/static seed", "Empty-state copy")
    _assert_contains(visible_html, "table-scroll", "Readable table surface")

    lowered_visible = visible_html.lower()
    for term in FORBIDDEN_TERMS:
        assert term not in lowered_visible, f"Forbidden language visible in app shell: {term}"

    print("visual_shell_marker=PASS")
    print("app_shell_css=PASS")
    print("runtime_cards=PASS")
    print("table_card_wrappers=PASS")
    print("skeleton_empty_state=PASS")
    print("forbidden_language=PASS")
    print("PHASE_1_30B_VISUAL_SHELL_QA_PASS")


if __name__ == "__main__":
    main()
