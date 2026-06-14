#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


REQUIRED_COPY = [
    "AI Bracket War Room 2026",
    "PremiumMatchdayWarRoom2026",
    "Advanced AI Scout Cards",
    "Friends League Exports",
    "Free vs Premium",
    "Premium Matchday",
]

REQUIRED_ACTIONS = [
    "Scroll to Match Center",
    "Scroll to AI Scout",
    "Scroll to Premium",
    "Buy Premium Matchday",
    "Buy Gumroad Source",
]

REQUIRED_CSS = [
    "border-radius: 999px",
    "overflow: hidden",
    "border: 0",
    "#071018",
    "#0B1320",
    "#A7FF00",
    "#FFD166",
    "#35D6E8",
    "@media (max-width: 760px)",
]


def main() -> None:
    import app

    shell = app._premium_matchday_war_room_shell_html()
    conversion = app._pmw_premium_conversion_panel_html()
    pricing = app._pmw_free_vs_premium_html()
    css = app.FINAL_PREMIUM_ALL_TABS_CSS
    combined = shell + conversion + pricing

    failures: list[str] = []

    for text in REQUIRED_COPY:
        if text not in combined:
            failures.append(f"missing public copy: {text}")

    for text in REQUIRED_ACTIONS:
        if not re.search(re.escape(text), combined, flags=re.I):
            failures.append(f"missing action/CTA: {text}")

    for text in REQUIRED_CSS:
        if text not in css:
            failures.append(f"missing CSS contract: {text}")

    if failures:
        print("PHASE_139_BUTTON_INVENTORY_FAIL")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("PHASE_139_BUTTON_INVENTORY_PASS")


if __name__ == "__main__":
    main()
