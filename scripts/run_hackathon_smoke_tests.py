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
BLOCKED_AI_SCOUT_TERMS = ("bet" + "ting", "od" + "ds", "sports" + "book")
FORBIDDEN_README_PHRASES = (
    "official fifa app",
    "official world cup app",
    "sportsbook",
    "betting odds",
    "guaranteed prediction",
)


def _check_readme() -> None:
    readme_path = REPO_ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme_lower = readme.lower()

    assert readme.startswith("---\n"), "README must start with Hugging Face Space metadata"
    for required in (
        "title: AI Bracket War Room 2026",
        "sdk: gradio",
        "app_file: app.py",
    ):
        assert required in readme, f"README missing Space metadata: {required}"

    for required_link in (
        "SPACE_DEPLOYMENT.md",
        "JUDGE_DEMO_SCRIPT.md",
        "releases/final/QA_HACKATHON_APP_PHASE_1_16.md",
    ):
        assert required_link in readme, f"README missing Phase 1.16 link: {required_link}"

    assert "unofficial fan-made football tournament planning demo" in readme_lower
    assert "not affiliated with or endorsed by fifa" in readme_lower
    assert "official logos, crests, sponsor marks, player likenesses" in readme_lower
    assert not any(phrase in readme_lower for phrase in FORBIDDEN_README_PHRASES)


def _check_phase_1_16_docs() -> None:
    required_docs = (
        "SPACE_DEPLOYMENT.md",
        "JUDGE_DEMO_SCRIPT.md",
        "releases/final/QA_HACKATHON_APP_PHASE_1_16.md",
    )
    for relative_path in required_docs:
        doc_path = REPO_ROOT / relative_path
        assert doc_path.exists(), f"Missing Phase 1.16 doc: {relative_path}"
        assert doc_path.read_text(encoding="utf-8").strip(), f"Empty Phase 1.16 doc: {relative_path}"


def main() -> None:
    _check_readme()
    _check_phase_1_16_docs()

    state = load_workbook_state()
    assert len(state["matches"]) == 104, "Expected 104 matches, got {}".format(len(state["matches"]))
    assert len(state["annex_c"]) == 495, "Expected 495 Annex C rows, got {}".format(len(state["annex_c"]))

    assert score_prediction("2-1", "2-1") == 5
    assert score_prediction("2-1", "3-1") == 2
    assert score_prediction("1-2", "3-1") == 0
    assert score_prediction("", "3-1") == 0

    blank_groups = build_group_table(state["matches"])
    blank_thirds = build_third_place_table(blank_groups)
    blank_bracket = build_bracket_mapping(blank_groups, blank_thirds, state["annex_c"])
    assert blank_bracket["status"] == "waiting_for_completed_results"

    import app

    loaded = app.initial_load()
    assert loaded[4]["status"] == "waiting_for_completed_results"

    demo_matches = apply_demo_scenario(state["matches"])
    demo_groups = build_group_table(demo_matches)
    demo_thirds = build_third_place_table(demo_groups)
    demo_bracket = build_bracket_mapping(demo_groups, demo_thirds, state["annex_c"])
    demo_html = app._bracket_html(demo_bracket)
    demo_outputs = app.load_demo_scenario_outputs(state, state["matches"])
    demo_friends = demo_outputs[6]
    ai_scout_output = app.build_ai_scout_output(demo_outputs[1])

    assert len(demo_groups) > 0, "Demo scenario should create group rows"
    assert len(demo_thirds) > 0, "Demo scenario should create third-place rows"
    assert demo_bracket["status"] in VALID_BRACKET_STATUSES
    assert demo_outputs[4]["status"] in VALID_BRACKET_STATUSES
    assert "sport-card" in demo_html and "Canonical Bracket Summary" in demo_html
    assert len(demo_friends) > 0, "Friends League output should not be empty"
    assert ai_scout_output.strip(), "AI Scout output should not be empty"
    lowered_ai_scout = ai_scout_output.lower()
    assert not any(term in lowered_ai_scout for term in BLOCKED_AI_SCOUT_TERMS)

    print("HACKATHON_SMOKE_TESTS_PASS")
    print("matches={}".format(len(state["matches"])))
    print("annex_c={}".format(len(state["annex_c"])))
    print("blank_status={}".format(blank_bracket["status"]))
    print(f"demo_group_rows={len(demo_groups)}")
    print(f"demo_third_place_rows={len(demo_thirds)}")
    print("demo_bracket_status={}".format(demo_bracket["status"]))
    print("app_import=PASS")
    print("judge_demo_boot=PASS")
    print("bracket_preview=PASS")
    print(f"friends_rows={len(demo_friends)}")
    print("ai_scout=PASS")
    print("readme_space_metadata=PASS")
    print("readme_disclaimer=PASS")
    print("phase_1_16_docs=PASS")


if __name__ == "__main__":
    main()
