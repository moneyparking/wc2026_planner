#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

APP = Path("app.py")
README = Path("README.md")

def main() -> int:
    app = APP.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert "SF_PREMIUM_WAR_ROOM_CSS" in app, "Missing SF_PREMIUM_WAR_ROOM_CSS"
    assert "PHASE_138_CLEANUP_CSS" in app, "Missing PHASE_138_CLEANUP_CSS"
    assert 'gr.HTML("<style>"' not in app, "Duplicate raw <style> injection remains"
    assert 'gr.HTML("<style>" + SF_PREMIUM_WAR_ROOM_CSS' not in app, "Duplicate SF PMW style injection remains"

    blocks_start = app.find("with gr.Blocks")
    tabs_start = app.find("with gr.Tabs", blocks_start)
    assert blocks_start != -1, "Cannot find gr.Blocks"
    assert tabs_start != -1, "Cannot find gr.Tabs after gr.Blocks"

    public_before_tabs = app[blocks_start:tabs_start]
    forbidden_public = [
        "gr.HTML(value=_appstore_first_screen_html())",
        "gr.HTML(_appstore_first_screen_html())",
        "gr.HTML(value=_premium_cta_strip_html())",
        "gr.HTML(_premium_cta_strip_html())",
        "gr.HTML(value=_pmw_ai_scout_cards_html())",
        "gr.HTML(_pmw_ai_scout_cards_html())",
        "gr.HTML(value=_pmw_friends_exports_html())",
        "gr.HTML(_pmw_friends_exports_html())",
        "gr.HTML(value=_pmw_free_vs_premium_html())",
        "gr.HTML(_pmw_free_vs_premium_html())",
    ]
    for token in forbidden_public:
        assert token not in public_before_tabs, f"Forbidden public pre-tabs render remains: {token}"

    m = re.search(
        r"def _premium_matchday_war_room_shell_html\(.*?\n(?=def |\nwith gr\.Blocks|\Z)",
        app,
        flags=re.S,
    )
    assert m, "Cannot locate _premium_matchday_war_room_shell_html body"
    hero_body = m.group(0)
    for token in [
        "_pmw_ai_scout_cards_html(",
        "_pmw_friends_exports_html(",
        "_pmw_free_vs_premium_html(",
        "pmw-dashboard-grid",
    ]:
        assert token not in hero_body, f"Hero still contains token: {token}"

    assert "Verified Cache Mode" in app, "Runtime truth must contain Verified Cache Mode"
    assert "Real-time provider secrets are not configured" in app, "Missing real-time provider secret caveat"
    assert "with gr.Tab(\"💎 Premium\"" in app, "Missing 💎 Premium tab"
    assert "with gr.Tab(\"🏟️ Match Center\"" in app, "Missing 🏟️ Match Center tab"
    for token in ["Load Demo Scenario", "Refresh Runtime", "Recalculate", "Ask AI Scout", "Open Friends League", "Pull Google Sheet"]:
        assert token in app, f"Missing public action: {token}"
    assert 'href="#"' not in app, "Dead href=# remains"

    assert "Runtime Data Mode" in readme, "README missing Runtime Data Mode"
    assert "LIVE_SCORE_PROVIDER" in readme, "README missing LIVE_SCORE_PROVIDER"
    assert "LIVE_SCORE_API_KEY" in readme, "README missing LIVE_SCORE_API_KEY"

    assert readme.startswith("---\n"), "README must start with YAML frontmatter"
    assert "\n---\n" in readme, "README frontmatter must close"
    assert "short_description:" in readme, "README missing short_description"

    for line in readme.splitlines():
        if line.startswith("short_description:"):
            value = line.split(":", 1)[1].strip().strip('"').strip("'")
            assert len(value) <= 60, f"short_description too long: {len(value)}"
            break

    print("PHASE_1_38_PREMIUM_WORKSPACE_CLEANUP_QA_PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
