from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from models.bracket_mapper import build_bracket_mapping
from models.data_loader import load_workbook_state
from models.demo_scenario import apply_demo_scenario
from models.fifa_rules import build_group_table, build_third_place_table
from models.scoring import score_prediction


VALID_BRACKET_STATUSES = {
    "waiting_for_completed_results",
    "annex_c_loaded_but_mapping_pending",
    "ready",
}


def main() -> None:
    state = load_workbook_state()
    assert len(state["matches"]) == 104, f"Expected 104 matches, got {len(state['matches'])}"
    assert len(state["annex_c"]) == 495, f"Expected 495 Annex C rows, got {len(state['annex_c'])}"

    assert score_prediction("2-1", "2-1") == 5
    assert score_prediction("2-1", "3-1") == 2
    assert score_prediction("1-2", "3-1") == 0
    assert score_prediction("", "3-1") == 0

    blank_groups = build_group_table(state["matches"])
    blank_thirds = build_third_place_table(blank_groups)
    blank_bracket = build_bracket_mapping(blank_groups, blank_thirds, state["annex_c"])
    assert blank_bracket["status"] == "waiting_for_completed_results"

    demo_matches = apply_demo_scenario(state["matches"])
    demo_groups = build_group_table(demo_matches)
    demo_thirds = build_third_place_table(demo_groups)
    demo_bracket = build_bracket_mapping(demo_groups, demo_thirds, state["annex_c"])

    assert len(demo_groups) > 0, "Demo scenario should create group rows"
    assert len(demo_thirds) > 0, "Demo scenario should create third-place rows"
    assert demo_bracket["status"] in VALID_BRACKET_STATUSES

    import app  # noqa: F401

    print("HACKATHON_SMOKE_TESTS_PASS")
    print(f"matches={len(state['matches'])}")
    print(f"annex_c={len(state['annex_c'])}")
    print(f"blank_status={blank_bracket['status']}")
    print(f"demo_group_rows={len(demo_groups)}")
    print(f"demo_third_place_rows={len(demo_thirds)}")
    print(f"demo_bracket_status={demo_bracket['status']}")


if __name__ == "__main__":
    main()
