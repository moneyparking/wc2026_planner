from __future__ import annotations

from pathlib import Path
import os
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ["LIVE_SCORE_PROVIDER"] = "verified_cache"
os.environ.setdefault("GOOGLE_SHEET_ENABLED", "false")

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
    assert "not affiliated with fifa" in readme_lower or "not affiliated with or endorsed by fifa" in readme_lower
    assert "official logos, crests, sponsor marks, player likenesses" in readme_lower
    for phase_1_19_copy in (
        "Change one result",
        "104-match",
        "AI Scout",
        "Friends League",
        "Tournament Impact Panel",
    ):
        assert phase_1_19_copy in readme, f"README missing Phase 1.19 copy: {phase_1_19_copy}"
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
    assert loaded[4]["status"] in VALID_BRACKET_STATUSES

    demo_matches = apply_demo_scenario(state["matches"])
    demo_groups = build_group_table(demo_matches)
    demo_thirds = build_third_place_table(demo_groups)
    demo_bracket = build_bracket_mapping(demo_groups, demo_thirds, state["annex_c"])
    demo_html = app._bracket_html(demo_bracket)
    demo_outputs = app.load_demo_scenario_outputs(state, state["matches"])
    demo_friends = demo_outputs[6]
    ai_scout_output = app.build_ai_scout_output(demo_outputs[1])
    impact_panel_output = demo_outputs[10]
    first_screen_copy = app._command_header_html()
    recalculated_outputs = app.compute_outputs(demo_outputs[0], demo_outputs[1])
    filtered_group_a_html = app.filter_match_planner(demo_outputs[1], "Group A")
    filtered_knockout_html = app.filter_match_planner(demo_outputs[1], "Knockout Stage")
    random_outputs = app.generate_random_match_outcomes(demo_outputs[0], demo_outputs[1])
    runtime_outputs = app.compute_outputs(state)
    runtime_state = runtime_outputs[0]["runtime_matches"]
    match1_runtime = runtime_state[runtime_state["match_no"].eq(1)].iloc[0]
    group_a_runtime = runtime_outputs[2][runtime_outputs[2]["Group_ID"].eq("A")]
    google_sheet_control = app.google_sheet_control_html(runtime_outputs[0])
    ai_scout_runtime = app.build_ai_scout_output(runtime_outputs[1], runtime_state, runtime_outputs[6])

    assert len(demo_groups) > 0, "Demo scenario should create group rows"
    assert len(demo_thirds) > 0, "Demo scenario should create third-place rows"
    assert demo_bracket["status"] in VALID_BRACKET_STATUSES
    assert demo_outputs[4]["status"] in VALID_BRACKET_STATUSES
    assert "sport-card" in demo_html and "Canonical Bracket Summary" in demo_html
    assert len(demo_friends) > 0, "Friends League output should not be empty"
    assert ai_scout_output.strip(), "AI Scout output should not be empty"
    assert impact_panel_output.strip() and "Tournament Impact Panel" in impact_panel_output
    assert recalculated_outputs[7].strip(), "Dashboard output should not be empty"
    assert recalculated_outputs[9].strip(), "AI Scout callback output should not be empty"
    assert recalculated_outputs[10].strip(), "Impact Panel callback output should not be empty"
    assert len(recalculated_outputs[1]) > 0, "Recalculation should return match rows"
    assert len(recalculated_outputs[2]) > 0, "Recalculation should return group rows"
    assert len(recalculated_outputs[3]) > 0, "Recalculation should return third-place rows"
    assert recalculated_outputs[4]["status"] in VALID_BRACKET_STATUSES
    assert recalculated_outputs[4]["contract_version"] == "BracketJSON_v1_phase_1_21"
    assert recalculated_outputs[4]["canonical_format"] == "tree_by_match_key"
    assert "Match_73" in recalculated_outputs[4]["matches"]
    assert "Match_104" in recalculated_outputs[4]["matches"]
    assert len(recalculated_outputs[4]["matches_flat"]) == 32
    assert "Filtered rows: 6 / 104" in filtered_group_a_html
    assert "M001" in filtered_group_a_html
    assert "Filtered rows: 32 / 104" in filtered_knockout_html
    assert int(random_outputs[1]["Result"].astype(str).str.strip().ne("").sum()) == 104
    assert random_outputs[5]["contract_version"] == "BracketJSON_v1_phase_1_21"
    assert int(match1_runtime["home_score"]) == 2 and int(match1_runtime["away_score"]) == 0
    assert match1_runtime["result_source"] in {"verified public results cache", "manual override", "local manual edit"}
    assert int(group_a_runtime[group_a_runtime["Team"].eq("Mexico")].iloc[0]["Pts"]) == 3
    assert "Google Sheet control plane" in google_sheet_control
    assert "Mexico 2–0 South Africa" in ai_scout_runtime and "Result impact" in ai_scout_runtime
    for required_copy in ("Change one result", "104-match", "AI Scout", "Friends League"):
        assert required_copy in first_screen_copy, f"First-screen copy missing: {required_copy}"
    assert "PHASE_1_18H_HONEST_PREVIEW_LABELS" not in first_screen_copy
    lowered_ai_scout = ai_scout_output.lower()
    assert not any(term in lowered_ai_scout for term in BLOCKED_AI_SCOUT_TERMS)

    print("phase_1_25_offgrid_acceptance=PASS")
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
    print("impact_panel=PASS")
    print("first_screen_copy=PASS")
    print("readme_space_metadata=PASS")
    print("readme_disclaimer=PASS")
    print("phase_1_16_docs=PASS")
    print("phase_1_21_planner_filters=PASS")
    print("phase_1_21_bracket_json_contract=PASS")
    print("phase_1_21_random_104_outcomes=PASS")
    print("runtime_state=PASS")
    print("match1_result_ingestion=PASS")
    print("group_a_runtime_standings=PASS")
    print("google_sheet_control=PASS")
    print("ai_scout_runtime_context=PASS")


if __name__ == "__main__":
    main()
