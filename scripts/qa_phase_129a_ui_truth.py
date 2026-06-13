from __future__ import annotations

from pathlib import Path
from html import escape
import sys

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


FORBIDDEN_TERMS = ("od" + "ds", "bet" + "ting", "wager", "sports" + "book", "parlay", "payout")


def fail(message: str) -> None:
    raise AssertionError(message)


def assert_contains(text: str, required: str, label: str) -> None:
    if required not in text:
        fail(f"{label} missing required text: {required}")


def main() -> None:
    import app
    from src.wc2026_data_loader import load_fixtures, load_groups

    if app.DEPLOY_MARKER != "PHASE_1_29A_UI_TRUTH_FULL_INTERACTION_FIX":
        fail(f"Wrong deploy marker: {app.DEPLOY_MARKER}")
    if "PHASE_1_28" in app._command_header_html():
        fail("Command header still exposes a stale Phase 1.28 marker.")

    fixtures = load_fixtures().sort_values("match_no")
    first_fixture = fixtures.iloc[0]
    if int(first_fixture["match_no"]) != 1:
        fail("Fixture CSV does not start at match 1.")
    if str(first_fixture["stage"]) != "Group Stage":
        fail("Match 1 must be a group-stage fixture.")

    seed_matches = app.phase_126_build_seed_matches()
    first_seed = seed_matches.iloc[0]
    if str(first_seed["Stage"]) != "Group Stage":
        fail("Live demo Match 1 must render as Group Stage.")
    if "Qualified Slot" in " ".join(first_seed.astype(str).tolist()) or "R32+" in " ".join(first_seed.astype(str).tolist()):
        fail("Live demo Match 1 leaked a knockout placeholder.")
    if str(first_seed["Team_A"]) != str(first_fixture["home"]) or str(first_seed["Team_B"]) != str(first_fixture["away"]):
        fail("Live demo Match 1 does not match the real fixture CSV.")

    group_html = app._visible_group_tracker_html(pd.DataFrame())
    groups = load_groups()
    for _, row in groups.iterrows():
        assert_contains(group_html, str(row["group"]), "Group tracker")
        display_team = app._display_team(row["team"]) if hasattr(app, "_display_team") else str(row["team"])
        assert_contains(group_html, escape(display_team), "Group tracker")
    assert_contains(group_html, "<thead>", "Group tracker table")
    assert_contains(group_html, "Visible preview: 48 / 48 team rows", "Group tracker")

    planner_html = app._visible_match_planner_html(pd.DataFrame(), "All 104 matches")
    for required in ("M001", "Group Stage", "Mexico", "South Africa"):
        assert_contains(planner_html, required, "Match planner")
    first_match_position = planner_html.find("M001")
    first_knockout_position = planner_html.find("Round of 32")
    if first_knockout_position != -1 and first_knockout_position < first_match_position:
        fail("Match planner shows a knockout row before Match 1.")

    state, matches, *_ = app.initial_load()
    load_payload = app.load_demo_ui_outputs(state, matches)
    recalc_payload = app.recalculate_ui_outputs(load_payload[0], load_payload[1])
    random_payload = app.random_outcomes_ui_outputs(recalc_payload[0], recalc_payload[1])
    for label, payload in (
        ("Load Judge Demo Scenario", load_payload),
        ("Recalculate War Room", recalc_payload),
        ("Generate Random Outcomes for all 104 matches", random_payload),
    ):
        status_html = payload[12]
        assert_contains(status_html, "Action Status", label)
        if label == "Recalculate War Room":
            assert "Recalculate War Room" in status_html or "Recalculate Impact / War Room" in status_html, label
        else:
            assert_contains(status_html, label, label)
        assert_contains(status_html, "Completed matches", label)
        assert_contains(payload[2], "<table>", f"{label} match planner preview")
        assert_contains(payload[4], "<table>", f"{label} group tracker preview")
        assert_contains(payload[6], "<table>", f"{label} third-place preview")
        assert_contains(payload[10], "<table>", f"{label} friends preview")

    scout = app.build_ai_scout_output(load_payload[1])
    for required in (
        "Rule-based squad-aware scout signal",
        "players loaded",
        "position distribution",
        "player sample",
        "Rule engine",
        "GK:",
        "DF:",
        "MF:",
        "FW:",
    ):
        assert_contains(scout, required, "AI Scout")

    visible_text = "\n".join(
        [
            app._command_header_html(),
            group_html,
            planner_html,
            scout,
            load_payload[12],
            recalc_payload[12],
            random_payload[12],
        ]
    ).lower()
    for term in FORBIDDEN_TERMS:
        if term in visible_text:
            fail(f"Forbidden term visible in Phase 1.29A UI output: {term}")

    print("PHASE_1_29A_UI_TRUTH_QA_PASS")
    print(f"deploy_marker={app.DEPLOY_MARKER}")
    print("first_fixture=M001 Mexico vs South Africa")
    print(f"group_rows={len(groups)}")
    print("primary_button_statuses=PASS")
    print("ai_scout_squad_aware=PASS")


if __name__ == "__main__":
    main()
