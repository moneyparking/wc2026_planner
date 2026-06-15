from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "releases" / "final" / "responsive_qa"
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
REPORT_JSON = OUTPUT_DIR / "PHASE_1_42_RESPONSIVE_QA_REPORT.json"
REPORT_MD = OUTPUT_DIR / "PHASE_1_42_RESPONSIVE_QA_REPORT.md"

VIEWPORTS = [
    {"name": "iphone_se_mini_like", "width": 375, "height": 812, "device": "iOS compact"},
    {"name": "iphone_12_13_14", "width": 390, "height": 844, "device": "iOS standard"},
    {"name": "iphone_pro_max", "width": 430, "height": 932, "device": "iOS large"},
    {"name": "android_compact", "width": 360, "height": 800, "device": "Android compact"},
    {"name": "pixel_samsung_common", "width": 412, "height": 915, "device": "Android common"},
    {"name": "ipad_portrait", "width": 768, "height": 1024, "device": "iPad portrait"},
    {"name": "laptop", "width": 1366, "height": 768, "device": "Desktop laptop"},
    {"name": "desktop", "width": 1920, "height": 1080, "device": "Desktop wide"},
]

REQUIRED_TEXT_PATTERNS = {
    "hero_product_name": r"AI Bracket War Room 2026",
    "demo_cta": r"Load Demo Scenario|Open Match Center|Demo Scenario",
    "recalculate_cta": r"Recalculate Impact|Recalculate.*War Room|Refresh Runtime",
    "match_center": r"Match Center|Match Planner",
    "ai_scout": r"AI Scout",
    "friends_league": r"Friends League",
    "premium_cta": r"Premium|Upgrade|Gumroad|Matchday Pack",
}

STATS_PATTERNS = [
    r"\b104\b",
    r"\b12\b",
]


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


@dataclass
class ViewportResult:
    name: str
    width: int
    height: int
    device: str
    passed: bool
    score: int
    screenshot: str
    checks: list[CheckResult]


def _safe_text_check(page: Page, pattern: str, timeout_ms: int = 2500) -> bool:
    try:
        page.get_by_text(re.compile(pattern, re.I)).first.wait_for(timeout=timeout_ms)
        return True
    except PlaywrightTimeoutError:
        return False


def _click_first_visible_text(page: Page, pattern: str, timeout_ms: int = 2500) -> bool:
    locator = page.get_by_text(re.compile(pattern, re.I)).first
    try:
        locator.wait_for(timeout=timeout_ms)
        locator.click(timeout=timeout_ms)
        page.wait_for_timeout(700)
        return True
    except Exception:
        return False


def _page_metrics(page: Page) -> dict[str, Any]:
    return page.evaluate(
        """() => {
            const body = document.body;
            const doc = document.documentElement;
            const interactive = Array.from(document.querySelectorAll('button, a, [role="button"], input, textarea, select'));
            const boxes = interactive.map((el) => {
                const r = el.getBoundingClientRect();
                const text = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 80);
                return { text, width: r.width, height: r.height, x: r.x, y: r.y, visible: r.width > 0 && r.height > 0 };
            }).filter(x => x.visible);

            const whiteBlocks = Array.from(document.querySelectorAll('div, section, main, article')).map((el) => {
                const r = el.getBoundingClientRect();
                const cs = window.getComputedStyle(el);
                return {
                    width: r.width,
                    height: r.height,
                    y: r.y,
                    bg: cs.backgroundColor,
                    visible: r.width > 150 && r.height > 60 && r.y < window.innerHeight
                };
            }).filter(x => x.visible && (
                x.bg === 'rgb(255, 255, 255)' ||
                x.bg === 'rgba(255, 255, 255, 1)' ||
                x.bg === 'rgb(249, 250, 251)' ||
                x.bg === 'rgb(248, 250, 252)'
            ));

            return {
                innerWidth: window.innerWidth,
                innerHeight: window.innerHeight,
                scrollWidth: Math.max(body.scrollWidth, doc.scrollWidth),
                clientWidth: doc.clientWidth,
                scrollHeight: Math.max(body.scrollHeight, doc.scrollHeight),
                horizontalOverflow: Math.max(body.scrollWidth, doc.scrollWidth) > doc.clientWidth + 2,
                minInteractiveHeight: boxes.length ? Math.min(...boxes.map(b => b.height)) : 0,
                smallTouchTargets: boxes.filter(b => b.height < 25 || b.width < 25).slice(0, 20),
                buttonLikeCount: boxes.length,
                whiteBlockCountAboveFold: whiteBlocks.length,
                whiteBlocksAboveFold: whiteBlocks.slice(0, 10),
                text: body.innerText.slice(0, 20000),
            };
        }"""
    )


def _above_fold_text(page: Page, pattern: str) -> bool:
    return page.evaluate(
        """(pattern) => {
            const rx = new RegExp(pattern, 'i');
            const nodes = Array.from(document.querySelectorAll('body *'));
            for (const el of nodes) {
                const text = (el.innerText || '').trim();
                if (!text || !rx.test(text)) continue;
                const r = el.getBoundingClientRect();
                if (r.width > 0 && r.height > 0 && r.top >= -20 && r.top < window.innerHeight) return true;
            }
            return false;
        }""",
        pattern,
    )


def _run_viewport(page: Page, url: str, viewport: dict[str, Any]) -> ViewportResult:
    checks: list[CheckResult] = []
    page.set_viewport_size({"width": viewport["width"], "height": viewport["height"]})
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(2500)

    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except PlaywrightTimeoutError:
        pass

    metrics = _page_metrics(page)

    checks.append(CheckResult(
        "app_loads",
        bool(metrics["text"].strip()),
        f"body text chars={len(metrics['text'])}",
    ))

    checks.append(CheckResult(
        "no_horizontal_scroll",
        not metrics["horizontalOverflow"],
        f"scrollWidth={metrics['scrollWidth']} clientWidth={metrics['clientWidth']}",
    ))

    for check_name, pattern in REQUIRED_TEXT_PATTERNS.items():
        passed = _safe_text_check(page, pattern)
        checks.append(CheckResult(check_name, passed, f"pattern={pattern}"))

    stats_hits = sum(1 for pattern in STATS_PATTERNS if _above_fold_text(page, pattern))
    checks.append(CheckResult(
        "stats_visible_above_fold",
        stats_hits >= 2,
        f"above-fold stat hits={stats_hits}/{len(STATS_PATTERNS)}",
    ))

    demo_clicked = _click_first_visible_text(page, r"Load Demo Scenario|Open Match Center|Demo Scenario")
    checks.append(CheckResult(
        "demo_action_clickable",
        demo_clicked,
        "clicked first visible demo/start CTA" if demo_clicked else "demo/start CTA not clickable",
    ))

    recalc_clicked = _click_first_visible_text(page, r"Recalculate Impact|Recalculate.*War Room|Refresh Runtime")
    checks.append(CheckResult(
        "recalculate_action_clickable",
        recalc_clicked,
        "clicked first visible recalculation CTA" if recalc_clicked else "recalculation CTA not clickable",
    ))

    post_metrics = _page_metrics(page)
    checks.append(CheckResult(
        "touch_targets_25px_minimum",
        len(post_metrics["smallTouchTargets"]) == 0,
        f"small targets={len(post_metrics['smallTouchTargets'])}; minInteractiveHeight={post_metrics['minInteractiveHeight']:.1f}px",
    ))

    checks.append(CheckResult(
        "interactive_controls_present",
        post_metrics["buttonLikeCount"] >= 4,
        f"interactive controls={post_metrics['buttonLikeCount']}",
    ))

    checks.append(CheckResult(
        "no_white_gradio_blocks_dominating_above_fold",
        post_metrics["whiteBlockCountAboveFold"] <= 2,
        f"white blocks above fold={post_metrics['whiteBlockCountAboveFold']}",
    ))

    screenshot_path = SCREENSHOT_DIR / f"{viewport['name']}_{viewport['width']}x{viewport['height']}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)

    passed_count = sum(1 for c in checks if c.passed)
    score = round((passed_count / len(checks)) * 100)
    hard_fail_names = {
        "app_loads",
        "no_horizontal_scroll",
        "hero_product_name",
        "demo_action_clickable",
        "recalculate_action_clickable",
    }
    hard_fail = any((c.name in hard_fail_names and not c.passed) for c in checks)
    passed = score >= 85 and not hard_fail

    return ViewportResult(
        name=viewport["name"],
        width=viewport["width"],
        height=viewport["height"],
        device=viewport["device"],
        passed=passed,
        score=score,
        screenshot=str(screenshot_path.relative_to(REPO_ROOT)),
        checks=checks,
    )


def _write_reports(results: list[ViewportResult], url: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    overall_passed = all(r.passed for r in results)
    average_score = round(sum(r.score for r in results) / len(results))

    payload = {
        "phase": "1.42",
        "qa_type": "responsive_cross_device",
        "url": url,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "overall_passed": overall_passed,
        "average_score": average_score,
        "viewports": [
            {
                **{k: v for k, v in asdict(r).items() if k != "checks"},
                "checks": [asdict(c) for c in r.checks],
            }
            for r in results
        ],
    }

    REPORT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# PHASE 1.42 Responsive QA Report",
        "",
        f"- URL: `{url}`",
        f"- Created UTC: `{payload['created_at']}`",
        f"- Overall: `{'PASS' if overall_passed else 'FAIL'}`",
        f"- Average score: `{average_score}/100`",
        "",
        "## Viewport Matrix",
        "",
        "| Viewport | Size | Device | Score | Result | Screenshot |",
        "|---|---:|---|---:|---|---|",
    ]

    for r in results:
        result = "PASS" if r.passed else "FAIL"
        lines.append(
            f"| {r.name} | {r.width}×{r.height} | {r.device} | {r.score}/100 | {result} | `{r.screenshot}` |"
        )

    lines.extend(["", "## Check Details", ""])

    for r in results:
        lines.append(f"### {r.name} — {r.width}×{r.height}")
        lines.append("")
        lines.append("| Check | Result | Detail |")
        lines.append("|---|---|---|")
        for c in r.checks:
            lines.append(f"| {c.name} | {'PASS' if c.passed else 'FAIL'} | {c.detail.replace('|', '/')} |")
        lines.append("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="PHASE 1.42 responsive QA for AI Bracket War Room 2026.")
    parser.add_argument("--url", default="http://127.0.0.1:7860", help="App URL to test.")
    parser.add_argument("--headed", action="store_true", help="Run browser in headed mode.")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    results: list[ViewportResult] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            )
        )
        page = context.new_page()

        for viewport in VIEWPORTS:
            print(f"[QA] {viewport['name']} {viewport['width']}x{viewport['height']}")
            try:
                result = _run_viewport(page, args.url, viewport)
            except Exception as exc:
                screenshot_path = SCREENSHOT_DIR / f"{viewport['name']}_{viewport['width']}x{viewport['height']}_error.png"
                try:
                    page.screenshot(path=str(screenshot_path), full_page=True)
                except Exception:
                    pass
                result = ViewportResult(
                    name=viewport["name"],
                    width=viewport["width"],
                    height=viewport["height"],
                    device=viewport["device"],
                    passed=False,
                    score=0,
                    screenshot=str(screenshot_path.relative_to(REPO_ROOT)),
                    checks=[CheckResult("viewport_runtime_error", False, repr(exc))],
                )
            results.append(result)

        context.close()
        browser.close()

    _write_reports(results, args.url)

    print(f"\nReport JSON: {REPORT_JSON}")
    print(f"Report MD:   {REPORT_MD}")
    print(f"Screenshots: {SCREENSHOT_DIR}")

    failed = [r for r in results if not r.passed]
    if failed:
        print("\nRESPONSIVE_QA_FAIL")
        for r in failed:
            print(f"- {r.name}: {r.score}/100")
        sys.exit(1)

    print("\nRESPONSIVE_QA_PASS")


if __name__ == "__main__":
    main()
