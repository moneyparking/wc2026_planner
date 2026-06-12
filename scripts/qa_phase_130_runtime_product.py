from __future__ import annotations

import os
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def main() -> None:
    os.environ["LIVE_SCORE_PROVIDER"] = "local_json"
    os.environ.setdefault("GOOGLE_SHEET_ENABLED", "false")

    import app
    from src.google_sheet_adapter import pull_sheet_runtime_state
    from src.live_score_adapter import fetch_live_results
    from src.runtime_engine import build_runtime_match_state
    from src.wc2026_data_loader import load_fixtures

    app_text = (REPO_ROOT / "app.py").read_text(encoding="utf-8")
    adapter_text = (REPO_ROOT / "src" / "live_score_adapter.py").read_text(encoding="utf-8")
    sheet_text = (REPO_ROOT / "src" / "google_sheet_adapter.py").read_text(encoding="utf-8")
    assert "PHASE 1.30" in app_text, "Phase 1.30 marker missing"
    assert "LIVE_SCORE_PROVIDER" in adapter_text and "GOOGLE_SHEET_ENABLED" in sheet_text, "Runtime env vars not handled safely"
    assert (REPO_ROOT / "data" / "live_results_override.json").exists(), "local_json live result file missing"

    live_results = fetch_live_results()
    sheet_state = pull_sheet_runtime_state()
    assert sheet_state.enabled is False and sheet_state.connected is False, "Google Sheet disabled mode should not connect"
    runtime = build_runtime_match_state(load_fixtures(), live_results, sheet_state)
    match1 = runtime[runtime["match_no"].eq(1)].iloc[0]
    assert match1["home"] == "Mexico" and match1["away"] == "South Africa", "Match 1 fixture mismatch"
    assert int(match1["home_score"]) == 2 and int(match1["away_score"]) == 1, "Match 1 result not ingested"
    assert match1["result_source"] in {"local_json", "manual override", "local manual edit"}, "Match 1 source mismatch"

    state = app.load_workbook_state()
    outputs = app.compute_outputs(state)
    groups = outputs[2]
    mexico = groups[(groups["Group_ID"].eq("A")) & (groups["Team"].eq("Mexico"))].iloc[0]
    south_africa = groups[(groups["Group_ID"].eq("A")) & (groups["Team"].eq("South Africa"))].iloc[0]
    assert int(mexico["Pts"]) == 3, "Mexico should have 3 pts from Match 1"
    assert int(south_africa["Pts"]) == 0, "South Africa should have 0 pts from Match 1"

    sheet_copy = app.google_sheet_control_html(outputs[0])
    assert "Google Sheet control plane" in sheet_copy
    assert "Results_Override" in sheet_copy and "Friends_Picks" in sheet_copy
    assert "How to connect your sheet" in sheet_copy

    ai_scout = app.build_ai_scout_output(outputs[1], outputs[0]["runtime_matches"], outputs[6])
    for required in ("Mexico 2-1 South Africa", "Result impact", "26 players", "Next action"):
        assert required in ai_scout, f"AI Scout missing runtime context: {required}"
    forbidden = ("betting", "odds", "sportsbook")
    assert not any(term in ai_scout.lower() for term in forbidden), "AI Scout contains forbidden betting terms"

    print("runtime_state=PASS")
    print("match1_result_ingestion=PASS")
    print("group_a_runtime_standings=PASS")
    print("google_sheet_control=PASS")
    print("ai_scout_runtime_context=PASS")
    print("PHASE_1_30_RUNTIME_PRODUCT_QA_PASS")


if __name__ == "__main__":
    main()
