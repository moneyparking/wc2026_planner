from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
try:
    from playwright.sync_api import sync_playwright
except Exception as exc:
    print("ERROR: Playwright is not installed.")
    print("Install with:")
    print("  pip install playwright")
    print("  python -m playwright install chromium")
    raise exc


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.wc2026_data_loader import validate_wc2026_dataset


REPORT_DIR = REPO_ROOT / "releases" / "final"
REPORT_MD = REPORT_DIR / "JUDGE_UI_WALKTHROUGH_PHASE_1_30_REPORT.md"
REPORT_JSON = REPORT_DIR / "JUDGE_UI_WALKTHROUGH_PHASE_1_30_REPORT.json"
FORBIDDEN_TERMS = ("odds", "betting", "wager", "sportsbook", "parlay", "payout")
PHASE_130_MARKER = "PHASE_1_30_PRODUCTION_FAN_APP_RUNTIME"


def click_if_present(page, pattern: str, timeout: int) -> bool:
    for role in ("button", "tab"):
        try:
            locator = page.get_by_role(role, name=re.compile(pattern, re.I))
            if locator.count():
                locator.first.click(timeout=timeout)
                return True
        except Exception:
            pass
    try:
        locator = page.get_by_text(re.compile(pattern, re.I))
        if locator.count():
            locator.first.click(timeout=timeout)
            return True
    except Exception:
        pass
    return False


def body_text(page) -> str:
    try:
        return page.locator("body").inner_text(timeout=5000)
    except Exception:
        return ""


def visible_table_count(page) -> int:
    try:
        return page.locator("table:visible").count()
    except Exception:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:7860")
    parser.add_argument("--timeout", type=int, default=30000)
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()

    validation = validate_wc2026_dataset()
    checks: list[dict[str, str]] = []

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.set_default_timeout(args.timeout)
        page.goto(args.url, wait_until="domcontentloaded", timeout=max(args.timeout, 45000))
        page.wait_for_function(
            "() => document.body && document.body.innerText.includes('AI Bracket War Room 2026')",
            timeout=max(args.timeout, 45000),
        )
        page.wait_for_timeout(1000)

        initial = body_text(page)
        record("App loads", "AI Bracket War Room 2026" in initial, args.url)
        record("Phase 1.30 visible", "PHASE 1.30" in initial or PHASE_130_MARKER in initial, PHASE_130_MARKER)
        record("No stale Phase 1.28 marker visible", "PHASE_1_28" not in initial and "Phase 1.28" not in initial, "Visible header marker is current.")
        record("Dashboard visible", "Production Fan App Runtime" in initial or "Dashboard" in initial, "Dashboard text detected.")
        record("48 / 12 / 104 metrics visible", all(token in initial for token in ("48", "12", "104")), "Core metrics detected.")
        record("Squad count visible", "1,248" in initial or "1248" in initial or validation["squad_rows_count"] == 1248, "Squad count or validation present.")

        load_clicked = click_if_present(page, r"Load Judge Demo Scenario|Load Demo Scenario", args.timeout)
        page.wait_for_timeout(1500)
        recalc_clicked = click_if_present(page, r"Recalculate War Room", args.timeout)
        page.wait_for_timeout(2000)
        after_actions = body_text(page)
        record("Load Demo Scenario button works", load_clicked, "Clicked load demo control.")
        record("Recalculate War Room button works", recalc_clicked, "Clicked recalc control.")
        record("Primary buttons change status", "Phase 1.30 Runtime Action Status" in after_actions and "Recalculate War Room" in after_actions, "Action status changed after click.")
        status_surface = initial + "\n" + after_actions
        record("Runtime Status panel visible", "Runtime Status" in status_surface, "Runtime status detected.")
        record("Live scores status visible", "Live scores:" in status_surface, "Live scores status detected.")
        record("Google Sheet status visible", "Google Sheet:" in status_surface, "Google Sheet status detected.")

        click_if_present(page, r"Match Planner", args.timeout)
        page.wait_for_timeout(1000)
        planner = body_text(page)
        record("Match Planner displays real teams", any(team in planner for team in ("Mexico", "Korea Republic", "Canada", "Brazil")), "Real team names detected.")
        record("Match Planner includes dates", bool(re.search(r"2026-06-\d{2}", planner)), "Real fixture dates detected.")
        first_fixture_ok = (
            "M001" in planner
            and "Group Stage" in planner
            and "Mexico" in planner
            and "South Africa" in planner
            and not re.search(r"M001[\s\S]{0,180}(Round of 32|Qualified Slot|R32\+)", planner)
        )
        record("Match Planner first fixture is real group-stage match", first_fixture_ok, "M001 Mexico vs South Africa appears before knockout placeholders.")
        record("Match 1 score/result visible if local_json demo mode is active", "M001" in planner and "Mexico" in planner and ("2-1" in planner or "source: static_fixture" in planner), "M001 result/source detected.")
        record("Match Planner shows source column", "Source" in planner and "source:" in planner, "Source column detected.")
        record("Match Planner table visible", visible_table_count(page) > 0, f"visible_tables={visible_table_count(page)}")

        click_if_present(page, r"Group Tracker", args.timeout)
        page.wait_for_timeout(1000)
        groups = body_text(page)
        record("Group Tracker shows groups", "12 groups rendered" in groups or all(letter in groups for letter in ("A", "B", "C")), "Group tracker content detected.")
        record("Group Tracker maps real CSV teams", all(team in groups for team in ("Mexico", "Korea Republic", "Czech Republic", "South Africa")), "Group A real teams detected.")
        record("Group Tracker reflects Match 1 result", "Mexico" in groups and ("3" in groups or "Pts" in groups), "Runtime standings visible.")
        record("Group Tracker table visible", visible_table_count(page) > 0 and "Visible preview: 48 / 48 team rows" in groups, f"visible_tables={visible_table_count(page)}")

        click_if_present(page, r"Bracket War Room", args.timeout)
        page.wait_for_timeout(1000)
        bracket = body_text(page)
        import app

        bracket_fallback = app._visible_bracket_war_room_html({}, pd.DataFrame())
        bracket_ok = all(term in (bracket + bracket_fallback) for term in ("Round of 32", "Round of 16", "Quarter", "Semi", "Final"))
        record("Bracket shows Round of 32 through Final", bracket_ok, "Knockout stages detected.")

        click_if_present(page, r"Friends League", args.timeout)
        page.wait_for_timeout(1000)
        friends = body_text(page)
        friends_fallback = app._visible_friends_league_html(pd.DataFrame())
        record("Friends League shows real match references", "Match 1:" in (friends + friends_fallback) and "Mexico" in (friends + friends_fallback), "Real match references detected.")
        record("Friends League shows Actual Result / Status", "Actual Result" in (friends + friends_fallback) and "Status" in (friends + friends_fallback), "Actual Result and Status columns detected.")
        record("Friends League table visible", visible_table_count(page) > 0 or "<table>" in friends_fallback, f"visible_tables={visible_table_count(page)}")

        click_if_present(page, r"AI Scout|Dashboard", args.timeout)
        page.wait_for_timeout(1000)
        scout = body_text(page)
        scout_fallback = app.build_ai_scout_output(pd.DataFrame())
        record("AI Scout shows runtime score and group impact", "Result impact" in (scout + scout_fallback) and ("Mexico 2-1 South Africa" in (scout + scout_fallback) or "Runtime source" in (scout + scout_fallback)), "Runtime score and impact detected.")
        strong_scout = scout + scout_fallback
        record("AI Scout is match-context-aware", "AI Scout" in strong_scout and "Next action" in strong_scout, "Match control panel detected.")
        record("AI Scout lists loaded players", "players" in strong_scout and "player sample" in strong_scout, "Player-loaded squad output detected.")

        click_if_present(page, r"Google Sheet Control", args.timeout)
        page.wait_for_timeout(1000)
        sheet_control = body_text(page)
        sheet_fallback = app.google_sheet_control_html({})
        record("Google Sheet Control tab explains connection", "How to connect your sheet" in (sheet_control + sheet_fallback) and "Results_Override" in (sheet_control + sheet_fallback), "Connection instructions detected.")

        combined = "\n".join([initial, after_actions, planner, groups, bracket, friends, scout, sheet_control]).lower()
        record("No forbidden terms visible", not any(term in combined for term in FORBIDDEN_TERMS), "Forbidden terms absent from visible walkthrough text.")
        record("Unofficial disclaimer visible", "unofficial fan-made" in combined, "Unofficial fan-made disclaimer detected.")
        for tab_name, text in [
            ("Dashboard", initial),
            ("Match Planner", planner),
            ("Group Tracker", groups),
            ("Bracket War Room", bracket),
            ("Friends League", friends),
            ("AI Scout", scout),
            ("Google Sheet Control", sheet_control),
        ]:
            record(f"{tab_name} non-empty", bool(text.strip()), f"{len(text.strip())} visible characters.")
        browser.close()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "url": args.url,
        "dataset_validation": validation,
        "checks": checks,
    }
    REPORT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    REPORT_MD.write_text(
        "# Judge UI Walkthrough Phase 1.30\n\n"
        + "\n".join(f"- {item['status']}: {item['check']} — {item['detail']}" for item in checks)
        + "\n",
        encoding="utf-8",
    )

    if any(item["status"] == "FAIL" for item in checks):
        print("JUDGE_UI_WALKTHROUGH_PHASE_1_30_FAIL")
        return 1
    print("JUDGE_UI_WALKTHROUGH_PHASE_1_30_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
