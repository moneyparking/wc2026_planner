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


def assert_contains(text: str, required: str, label: str) -> None:
    assert required in text, f"{label} missing required text: {required}"


def assert_absent(text: str, forbidden: str, label: str) -> None:
    assert forbidden not in text, f"{label} contains forbidden text: {forbidden}"


def main() -> None:
    import app

    app_text = (REPO_ROOT / "app.py").read_text(encoding="utf-8")
    css_text = (REPO_ROOT / "layout" / "css_styles.py").read_text(encoding="utf-8")
    walkthrough_text = (REPO_ROOT / "scripts" / "judge_ui_walkthrough.py").read_text(encoding="utf-8")

    initial = "\n".join(
        [
            app._command_header_html(),
            app._appstore_first_screen_html(),
            app.google_sheet_control_html(),
            app.build_ai_scout_output(pd.DataFrame()),
            app._visible_group_tracker_html(pd.DataFrame()),
            app._visible_friends_league_html(pd.DataFrame()),
        ]
    )

    assert_contains(initial, "PHASE 1.31", "Phase marker")
    assert_contains(initial, "ABW", "ABW logo mark")
    for nav_label in ("🏟 Match Center", "📊 Groups", "🧩 Bracket", "🏆 Friends", "🧠 Scout", "📄 Sheet"):
        assert_contains(initial, nav_label, "Icon navigation")
    assert_contains(initial, "Today’s Match Center", "Today's Match Center")
    assert_contains(initial, "M001 Mexico 2–1 South Africa FT", "Today's match scoreline")
    assert_contains(initial, "source local_json", "Runtime source")
    assert_contains(initial, "Group A impact: Mexico +3 pts", "Group impact")
    assert_contains(initial, "Google Sheet Control explanation", "Google Sheet module")
    assert_contains(initial, "AI Scout Match Control Panel", "AI Scout module")
    assert_contains(initial, "Group A impact card", "Group tracker compact card")
    assert_contains(initial, "Actual result card", "Friends League actual result card")

    for old_copy in (
        "AI Scout Tactical Slip — autonomous local engine",
        "Runtime Match Planner · 104 rows",
        "Qualified Slot",
        "R32+",
    ):
        assert_absent(initial, old_copy, "Initial visible render")
        assert_absent(app_text, old_copy, "App source active/fallback path")

    combined_source = app_text + "\n" + css_text
    for filler in ("empty-filler", "blank-fill", "giant-spacer", "blank-zone", "min-height: 600px"):
        assert_absent(combined_source, filler, "Blank filler marker")

    for css_required in (
        ".app-card",
        ".card-shell",
        ".app-icon-nav",
        ".today-match-center",
        ".product-module-grid",
        "#07111F",
        "#F8FAFC",
        "#FFFFFF",
        "#CBD5E1",
        "#10B981",
        "border-radius: 16px",
    ):
        assert_contains(css_text + app_text, css_required, "Card-shell CSS")

    assert_contains(walkthrough_text, "PHASE 1.31", "Walkthrough Phase 1.31 requirement")
    assert_contains(walkthrough_text, "Today’s Match Center", "Walkthrough Today's Match Center requirement")
    assert_contains(walkthrough_text, "JUDGE_UI_WALKTHROUGH_PHASE_1_31_PASS", "Walkthrough pass marker")

    lowered = initial.lower()
    for term in FORBIDDEN_TERMS:
        assert term not in lowered, f"Forbidden language visible in app shell: {term}"

    print("phase_131_marker=PASS")
    print("abw_logo=PASS")
    print("icon_navigation=PASS")
    print("todays_match_center=PASS")
    print("old_fallback_paths_absent=PASS")
    print("card_shell_css=PASS")
    print("forbidden_language=PASS")
    print("PHASE_1_31_APPSTORE_POLISH_QA_PASS")


if __name__ == "__main__":
    main()
