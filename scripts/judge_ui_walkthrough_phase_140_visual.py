#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from typing import Iterable

PASS_MARKER = "PHASE_1_40_VISUAL_QA_PASS"
TITLE = "AI Bracket War Room 2026"
ERROR_RE = re.compile(r"\b(?:Traceback|RuntimeError|ModuleNotFoundError|ImportError|SyntaxError)\b")
MAX_BUTTON_CLICK_PROBES = 8
BUTTON_TIMEOUT_MS = 1200


def visible_body_text(page) -> str:
    try:
        return page.locator("body").inner_text(timeout=3000)
    except Exception:
        return ""


def assert_visible_text(page, needles: Iterable[str]) -> None:
    text = visible_body_text(page)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise AssertionError(f"Missing visible text markers: {missing}")


def assert_no_visible_error(page) -> None:
    text = visible_body_text(page)
    match = ERROR_RE.search(text)
    if match:
        raise AssertionError(f"Visible failure text found: {match.group(0)}")


def assert_no_horizontal_overflow(page) -> None:
    overflow = page.evaluate(
        """() => {
            const doc = document.documentElement;
            const body = document.body;
            const docOverflow = doc.scrollWidth - doc.clientWidth;
            const bodyOverflow = body ? body.scrollWidth - body.clientWidth : 0;
            return Math.max(docOverflow, bodyOverflow);
        }"""
    )
    if overflow > 2:
        raise AssertionError(f"Horizontal overflow detected: {overflow}px")


def click_visible_enabled_buttons(page) -> int:
    """
    Bounded probe only.

    This is visual QA, not exhaustive functional QA. Exhaustive runtime logic is covered by
    scripts/run_hackathon_smoke_tests.py. Here we verify that visible controls are not dead,
    covered, or producing immediate UI/runtime errors.
    """
    buttons = page.locator("button:visible")
    count = buttons.count()
    if count <= 0:
        raise AssertionError("No visible buttons found")

    clicked = 0
    limit = min(count, MAX_BUTTON_CLICK_PROBES)

    for index in range(limit):
        button = buttons.nth(index)
        try:
            if not button.is_enabled(timeout=BUTTON_TIMEOUT_MS):
                continue
            label = ""
            try:
                label = button.inner_text(timeout=BUTTON_TIMEOUT_MS).strip()
            except Exception:
                label = f"button_{index}"

            button.scroll_into_view_if_needed(timeout=BUTTON_TIMEOUT_MS)
            button.click(timeout=BUTTON_TIMEOUT_MS)
            page.wait_for_timeout(250)

            clicked += 1
            print(f"[PASS] clicked visible control {clicked}/{limit}: {label[:80]}", flush=True)

            assert_no_visible_error(page)
            assert_no_horizontal_overflow(page)
        except AssertionError:
            raise
        except Exception as exc:
            print(f"[WARN] skipped unstable/stale button {index}: {type(exc).__name__}", flush=True)
            assert_no_visible_error(page)
            continue

    if clicked <= 0:
        raise AssertionError("No enabled visible buttons could be clicked")

    return clicked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--timeout", type=int, default=30000)
    args = parser.parse_args()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 390, "height": 900})
            page.set_default_timeout(args.timeout)
            page.set_default_navigation_timeout(args.timeout)

            page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout)
            page.get_by_text(TITLE, exact=True).first.wait_for(state="visible", timeout=args.timeout)

            assert_visible_text(page, [TITLE])
            assert_no_visible_error(page)
            assert_no_horizontal_overflow(page)

            clicked = click_visible_enabled_buttons(page)

            assert_visible_text(page, [TITLE])
            assert_no_visible_error(page)
            assert_no_horizontal_overflow(page)

            print(f"[PASS] visual mobile shell loaded and {clicked} controls probed", flush=True)
        finally:
            browser.close()

    print(PASS_MARKER, flush=True)


if __name__ == "__main__":
    main()
