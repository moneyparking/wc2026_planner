from __future__ import annotations

import os
import re
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
    source_text = app_text + "\n" + css_text

    initial = "\n".join(
        [
            app._command_header_html(),
            app._appstore_first_screen_html(),
            app._visible_runtime_match_planner_html(pd.DataFrame(), "All 104 matches"),
            app._visible_group_tracker_html(pd.DataFrame()),
            app._visible_bracket_war_room_html({}, pd.DataFrame()),
            app._visible_friends_league_html(pd.DataFrame()),
            app.build_ai_scout_output(pd.DataFrame()),
            app.google_sheet_control_html(),
        ]
    )

    assert_contains(initial, "PHASE 1.32", "Phase 1.32 marker")
    assert_contains(initial, "ABW", "ABW logo")
    assert_contains(initial, "Today’s Match Center", "Today's Match Center")
    assert_contains(initial, "What Changed", "What Changed panel")
    assert_contains(initial, "Runtime Status Cards", "Runtime Status Cards")
    assert_contains(initial, "Quick Navigation Cards", "Quick Navigation Cards")
    assert_contains(initial, "Google Sheet Control Snapshot", "Google Sheet snapshot")
    assert_contains(initial, "M001 Mexico 2–1 South Africa · FT", "M001 runtime score")
    assert_contains(initial, "Mexico +3 pts", "Mexico points")
    assert_contains(initial, "AI Scout — Match Control Panel", "AI Scout panel")
    assert_contains(initial, "Actual Result", "Friends League actual result")
    assert_contains(initial, "Status", "Friends League status")

    for old_copy in (
        "AI Scout Tactical Slip",
        "local runtime engine",
        "autonomous local engine",
        "Runtime Match Planner · 104 rows",
    ):
        assert_absent(app_text, old_copy, "Old active/fallback app copy")
        assert_absent(initial, old_copy, "Old visible app copy")

    assert not re.search(r"M001[\s\S]{0,180}(Round of 32|Qualified Slot|R32\+)", initial), "M001 placeholder-first path visible"
    assert not re.search(r"M001[\s\S]{0,180}(Round of 32|Qualified Slot|R32\+)", app_text), "M001 placeholder-first path in active app code"

    for filler in ("empty-filler", "blank-fill", "giant-spacer", "blank-zone", "min-height: 600px"):
        assert_absent(source_text, filler, "Filler/spacer marker")

    for match in re.finditer(r"min-height:\s*(\d+)px", source_text):
        value = int(match.group(1))
        assert value <= 320, f"min-height above 320px found: {value}px"

    table_position = initial.lower().find("<table")
    first_screen_position = initial.find("Today’s Match Center")
    assert first_screen_position != -1 and (table_position == -1 or first_screen_position < table_position), "Initial render is not card-first"

    for required_css in ("#07111F", "#F8FAFC", "#FFFFFF", "#0F172A", "#64748B", "#CBD5E1", "#10B981", "#F59E0B", "#EF4444", "border-radius: 16px"):
        assert_contains(source_text, required_css, "Visual system CSS")

    assert_contains(walkthrough_text, "PHASE 1.32", "Walkthrough Phase 1.32 requirement")
    assert_contains(walkthrough_text, "JUDGE_UI_WALKTHROUGH_PHASE_1_32_PASS", "Walkthrough Phase 1.32 marker")

    lowered = initial.lower()
    for term in FORBIDDEN_TERMS:
        assert term not in lowered, f"Forbidden language visible: {term}"

    print("phase_132_marker=PASS")
    print("first_screen_card_first=PASS")
    print("runtime_status_cards=PASS")
    print("quick_navigation_cards=PASS")
    print("what_changed_panel=PASS")
    print("google_sheet_snapshot=PASS")
    print("old_copy_removed=PASS")
    print("no_placeholder_first_m001=PASS")
    print("no_large_empty_zones=PASS")
    print("forbidden_language=PASS")
    print("PHASE_1_32_VISUAL_COMPLETION_QA_PASS")


if __name__ == "__main__":
    main()
