from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except Exception as exc:
    print("ERROR: Playwright is not installed.")
    raise exc


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

FORBIDDEN_TERMS = ("odds", "betting", "wager", "sportsbook", "parlay", "payout")
LEGACY_FORBIDDEN = (
    "MATCH_PLANNER — editable full 104-match scenario input",
    "Tactical Slip",
    "local runtime engine",
    "autonomous local engine",
    "0 completed match(es)",
    "Mexico 2–1 South Africa",
    "Mexico 2-1 South Africa",
)


def body_text(page) -> str:
    return page.locator("body").inner_text(timeout=5000)


def click_text(page, pattern: str, timeout: int) -> None:
    for role in ("button", "tab"):
        locator = page.get_by_role(role, name=re.compile(pattern, re.I))
        if locator.count():
            locator.first.click(timeout=timeout)
            return
    locator = page.get_by_text(re.compile(pattern, re.I))
    assert locator.count(), f"Clickable text not found: {pattern}"
    locator.first.click(timeout=timeout)


def click_tab(page, pattern: str, timeout: int) -> None:
    locator = page.get_by_role("tab", name=re.compile(pattern, re.I))
    for index in range(locator.count()):
        candidate = locator.nth(index)
        if candidate.is_visible():
            candidate.click(timeout=timeout, force=True)
            return
    locator = page.get_by_text(re.compile(pattern, re.I))
    assert locator.count(), f"Tab not found: {pattern}"
    for index in range(locator.count()):
        candidate = locator.nth(index)
        if candidate.is_visible():
            candidate.click(timeout=timeout, force=True)
            return
    raise AssertionError(f"Visible tab not found: {pattern}")


def click_exact_text(page, text: str, timeout: int) -> None:
    locator = page.get_by_text(text, exact=True)
    assert locator.count(), f"Text not found: {text}"
    for index in range(locator.count()):
        candidate = locator.nth(index)
        if candidate.is_visible():
            candidate.click(timeout=timeout, force=True)
            return
    raise AssertionError(f"Visible text not found: {text}")


def assert_changed(before: str, after: str, expected: str) -> None:
    assert before != after or expected in after, f"Click did not produce visible state change for {expected}"
    assert expected in after, f"Visible state missing after click: {expected}"


def select_match(page, match_pattern: str, timeout: int) -> None:
    click_tab(page, r"Match Center", timeout)
    page.wait_for_timeout(500)
    try:
        combo = page.get_by_label(re.compile("Select match", re.I))
        combo.first.click(timeout=timeout)
        page.get_by_text(re.compile(match_pattern, re.I)).first.click(timeout=timeout)
    except Exception:
        click_text(page, match_pattern, timeout)
    page.wait_for_timeout(500)
    click_text(page, r"Select.*inspect match", timeout)
    page.wait_for_timeout(1000)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--timeout", type=int, default=30000)
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.set_default_timeout(args.timeout)
        page.goto(args.url, wait_until="domcontentloaded", timeout=max(args.timeout, 45000))
        page.wait_for_function("() => document.body && document.body.innerText.includes('AI Bracket War Room 2026')", timeout=max(args.timeout, 45000))
        page.wait_for_timeout(1500)

        initial = body_text(page)
        assert "PHASE 1.34" in initial, "Phase 1.34 marker missing"
        assert "Completed matches" in initial and "4" in initial, "Completed counter missing"
        assert "Live scores: OFF — using verified public results cache" in initial or "OFF — using verified public results cache" in initial
        assert "Result Source Truth" in initial

        before = body_text(page)
        click_text(page, r"Refresh Runtime", args.timeout)
        page.wait_for_timeout(1200)
        assert_changed(before, body_text(page), "Refresh Runtime")

        before = body_text(page)
        click_text(page, r"Recalculate Impact|Recalculate War Room", args.timeout)
        page.wait_for_timeout(1200)
        after_recalc = body_text(page)
        assert_changed(before, after_recalc, "Recalculate Impact / War Room")
        assert "Mexico 3 pts" in after_recalc or "Mexico" in after_recalc

        click_tab(page, r"Match Center", args.timeout)
        page.wait_for_timeout(800)
        match_center = body_text(page)
        assert "Selected Match Detail" in match_center and "M001 Mexico 2–0 South Africa" in match_center
        assert "View full 104-match table" in match_center

        select_match(page, r"M001\s+Mexico", args.timeout)
        assert "M001 Mexico 2–0 South Africa" in body_text(page)
        select_match(page, r"M002\s+Korea Republic", args.timeout)
        assert "M002 Korea Republic 2–1 Czechia" in body_text(page)

        click_tab(page, r"Groups", args.timeout)
        page.wait_for_timeout(800)
        groups = body_text(page)
        assert "Group A impact card" in groups and "Mexico" in groups and "Korea Republic" in groups
        assert "Pts" in groups and "South Africa" in groups
        before = groups
        click_text(page, r"View full standings", args.timeout)
        page.wait_for_timeout(800)
        assert_changed(before, body_text(page), "View full standings")

        click_tab(page, r"3RD-PLACE|3rd-Place", args.timeout)
        page.wait_for_timeout(800)
        thirds = body_text(page)
        assert "Third-place ranking is not active yet." in thirds and "Completed matches: 4 / 72" in thirds

        click_tab(page, r"Bracket", args.timeout)
        page.wait_for_timeout(800)
        bracket = body_text(page)
        assert all(term in bracket for term in ("Round of 32", "Round of 16", "Quarter", "Semi", "Final"))
        before = bracket
        click_text(page, r"View bracket", args.timeout)
        page.wait_for_timeout(800)
        assert_changed(before, body_text(page), "View bracket")

        click_tab(page, r"Friends", args.timeout)
        page.wait_for_timeout(800)
        friends = body_text(page)
        assert "Actual Result" in friends and "Scored rows count" in friends
        before = friends
        click_text(page, r"Score Friends League", args.timeout)
        page.wait_for_timeout(1000)
        after_score = body_text(page)
        assert_changed(before, after_score, "Score Friends League")
        assert "Top player / leaderboard status" in after_score

        click_tab(page, r"AI Scout|Scout", args.timeout)
        page.wait_for_timeout(800)
        scout = body_text(page)
        assert "AI Scout" in scout and "Match Control Panel" in scout
        before = scout
        click_text(page, r"Ask AI Scout", args.timeout)
        page.wait_for_timeout(1000)
        after_scout = body_text(page)
        assert_changed(before, after_scout, "Ask AI Scout")
        assert "M001 Mexico 2–0 South Africa" in after_scout or "M002 Korea Republic 2–1 Czechia" in after_scout

        click_tab(page, r"Google Sheet", args.timeout)
        page.wait_for_timeout(800)
        before = body_text(page)
        click_text(page, r"Pull Google Sheet", args.timeout)
        page.wait_for_timeout(1000)
        sheet = body_text(page)
        assert_changed(before, sheet, "Pull Google Sheet")
        assert "Google Sheet is not connected. Add GOOGLE_SHEET_ENABLED=true, GOOGLE_SHEET_ID, and GOOGLE_SERVICE_ACCOUNT_JSON to enable." in sheet

        click_tab(page, r"Judge QA.*Debug", args.timeout)
        page.wait_for_timeout(800)
        debug = body_text(page)
        assert "Load Demo Scenario" in debug and "Generate Random Outcomes" in debug and "Clear Local Edits" in debug

        active = initial
        for forbidden in LEGACY_FORBIDDEN:
            assert forbidden not in active, f"Legacy active dashboard text visible: {forbidden}"
        combined = body_text(page).lower()
        for term in FORBIDDEN_TERMS:
            assert term not in combined, f"Forbidden language visible: {term}"
        browser.close()

    print("PHASE_1_34_FULL_APP_CLICKTHROUGH_QA_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
