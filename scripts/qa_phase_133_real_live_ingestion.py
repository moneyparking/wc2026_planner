from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
from html import unescape


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ["LIVE_SCORE_PROVIDER"] = "verified_cache"
os.environ.setdefault("GOOGLE_SHEET_ENABLED", "false")
for key in (
    "LIVE_SCORE_API_KEY",
    "LIVE_SCORE_API_SECRET",
    "FOOTBALL_DATA_API_KEY",
    "SPORTMONKS_API_KEY",
    "API_FOOTBALL_KEY",
):
    os.environ.pop(key, None)


FORBIDDEN_TERMS = ("od" + "ds", "bet" + "ting", "wager", "sports" + "book", "parlay", "payout")
PROVIDERS = ("none", "verified_cache", "local_json", "live_score_api", "football_data", "sportmonks", "api_football")


def _assert_contains(text: str, required: str, label: str) -> None:
    assert required in text, f"{label} missing: {required}"


def _assert_absent(text: str, forbidden: str, label: str) -> None:
    assert forbidden not in text, f"{label} contains forbidden text: {forbidden}"


def main() -> None:
    import app
    from src.live_score_adapter import fetch_live_results, get_live_score_status
    from src.runtime_engine import build_runtime_match_state
    from src.wc2026_data_loader import load_fixtures
    from src.google_sheet_adapter import SheetRuntimeState

    adapter_text = (REPO_ROOT / "src" / "live_score_adapter.py").read_text(encoding="utf-8")
    app_text = (REPO_ROOT / "app.py").read_text(encoding="utf-8")
    judge_text = (REPO_ROOT / "scripts" / "judge_ui_walkthrough.py").read_text(encoding="utf-8")
    active = "\n".join(
        [
            app._command_header_html(),
            app._appstore_first_screen_html(),
            app._visible_runtime_match_planner_html(app.initial_load()[0]["runtime_matches"]),
            app._visible_group_tracker_html(app.initial_load()[2]),
            app._visible_friends_league_html(app.initial_load()[6], app.initial_load()[0]["runtime_matches"]),
            app.build_ai_scout_output(app.initial_load()[1], app.initial_load()[0]["runtime_matches"], app.initial_load()[6]),
            app.google_sheet_control_html(app.initial_load()[0]),
        ]
    )
    active = unescape(active)

    _assert_contains(active, "PHASE 1.33 — Real Results + Live Ingestion Ready", "Phase marker")
    for provider in PROVIDERS:
        _assert_contains(adapter_text, provider, f"Provider support {provider}")

    verified_path = REPO_ROOT / "data" / "worldcup_results_verified.json"
    provider_map_path = REPO_ROOT / "data" / "provider_match_id_map.csv"
    assert verified_path.exists(), "worldcup_results_verified.json missing"
    assert provider_map_path.exists(), "provider_match_id_map.csv missing"

    verified = json.loads(verified_path.read_text(encoding="utf-8"))
    expected = {
        1: (2, 0),
        2: (2, 1),
        3: (1, 1),
        4: (4, 1),
    }
    for row in verified:
        match_no = int(row["match_no"])
        if match_no in expected:
            assert (int(row["home_score"]), int(row["away_score"])) == expected[match_no], f"M{match_no:03d} verified score mismatch"
    assert "2-1 South Africa" not in verified_path.read_text(encoding="utf-8"), "Old M001 2-1 in verified cache"

    fixtures = load_fixtures()
    live_results = fetch_live_results(fixtures)
    status = get_live_score_status()
    runtime = build_runtime_match_state(fixtures, live_results, SheetRuntimeState(False, False, "", "", [], [], [], []))
    assert int(runtime["is_completed"].sum()) == 4, "completed matches must be 4"
    assert int(runtime["is_live"].sum()) == 0, "live matches must be 0 without provider credentials"
    scheduled = runtime[~runtime["is_completed"].astype(bool)].sort_values("match_no")
    assert not scheduled.empty, "Expected an uncompleted next match"
    assert int(scheduled.iloc[0]["match_no"]) == 5, "Next match must be M005 or first uncompleted after M004"
    assert status.status_label == "OFF — using verified public results cache", "Live scores verified cache wording mismatch"

    for required in (
        "Live scores: OFF — using verified public results cache",
        "Result Source Truth",
        "Verified public results cache",
        "Google Sheet: OFF — ready to connect",
        "M001 Mexico 2–0 South Africa",
        "M002 Korea Republic 2–1 Czechia",
        "M003 Canada 1–1 Bosnia & Herzegovina",
        "M004 United States 4–1 Paraguay",
        "Actual Result",
        "Status",
        "Source",
        "Points",
        "AI Scout — Match Control Panel",
        "Runtime source: verified public results cache",
        "Results_Override",
        "Friends_Picks",
        "League_Settings",
        "Admin_Notes",
    ):
        _assert_contains(active, required, "Active UI")
    for required in ("Source priority", "Manual override", "live provider", "verified public cache", "static fixture seed"):
        _assert_contains(active, required, "Source priority")

    for required in (
        "Mexico",
        "Korea Republic",
        "Czechia",
        "South Africa",
        "Canada",
        "Bosnia & Herzegovina",
        "United States",
        "Paraguay",
    ):
        _assert_contains(active, required, "Team standings/UI")

    assert re.search(r"Mexico[\s\S]{0,200}3", active), "Group A must show Mexico 3"
    assert re.search(r"Korea Republic[\s\S]{0,200}3", active), "Group A must show Korea Republic 3"
    assert re.search(r"Canada[\s\S]{0,200}1", active), "Group B must show Canada 1"
    assert re.search(r"Bosnia & Herzegovina[\s\S]{0,200}1", active), "Group B must show Bosnia & Herzegovina 1"
    assert re.search(r"United States[\s\S]{0,200}3", active), "Group D must show United States 3"

    assert not re.search(r"M001\s+Mexico\s+2[\-–]1\s+South Africa", active), "Old M001 2-1 visible in active UI"
    assert "M001 Mexico 2-1 South Africa" not in app_text, "Old M001 2-1 active code path remains"
    for term in FORBIDDEN_TERMS:
        _assert_absent(active.lower(), term, "Active UI forbidden language")

    _assert_contains(judge_text, "JUDGE_UI_WALKTHROUGH_PHASE_1_33_PASS", "Walkthrough Phase 1.33 pass marker")

    print("phase_133_marker=PASS")
    print("live_adapter_providers=PASS")
    print("verified_results_cache=PASS")
    print("runtime_completed_4=PASS")
    print("runtime_live_0=PASS")
    print("result_source_truth=PASS")
    print("group_standings_verified=PASS")
    print("friends_league_verified_results=PASS")
    print("ai_scout_verified_result=PASS")
    print("google_sheet_override_ready=PASS")
    print("forbidden_language=PASS")
    print("PHASE_1_33_REAL_LIVE_INGESTION_QA_PASS")


if __name__ == "__main__":
    main()
