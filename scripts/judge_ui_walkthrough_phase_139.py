#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re


MARKER = "JUDGE_UI_WALKTHROUGH_PHASE_1_39_PASS"

REQUIRED_TEXT = [
    "AI Bracket War Room 2026",
    "48 teams",
    "12 groups",
    "104 matches",
    "Premium Matchday Pack",
]

FORBIDDEN_PUBLIC_TEXT = [
    "Judge QA / Debug",
    "Legacy / Debug Surface",
    "Generate Random Outcomes",
    "Clear Local Edits",
    "sportsbook",
    "casino",
    "wager",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:7860")
    parser.add_argument("--timeout", type=int, default=60000)
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        print("PLAYWRIGHT_NOT_AVAILABLE")
        print(str(exc))
        raise SystemExit(1)

    failures: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.set_default_timeout(args.timeout)
        page.set_default_navigation_timeout(args.timeout)

        page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout)
        page.locator("body").wait_for(state="visible", timeout=args.timeout)
        page.wait_for_timeout(3000)

        body = page.locator("body")
        body_text = body.inner_text(timeout=args.timeout)

        if args.dump:
            print("----- BODY TEXT START -----")
            print(body_text[:5000])
            print("----- BODY TEXT END -----")

        for text in REQUIRED_TEXT:
            if text not in body_text:
                failures.append(f"Required text not visible: {text}")

        lower_body = body_text.lower()
        for text in FORBIDDEN_PUBLIC_TEXT:
            if text.lower() in lower_body:
                failures.append(f"Forbidden public text visible: {text}")

        candidate_labels = [
            "Run Judge Demo",
            "Inspect Match",
            "View Bracket",
            "Open Friends League",
            "Ask AI Scout",
            "Unlock Premium Matchday Pack",
        ]

        clicked = 0
        visible_buttons = page.get_by_role("button")
        button_texts: list[str] = []

        for i in range(visible_buttons.count()):
            try:
                txt = visible_buttons.nth(i).inner_text(timeout=1000).strip()
                if txt:
                    button_texts.append(txt)
            except Exception:
                pass

        for label in candidate_labels:
            locator = page.get_by_role("button", name=re.compile(re.escape(label), re.I))
            if locator.count() == 0:
                continue

            locator.first.click(timeout=args.timeout)
            page.wait_for_timeout(1200)
            after = body.inner_text(timeout=args.timeout)
            clicked += 1

            if "Traceback" in after:
                failures.append(f"Traceback visible after clicking: {label}")

        if clicked == 0:
            failures.append(
                "No Phase 1.39 public action buttons found. "
                f"Visible buttons: {button_texts[:40]}"
            )

        if failures:
            print("JUDGE_UI_WALKTHROUGH_PHASE_1_39_FAIL")
            for failure in failures:
                print(f"- {failure}")
            browser.close()
            raise SystemExit(1)

        browser.close()

    print(MARKER)
    print(f"buttons_clicked={clicked}")


if __name__ == "__main__":
    main()
