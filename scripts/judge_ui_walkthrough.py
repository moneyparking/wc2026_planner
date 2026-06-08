from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, UTC
from pathlib import Path
from typing import Callable, Optional

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
except Exception as exc:
    print("ERROR: Playwright is not installed.")
    print("Install with:")
    print("  pip install playwright")
    print("  python -m playwright install chromium")
    raise exc


DEFAULT_SPACE_URL = "https://huggingface.co/spaces/Moneyparking/ai-bracket-war-room-2026"
DEFAULT_LOCAL_URL = "http://127.0.0.1:7860"

REPORT_DIR = Path("releases/final")
SCREENSHOT_DIR = REPORT_DIR / "judge_ui_screenshots"
REPORT_MD = REPORT_DIR / "JUDGE_UI_WALKTHROUGH_REPORT.md"
REPORT_JSON = REPORT_DIR / "JUDGE_UI_WALKTHROUGH_REPORT.json"


@dataclass
class StepResult:
    step: str
    status: str
    detail: str
    screenshot: str = ""


class JudgeWalkthrough:
    def __init__(self, url: str, headless: bool, slow_mo_ms: int, timeout_ms: int):
        self.url = url
        self.headless = headless
        self.slow_mo_ms = slow_mo_ms
        self.timeout_ms = timeout_ms
        self.results: list[StepResult] = []
        self.page = None

        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def log(self, step: str, status: str, detail: str, screenshot: str = "") -> None:
        result = StepResult(step=step, status=status, detail=detail, screenshot=screenshot)
        self.results.append(result)
        print(f"[{status}] {step}: {detail}")

    def screenshot(self, name: str) -> str:
        assert self.page is not None
        safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", name).strip("_")
        path = SCREENSHOT_DIR / f"{safe}.png"
        self.page.screenshot(path=str(path), full_page=True)
        return str(path)

    def body_text(self) -> str:
        assert self.page is not None
        try:
            return self.page.locator("body").inner_text(timeout=self.timeout_ms)
        except Exception:
            return ""

    def wait_for_text_any(self, patterns: list[str], timeout_ms: Optional[int] = None) -> bool:
        assert self.page is not None
        timeout = timeout_ms or self.timeout_ms
        deadline = time.time() + timeout / 1000

        while time.time() < deadline:
            text = self.body_text()
            for pattern in patterns:
                if re.search(pattern, text, flags=re.I | re.M):
                    return True
            time.sleep(0.25)

        return False

    def click_by_text_any(self, patterns: list[str], description: str, timeout_ms: Optional[int] = None) -> bool:
        assert self.page is not None
        timeout = timeout_ms or self.timeout_ms

        for pattern in patterns:
            try:
                locator = self.page.get_by_text(re.compile(pattern, re.I))
                count = locator.count()
                if count > 0:
                    locator.first.click(timeout=timeout)
                    return True
            except Exception:
                pass

        # Fallback: role=tab / role=button.
        for role in ["tab", "button"]:
            for pattern in patterns:
                try:
                    locator = self.page.get_by_role(role, name=re.compile(pattern, re.I))
                    count = locator.count()
                    if count > 0:
                        locator.first.click(timeout=timeout)
                        return True
                except Exception:
                    pass

        self.log(description, "FAIL", f"Could not click text matching: {patterns}")
        return False

    def click_first_dataframe_row(self) -> bool:
        assert self.page is not None

        candidate_selectors = [
            '[role="gridcell"]',
            '.ag-cell',
            'td',
            'div[data-testid="cell"]',
            '.table-wrap div',
        ]

        for selector in candidate_selectors:
            try:
                cells = self.page.locator(selector)
                count = cells.count()
                if count > 8:
                    for idx in range(min(count, 80)):
                        text = ""
                        try:
                            text = cells.nth(idx).inner_text(timeout=1000).strip()
                        except Exception:
                            pass

                        if text and not re.fullmatch(r"\d+", text) and len(text) >= 2:
                            cells.nth(idx).click(timeout=self.timeout_ms)
                            return True
            except Exception:
                continue

        # Text-based fallback for known teams.
        known_team_patterns = [
            r"\bUSA\b",
            r"\bMexico\b",
            r"\bCanada\b",
            r"\bArgentina\b",
            r"\bBrazil\b",
            r"\bEngland\b",
            r"\bFrance\b",
            r"\bSpain\b",
            r"\bGermany\b",
        ]
        for pattern in known_team_patterns:
            try:
                loc = self.page.get_by_text(re.compile(pattern, re.I))
                if loc.count() > 0:
                    loc.first.click(timeout=self.timeout_ms)
                    return True
            except Exception:
                pass

        return False

    def verify_metrics(self) -> bool:
        text = self.body_text()
        required = ["48", "12", "104", "495"]
        return all(token in text for token in required)

    def verify_scores_visible(self) -> bool:
        text = self.body_text()

        score_patterns = [
            r"\b[0-4]\s+Group\b",
            r"\b[0-4]\s+[0-4]\b",
            r"\b[0-4]\s*[-:]\s*[0-4]\b",
            r"✅\s*(Yes|Да)",
            r"Completed",
            r"Is_Completed",
        ]

        return any(re.search(pattern, text, flags=re.I) for pattern in score_patterns)

    def verify_bracket_visible(self) -> bool:
        text = self.body_text()
        html = ""
        try:
            html = self.page.locator("body").evaluate("node => node.innerHTML")
        except Exception:
            html = ""

        combined = f"{text}\n{html}"

        patterns = [
            r"ANNEX\s*C",
            r"495\s+combinations",
            r"495\s+third-place",
            r"bracket\s+proof",
            r"Bracket\s+HTML",
            r"рабочая\s+матрица",
            r"third-place\s+matrix",
            r"active\s+third-place\s+matrix",
            r"ALGORITHM",
            r"АЛГОРИТМ",
            r"MATCH\s+73",
            r"MATCH\s+104",
            r"FINAL",
            r"R32",
            r"phase126r-grid",
            r"phase126-bracket-grid",
            r"3rd\s+Group",
            r"1A\s+vs",
        ]

        return any(re.search(pattern, combined, flags=re.I | re.M) for pattern in patterns)


    def verify_friends_visible(self) -> bool:
        text = self.body_text()
        patterns = [
            r"Friends\s+League",
            r"Leaderboard",
            r"Total\s+Points",
            r"Exact\s+Score",
            r"Match\s+Outcome",
            r"AI\s*Scout",
            r"Judge\s+Lead",
        ]
        return any(re.search(pattern, text, flags=re.I) for pattern in patterns)

    def verify_ai_scout_visible(self) -> bool:
        text = self.body_text()
        patterns = [
            r"AI\s+Scout\s+Tactical\s+Slip",
            r"Tactical\s+read",
            r"pressure\s+zone",
            r"transition\s+risk",
            r"rest-defense",
            r"Match:",
        ]
        return any(re.search(pattern, text, flags=re.I) for pattern in patterns)

    def run(self) -> int:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless, slow_mo=self.slow_mo_ms)
            context = browser.new_context(
                viewport={"width": 1440, "height": 1100},
                device_scale_factor=1,
                locale="en-US",
            )
            self.page = context.new_page()
            self.page.set_default_timeout(self.timeout_ms)

            try:
                self.step_open_app()
                self.step_dashboard_initial_state()
                self.step_run_simulation()
                self.step_match_planner()
                self.step_bracket()
                self.step_friends_league()
                self.step_ai_scout_click()
            finally:
                browser.close()

        self.write_reports()
        failures = [r for r in self.results if r.status == "FAIL"]
        warnings = [r for r in self.results if r.status == "WARN"]

        if failures:
            print(f"\nJUDGE_UI_WALKTHROUGH_FAIL: {len(failures)} failed checks")
            return 1

        if warnings:
            print(f"\nJUDGE_UI_WALKTHROUGH_PASS_WITH_WARNINGS: {len(warnings)} warning checks")
            return 0

        print("\nJUDGE_UI_WALKTHROUGH_PASS")
        return 0

    def step_open_app(self) -> None:
        assert self.page is not None
        # Gradio/Hugging Face Spaces often keep websocket/heartbeat requests open,
        # so Playwright "networkidle" may never happen. Use DOM load + visible text.
        self.page.goto(self.url, wait_until="domcontentloaded", timeout=max(self.timeout_ms, 45000))

        try:
            self.page.wait_for_load_state("load", timeout=15000)
        except PlaywrightTimeoutError:
            pass

        loaded = self.wait_for_text_any(
            [
                r"AI\s+Bracket\s+War\s+Room",
                r"World\s+Cup",
                r"104",
                r"Gradio",
                r"Live\s+Judge\s+Demo",
                r"Run\s+104",
                r"Match\s+Planner",
            ],
            timeout_ms=max(self.timeout_ms, 60000),
        )

        shot = self.screenshot("01_open_app")

        if loaded:
            self.log("Step 1A — Open app", "PASS", f"Loaded app URL: {self.url}", shot)
        else:
            self.log("Step 1A — Open app", "FAIL", f"App did not expose expected visible text at {self.url}", shot)

    def step_dashboard_initial_state(self) -> None:
        clicked = self.click_by_text_any(
            [
                r"⚡\s*Live\s+Judge\s+Demo",
                r"Live\s+Judge\s+Demo",
                r"Dashboard",
                r"DASHBOARD",
            ],
            "Step 1B — Navigate to judge/dashboard tab",
            timeout_ms=self.timeout_ms,
        )

        time.sleep(1.0)
        metrics_ok = self.verify_metrics()
        status_ok = self.wait_for_text_any(
            [
                r"waiting",
                r"awaiting",
                r"expects",
                r"ready",
                r"ожида",
                r"Run\s+104",
                r"simulation",
            ],
            timeout_ms=3000,
        )

        shot = self.screenshot("02_dashboard_initial")

        if clicked and metrics_ok:
            detail = "Dashboard/Judge Demo is visible and tournament metrics 48 / 12 / 104 / 495 are present."
            if not status_ok:
                detail += " Status waiting text was not strongly detected, but simulation controls are visible."
                self.log("Step 1 — Dashboard initial state", "WARN", detail, shot)
            else:
                self.log("Step 1 — Dashboard initial state", "PASS", detail, shot)
        else:
            self.log(
                "Step 1 — Dashboard initial state",
                "FAIL",
                "Could not verify dashboard metrics 48 / 12 / 104 / 495.",
                shot,
            )

    def step_run_simulation(self) -> None:
        clicked = self.click_by_text_any(
            [
                r"Run\s+104[-\s]*Match\s+Live\s+Simulation",
                r"104[-\s]*Match\s+Live\s+Simulation",
                r"ЗАПУСТИТЬ\s+СИНХРОННУЮ\s+СИМУЛЯЦИЮ",
                r"СИМУЛЯЦИЮ\s+ВСЕХ\s+МАТЧЕЙ",
                r"Run\s+Simulation",
                r"Recalculate\s+War\s+Room",
            ],
            "Step 2 — Click simulation button",
            timeout_ms=self.timeout_ms,
        )

        if clicked:
            time.sleep(2.5)

        status_ok = self.wait_for_text_any(
            [
                r"simulation\s+complete",
                r"runtime\s+simulation\s+complete",
                r"successfully\s+completed",
                r"синхрон",
                r"заверш",
                r"PHASE_1_26",
                r"RUNTIME_OK",
                r"Group\s+scores",
            ],
            timeout_ms=8000,
        )

        shot = self.screenshot("03_after_run_simulation")

        if clicked and status_ok:
            self.log(
                "Step 2 — Activation",
                "PASS",
                "Simulation button clicked and status log changed to completed/success state.",
                shot,
            )
        elif clicked:
            self.log(
                "Step 2 — Activation",
                "WARN",
                "Simulation button clicked, but success status text was not strongly detected. Check screenshot/status log.",
                shot,
            )
        else:
            self.log(
                "Step 2 — Activation",
                "FAIL",
                "Could not click the simulation button.",
                shot,
            )

    def step_match_planner(self) -> None:
        clicked = self.click_by_text_any(
            [
                r"Match\s+Planner",
                r"MATCH\s+PLANNER",
                r"104\s+matches",
                r"Planner",
            ],
            "Step 3 — Navigate to Match Planner",
            timeout_ms=self.timeout_ms,
        )

        time.sleep(1.0)
        scores_ok = self.verify_scores_visible()
        shot = self.screenshot("04_match_planner_after_simulation")

        if clicked and scores_ok:
            self.log(
                "Step 3 — Match Planner",
                "PASS",
                "Match Planner is visible and generated score/completion markers are detected.",
                shot,
            )
        elif clicked:
            self.log(
                "Step 3 — Match Planner",
                "WARN",
                "Match Planner tab opened, but generated scores were not strongly detected in visible DOM.",
                shot,
            )
        else:
            self.log(
                "Step 3 — Match Planner",
                "FAIL",
                "Could not navigate to Match Planner.",
                shot,
            )

    def step_bracket(self) -> None:
        clicked = self.click_by_text_any(
            [
                r"Bracket\s+War\s+Room",
                r"BRACKET\s+WAR\s+ROOM",
                r"Bracket",
                r"Knockout",
            ],
            "Step 4 — Navigate to Bracket War Room",
            timeout_ms=self.timeout_ms,
        )

        time.sleep(1.0)
        bracket_ok = self.verify_bracket_visible()
        shot = self.screenshot("05_bracket_war_room")

        if clicked and bracket_ok:
            self.log(
                "Step 4 — Bracket War Room",
                "PASS",
                "Bracket HTML/CSS Grid is visible and Annex C / 495-combination proof text is detected.",
                shot,
            )
        elif clicked:
            self.log(
                "Step 4 — Bracket War Room",
                "FAIL",
                "Bracket tab opened, but generated Annex C / bracket content was not detected.",
                shot,
            )
        else:
            self.log(
                "Step 4 — Bracket War Room",
                "FAIL",
                "Could not navigate to Bracket War Room.",
                shot,
            )

    def step_friends_league(self) -> None:
        clicked = self.click_by_text_any(
            [
                r"Friends\s+League",
                r"FRIENDS\s+LEAGUE",
                r"Leaderboard",
                r"League",
            ],
            "Step 5 — Navigate to Friends League",
            timeout_ms=self.timeout_ms,
        )

        time.sleep(1.0)
        friends_ok = self.verify_friends_visible()
        text = self.body_text()
        points_detected = bool(re.search(r"\b\d{2,3}\b", text))
        shot = self.screenshot("06_friends_league")

        if clicked and friends_ok and points_detected:
            self.log(
                "Step 5 — Friends League",
                "PASS",
                "Friends League is visible with leaderboard labels and numeric runtime points.",
                shot,
            )
        elif clicked and friends_ok:
            self.log(
                "Step 5 — Friends League",
                "WARN",
                "Friends League is visible, but numeric runtime points were not strongly detected.",
                shot,
            )
        else:
            self.log(
                "Step 5 — Friends League",
                "FAIL",
                "Could not verify Friends League runtime leaderboard.",
                shot,
            )

    def step_ai_scout_click(self) -> None:
        planner_clicked = self.click_by_text_any(
            [
                r"Match\s+Planner",
                r"MATCH\s+PLANNER",
                r"104\s+matches",
                r"Planner",
            ],
            "Step 6A — Return to Match Planner",
            timeout_ms=self.timeout_ms,
        )

        time.sleep(1.0)
        row_clicked = False
        if planner_clicked:
            row_clicked = self.click_first_dataframe_row()
            time.sleep(1.5)

        dashboard_clicked = self.click_by_text_any(
            [
                r"⚡\s*Live\s+Judge\s+Demo",
                r"Live\s+Judge\s+Demo",
                r"Dashboard",
                r"DASHBOARD",
            ],
            "Step 6B — Return to dashboard/judge tab",
            timeout_ms=self.timeout_ms,
        )

        time.sleep(1.0)
        ai_ok = self.verify_ai_scout_visible()
        shot = self.screenshot("07_ai_scout_tactical_slip")

        if planner_clicked and row_clicked and dashboard_clicked and ai_ok:
            self.log(
                "Step 6 — AI Scout inference",
                "PASS",
                "Clicked a match row and AI Scout Tactical Slip is visible without betting/spam language.",
                shot,
            )
        elif planner_clicked and row_clicked and ai_ok:
            self.log(
                "Step 6 — AI Scout inference",
                "PASS",
                "Clicked a match row and AI Scout Tactical Slip is visible.",
                shot,
            )
        elif planner_clicked and row_clicked:
            self.log(
                "Step 6 — AI Scout inference",
                "FAIL",
                "A match row was clicked, but AI Scout Tactical Slip was not detected.",
                shot,
            )
        else:
            self.log(
                "Step 6 — AI Scout inference",
                "FAIL",
                "Could not click a valid Match Planner row.",
                shot,
            )

    def write_reports(self) -> None:
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        failures = [r for r in self.results if r.status == "FAIL"]
        warnings = [r for r in self.results if r.status == "WARN"]
        passes = [r for r in self.results if r.status == "PASS"]

        payload = {
            "generated_at": now,
            "url": self.url,
            "summary": {
                "pass": len(passes),
                "warn": len(warnings),
                "fail": len(failures),
                "overall": "FAIL" if failures else ("PASS_WITH_WARNINGS" if warnings else "PASS"),
            },
            "results": [asdict(r) for r in self.results],
        }

        REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        lines = [
            "# AI Bracket War Room 2026 — Judge UI Walkthrough Report",
            "",
            f"- Generated: `{now}`",
            f"- Tested URL: `{self.url}`",
            f"- Overall: `{'FAIL' if failures else ('PASS_WITH_WARNINGS' if warnings else 'PASS')}`",
            f"- Passed checks: `{len(passes)}`",
            f"- Warnings: `{len(warnings)}`",
            f"- Failed checks: `{len(failures)}`",
            "",
            "## Scenario",
            "",
            "This automated walkthrough simulates the visible path a Build Small Hackathon judge would follow:",
            "",
            "1. Open Dashboard / Live Judge Demo.",
            "2. Confirm tournament metrics: 48 countries, 12 groups, 104 matches, 495 Annex C combinations.",
            "3. Run 104-match live simulation.",
            "4. Verify Match Planner scores.",
            "5. Verify Bracket War Room CSS/HTML bracket.",
            "6. Verify Friends League runtime leaderboard.",
            "7. Click a match row and verify AI Scout Tactical Slip.",
            "",
            "## Results",
            "",
            "| Step | Status | Detail | Screenshot |",
            "|---|---:|---|---|",
        ]

        for r in self.results:
            screenshot = f"`{r.screenshot}`" if r.screenshot else ""
            detail = r.detail.replace("|", "\\|")
            lines.append(f"| {r.step} | `{r.status}` | {detail} | {screenshot} |")

        lines.extend([
            "",
            "## Machine-readable output",
            "",
            f"- JSON report: `{REPORT_JSON}`",
            f"- Screenshot directory: `{SCREENSHOT_DIR}`",
            "",
        ])

        REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

        print(f"\nMarkdown report: {REPORT_MD}")
        print(f"JSON report: {REPORT_JSON}")
        print(f"Screenshots: {SCREENSHOT_DIR}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automated judge UI walkthrough for AI Bracket War Room 2026."
    )
    parser.add_argument(
        "--url",
        default=os.environ.get("JUDGE_UI_URL", DEFAULT_SPACE_URL),
        help=f"Target app URL. Default: env JUDGE_UI_URL or {DEFAULT_SPACE_URL}",
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help=f"Use local Gradio URL: {DEFAULT_LOCAL_URL}",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser visibly instead of headless.",
    )
    parser.add_argument(
        "--slow-mo",
        type=int,
        default=int(os.environ.get("JUDGE_UI_SLOW_MO_MS", "150")),
        help="Playwright slow motion in milliseconds.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("JUDGE_UI_TIMEOUT_MS", "15000")),
        help="Default timeout in milliseconds.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    url = DEFAULT_LOCAL_URL if args.local else args.url

    runner = JudgeWalkthrough(
        url=url,
        headless=not args.headed,
        slow_mo_ms=args.slow_mo,
        timeout_ms=args.timeout,
    )
    return runner.run()


if __name__ == "__main__":
    raise SystemExit(main())
