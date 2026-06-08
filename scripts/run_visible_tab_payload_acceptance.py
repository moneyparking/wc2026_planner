from __future__ import annotations

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import app


FORBIDDEN_BRACKET_TERMS = (
    "depends_on",
    "Array(2)",
    "QF_M098",
    "SF_M101",
    "annex_c_loaded_but_mapping_pending",
)


def _row_count(html: str) -> int:
    return len(re.findall(r"<tr data-row=", html))


def _assert_contains(html: str, marker: str, label: str) -> None:
    assert marker in html, f"{label} missing marker: {marker}"


def _assert_not_contains(html: str, marker: str, label: str) -> None:
    assert marker not in html, f"{label} leaked forbidden marker: {marker}"


def main() -> None:
    loaded_state = app.initial_load()[0]
    demo_outputs = app.load_demo_scenario_outputs(loaded_state)
    recalculated_outputs = app.recalculate_outputs(demo_outputs[0])

    match_html = recalculated_outputs[2]
    group_html = recalculated_outputs[3]
    third_html = recalculated_outputs[4]
    bracket_html = recalculated_outputs[6]
    friends_html = recalculated_outputs[7]

    match_rows = _row_count(match_html)
    group_rows = _row_count(group_html)
    third_rows = _row_count(third_html)
    bracket_rows = _row_count(bracket_html)
    friends_rows = _row_count(friends_html)

    match_ids = len(re.findall(r"M\d{3}", match_html))

    _assert_contains(match_html, "Engine loaded:", "Match Planner")
    _assert_contains(match_html, "/ 104 matches", "Match Planner")
    _assert_contains(match_html, "Visible preview:", "Match Planner")
    _assert_not_contains(match_html, "104 / 104 matches loaded", "Match Planner")
    assert match_rows >= 10 or match_ids >= 10, "Match Planner needs at least 10 visible rows or 10 match IDs"

    _assert_contains(group_html, "Computed group rows:", "Group Tracker")
    _assert_contains(group_html, "Visible preview:", "Group Tracker")
    assert group_rows >= 8, "Group Tracker needs at least 8 visible rows"

    _assert_contains(third_html, "Computed third-place rows:", "3rd-Place Ranking")
    _assert_contains(third_html, "Visible preview:", "3rd-Place Ranking")
    assert third_rows >= 1, "3rd-Place Ranking needs at least 1 visible row"

    _assert_contains(friends_html, "Demo scoreboard rows:", "Friends League")
    _assert_contains(friends_html, "Visible preview:", "Friends League")
    assert friends_rows >= 5, "Friends League needs at least 5 visible player rows"

    _assert_contains(bracket_html, "Round of 32 Preview", "Bracket War Room")
    _assert_contains(bracket_html, "Visible preview:", "Bracket War Room")
    assert bracket_rows >= 8, "Bracket War Room needs at least 8 visible rows"

    for term in FORBIDDEN_BRACKET_TERMS:
        _assert_not_contains(bracket_html, term, "Bracket War Room")

    print("VISIBLE_TAB_PAYLOAD_ACCEPTANCE_PASS")
    print(f"match_rows={match_rows}")
    print(f"group_rows={group_rows}")
    print(f"third_rows={third_rows}")
    print(f"friends_rows={friends_rows}")
    print(f"bracket_rows={bracket_rows}")


if __name__ == "__main__":
    main()
