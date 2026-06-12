from __future__ import annotations

import os
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ["LIVE_SCORE_PROVIDER"] = "local_json"
os.environ.setdefault("GOOGLE_SHEET_ENABLED", "false")


FORBIDDEN_TERMS = ("od" + "ds", "bet" + "ting", "wager", "sports" + "book", "parlay", "payout")
OLD_ACTIVE_MARKERS = (
    "PHASE_1_30_PRODUCTION_FAN_APP_RUNTIME",
    "PHASE 1.30B Visual Surface + AppStore Shell",
    "PHASE_1_29A_UI_TRUTH_FULL_INTERACTION_FIX",
)
DEBUG_COPY = (
    "Scenario Controls",
    "Build Small Status",
    "Workbook:",
    "90-second Judge Verification",
    "Phase 1.29A Interaction Status",
    "Phase 1.30 Runtime Action Status",
    "War Room Runtime Engine",
    "Tournament Impact Panel",
    "Judge Demo Path",
)


def main() -> None:
    import app

    active = "\n".join(
        [
            app._command_header_html(),
            app._appstore_first_screen_html(),
            app._product_dashboard_html(),
        ]
    )
    app_text = (REPO_ROOT / "app.py").read_text(encoding="utf-8")

    assert "PHASE 1.32A — Final Product Shell" in active, "Phase 1.32A marker missing"
    for old_marker in OLD_ACTIVE_MARKERS:
        assert old_marker not in active, f"Old phase marker visible in active UI: {old_marker}"
    for debug in DEBUG_COPY:
        assert debug not in active, f"Debug copy visible in active dashboard: {debug}"

    for required in (
        "ABW",
        "Today’s Match Center",
        "M001 Mexico 2–1 South Africa · FT",
        "What Changed",
        "Runtime Status Cards",
        "Quick Navigation Cards",
        "Google Sheet Control Snapshot",
        "Completed matches",
        "1",
        "Live matches",
        "0",
        "Next match",
        "M002 Korea Republic vs Czechia",
        "Google Sheet: OFF — ready to connect",
    ):
        assert required in active, f"Active product shell missing: {required}"

    assert "0 completed match(es)" not in active, "Contradictory completed counter visible"
    assert "Google Sheet disabled" not in active, "Contradictory Google Sheet disabled wording visible"
    assert "Judge QA / Debug" in app_text, "Final debug tab missing"
    debug_tab_index = app_text.find('with gr.Tab("Judge QA / Debug")')
    assert debug_tab_index > app_text.find('with gr.Tab("📄 Google Sheet")'), "Debug tab is not last"

    lowered = active.lower()
    for term in FORBIDDEN_TERMS:
        assert term not in lowered, f"Forbidden language visible: {term}"

    print("phase_132a_marker=PASS")
    print("old_phase_markers_hidden=PASS")
    print("debug_ui_removed_from_active_dashboard=PASS")
    print("runtime_counters_consistent=PASS")
    print("google_sheet_status_consistent=PASS")
    print("debug_tab_last=PASS")
    print("forbidden_language=PASS")
    print("PHASE_1_32A_FINAL_PRODUCT_SHELL_QA_PASS")


if __name__ == "__main__":
    main()
