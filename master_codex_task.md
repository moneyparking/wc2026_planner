

# MASTER CODEX TASK — AI Bracket War Room 2026 FINAL PATCH

## Role

You are **Codex Coding Engineer** working inside the `wc2026_planner` Codespace.

Your mission is to make the Hugging Face Space **AI Bracket War Room 2026** final, judge-ready, premium-looking, and product-ready in **one precise coding pass**.

This is a consolidation task. Do **not** expand scope. Do **not** invent a new app. Do **not** rewrite the runtime engine.

---

## Current Target

**Project:** AI Bracket War Room 2026  
**Repo directory:** `/workspaces/wc2026_planner`  
**Main file to patch:** `app_pixel_perfect_premium.py`  
**Fallback file if the repo uses only one app entrypoint:** `app.py`  
**Target phase:** `PHASE_1_41_FINAL_HAPPY_PATH_PIXEL_PERFECT`  
**Product-readiness target:** 82/100 → 9.5+ judge score on first-screen clarity, demo path, visible state change, UI polish, and monetization clarity.

---

## Non-Negotiable Constraints

1. Preserve the runtime engine.
2. Preserve dataset loaders.
3. Preserve Friends League scoring logic.
4. Preserve AI Scout logic.
5. Preserve Google Sheet functions.
6. Preserve verified cache mode.
7. Preserve safety/legal disclaimers:
   - unofficial fan-made;
   - no gambling;
   - no official affiliation;
   - no official marks/logos/crests/player likenesses.
8. No new dependencies.
9. Keep Gradio 5.34.2 compatibility.
10. Do not put raw components directly inside `gr.Tabs` outside `gr.Tab`.
11. Keep all existing `.click()` handlers functional after output tuple changes.
12. Make minimal diffs where possible.
13. No placeholders.
14. No TODO comments.
15. No broken or dangling component references.

---

# SECTION 1 — How to Use the Other 3 CustomGPT Agents

Before applying code, if these agents are available in the same ChatGPT workspace, query them once to refresh their latest recommendations. Use the prompts below exactly.

If they are not available, continue using the embedded consolidated specs in this file.

## 1A. Query: Gradio Product Architect

```text
You are HF Gradio Product Architect for AI Bracket War Room 2026.

Review the current target file app_pixel_perfect_premium.py and produce only implementation-critical patch guidance.

Goal:
Make the first-screen and tab flow judge-winning:
Hero + stats row 104/12/156/24 + happy path:
1 · Load Demo Scenario
2 · Recalculate War Room
3 · Review Ripple Effects

Demote all Refresh Runtime, Pull Google Sheet, Judge QA, Debug, legacy/admin controls into one Accordion named Operator Tools, open=False.

Keep AI Scout Cards and Private Friends League as dedicated tabs.
Add ripple_review_html after Load Demo/Recalculate.
Keep Gradio-safe output tuple ordering.

Return:
1. Exact component structure.
2. Output tuple changes.
3. Binding changes.
4. QA risks.
No scope expansion.
```

Expected output to integrate:
- Public first screen must show only the fan/judge happy path.
- Operator controls must move to `gr.Accordion("Operator Tools", open=False)`.
- `ripple_review_html` must be populated after Load Demo and Recalculate.
- AI Scout and Friends League should remain accessible without page reload via dedicated tabs and optional visible modal/group surfaces.

## 1B. Query: SF Design Elite

```text
You are SF Design Elite for AI Bracket War Room 2026.

Review app_pixel_perfect_premium.py and output only final UI/CSS changes needed to match a premium sports-tech command center.

Strict design target:
- stadium night background #071018 / #0B1320;
- neon lime #A7FF00, gold #FFD166, cyan #35D6E8;
- neon only on CTA / primary buttons;
- all cards unified glass-effect;
- no legacy Gradio look;
- stats row above fold:
  104 Matches / 12 Groups / 156 AI Scout Cards / 24 Exports;
- AI Scout cards exactly:
  Match Pressure / Key Matchup / Bracket Impact;
- mobile 375px: stats remain visible above fold, CTAs full-width.

Return:
1. Final CSS override block.
2. Required HTML/class changes.
3. Mobile QA checklist.
No new features.
```

Expected output to integrate:
- Append final CSS last in `gr.Blocks(css=...)`.
- Use `PHASE_141_PIXEL_PERFECT_PREMIUM_UNIFIED_CSS` or equivalent final override.
- Cards with `.pmw-card`, `.pmw-final-card`, `.pmw-final-stat`, `.sport-card`, `.app-card`, `.card-shell`, `.price-card`, `.premium-pricing-grid article` should share the same premium glass system.
- Reduce neon leaks in non-CTA elements.
- Suppress default Gradio visual artifacts.

## 1C. Query: HF Build Small Judge Evaluator

```text
You are HF Build Small Judge Evaluator.

Evaluate AI Bracket War Room 2026 against the current scoring rubric.

Use the judge demo path:
10s hero → Load Demo Scenario → Recalculate War Room → Review Ripple → AI Scout → Friends League → Premium CTA.

Return only:
1. Current scorecard 0-10 by category.
2. Critical blockers ranked high/medium/low.
3. Highest-impact final code patch.
4. Final 60-second demo script.
5. Pass/fail gate for submission.

Assume no hidden functionality. Judge only visible app behavior and repository quality.
```

Expected output to integrate:
- Exact first-screen stats row is a scoring blocker.
- Button naming mismatch is a scoring blocker.
- Premium CTA must be visible in hero, not buried.
- AI Scout labels must be `Match Pressure`, `Key Matchup`, `Bracket Impact`.
- Public operator leakage reduces product polish.

---

# SECTION 2 — Consolidated Specs From the 4-Agent System

## Grok Architect Output — Product Wrapper Direction

Grok’s role is not to rewrite the repository. Grok defines the CustomGPT/product wrapper around the Hugging Face Space.

Use this direction as product framing only:

- HF Space is the free runtime layer of a premium product.
- The app must look like a finished fan product, not a Gradio demo.
- Core promise:
  **Change one score and instantly understand group movement, third-place pressure, bracket path, Friends League swing, and AI Scout explanation.**
- Judge path must be visible in under 10 seconds.
- Premium funnel must be clear:
  - Free core demo;
  - Premium Matchday Pack;
  - Ultimate bundle;
  - Source/business tier.
- Avoid all official World Cup/FIFA branding and gambling language.

Do not add a new monetization engine. Only improve visible product packaging and CTA clarity.

---

## HF Gradio Product Architect — Implementation Spec

Implement exact happy path:

```text
Open Space
→ click Load Demo Scenario
→ click Recalculate War Room
→ Review Ripple Effects visible:
   Match Center
   Groups
   Third-place
   Bracket
   AI Scout
   Friends League
→ open AI Scout
→ open Friends League
→ open Premium CTA
```

Public first screen must contain:

1. Hero.
2. Stats row:
   - 104 Matches
   - 12 Groups
   - 156 AI Scout Cards
   - 24 Exports
3. Main action rail:
   - `1 · Load Demo Scenario`
   - `2 · Recalculate War Room`
   - `3 · Review Ripple Effects`
   - `Open AI Scout`
   - `Open Friends League`
4. Ripple review board after interaction.
5. Strong Premium CTA:
   - `Unlock Premium Matchday Pack — $9`

Operator/admin controls must move into:

```python
with gr.Accordion("Operator Tools", open=False, elem_classes=["pmw-operator-tools"]):
    ...
```

Move these out of the public first-screen/top-level flow:

- Refresh Runtime
- Pull Google Sheet
- Google Sheet control panel
- Judge QA / Debug
- Legacy admin surfaces
- raw source-priority/debug copy

Keep them functional inside Operator Tools.

---

## SF Design Elite — Final Visual Spec

Design system:

```text
Background: #071018 / #0B1320
Text: #F8FAFC
Muted: #A9B8C9
Neon lime: #A7FF00
Gold: #FFD166
Cyan: #35D6E8
Error/alert: #FB7185
Radius: 22px–30px cards, 999px buttons
Grid: 8px system
Typography: clean sans, heavy product headings
Icon style: flat/line only
```

Visual behavior:

- All cards share one premium glass system.
- Tables are secondary surfaces.
- Neon is limited to:
  - primary CTA;
  - primary demo/recalculate buttons;
  - controlled glow on hero.
- No default white Gradio panels.
- No inconsistent card borders.
- No mixed legacy button styles.
- Mobile:
  - hero remains readable;
  - stats stay above fold;
  - CTAs full-width;
  - ripple grid collapses to one column under 760px.

---

## HF Build Small Judge Evaluator — Scoring Blockers

Fix these before submission:

1. First-screen stats must exactly read:
   - `104 Matches`
   - `12 Groups`
   - `156 AI Scout Cards`
   - `24 Exports`

2. Recalculate button must say:
   - `2 · Recalculate War Room`

3. AI Scout cards must exactly read:
   - `Match Pressure`
   - `Key Matchup`
   - `Bracket Impact`

4. Hero must include hard CTA:
   - `Unlock Premium Matchday Pack — $9`

5. Operator controls must not appear in the public path.

6. README or visible copy should have one canonical demo path:
   - Load Demo → Recalculate War Room → Review Ripple → AI Scout → Friends League → Premium.

---

# SECTION 3 — Exact Copy Schema

Use these exact strings where applicable.

## Hero

```text
AI Bracket War Room 2026 — One score in. Every consequence out.
```

Supporting copy:

```text
Load a demo scenario, recalculate the War Room, then inspect group movement, third-place pressure, bracket impact, AI Scout cards, and private Friends League swing.
```

Safety copy:

```text
Unofficial fan-made planner. No gambling, no official marks, no affiliation with tournament organizers, teams, sponsors, broadcasters, or official platforms.
```

## Stats Row

```text
104 Matches
Complete tournament planner

12 Groups
Expanded format tracker

156 AI Scout Cards
Match Pressure · Key Matchup · Bracket Impact

24 Exports
Friends League + scenario packs
```

## Primary Rail

```text
1 · Load Demo Scenario
2 · Recalculate War Room
3 · Review Ripple Effects
Open AI Scout
Open Friends League
```

## Ripple Cards

```text
01 Match Center
Runtime score and selected match context updated.

02 Groups
Group rows recalculated from the scenario.

03 Third-place pool
Contenders ranked for knockout slots.

04 Bracket
Bracket preview redrawn after group movement.

05 AI Scout
Pressure, key matchup, and bracket impact cards refreshed.

06 Friends League
Private league rows ready for scoring/export.
```

## AI Scout Cards

```text
Match Pressure
Reads score state, group stakes, and urgency for the selected fixture.

Key Matchup
Highlights squad balance, depth, and tactical mismatch notes.

Bracket Impact
Shows how one result changes knockout path and Friends League swing.
```

## Premium CTA

```text
Unlock Premium Matchday Pack — $9
```

---

# SECTION 4 — Required Code Changes

## 4A. Add helper escape alias if missing

If `_pmw_escape` does not exist, add:

```python
def _pmw_escape(value: object) -> str:
    return escape(str(value if value is not None else ""))
```

If `_pmw_safe` already exists and is used consistently, using `_pmw_safe` is acceptable. Do not create duplicate helpers unnecessarily.

## 4B. Add Runtime Snapshot Helper If Missing

Add near other PMW helpers:

```python
def _pmw_runtime_snapshot(state: dict | None) -> dict:
    state = state or {}
    runtime = state.get("runtime_matches", pd.DataFrame())
    summary = state.get("runtime_summary") or {}
    scoreline = "Demo scenario ready"
    status = "Ready"
    source = "verified cache"

    if isinstance(runtime, pd.DataFrame) and not runtime.empty:
        completed = runtime[runtime.get("is_completed", pd.Series([False] * len(runtime))).astype(bool)]
        row = completed.head(1).iloc[0] if not completed.empty else runtime.head(1).iloc[0]
        try:
            scoreline = _scoreline_label(row)
        except Exception:
            home = _display_team(row.get("home", "Team A"))
            away = _display_team(row.get("away", "Team B"))
            scoreline = f"{home} vs {away}"
        status = str(row.get("status") or ("FT" if bool(row.get("is_completed")) else "Scheduled"))
        source = str(row.get("result_source") or "verified cache")

    return {
        "scoreline": scoreline,
        "status": status,
        "source": source,
        "completed": summary.get("completed_matches_count", 0),
        "live_count": summary.get("live_matches_count", 0),
        "next_match": summary.get("next_match", "Next match ready"),
    }
```

Adjust if current code already has a better equivalent.

## 4C. Add `_pmw_ripple_review_html`

Add near `_pmw_ai_scout_cards_html`, `build_ai_scout_output`, or other premium HTML helpers.

```python
def _pmw_ripple_review_html(
    state: dict | None,
    groups: pd.DataFrame | None,
    thirds: pd.DataFrame | None,
    bracket: dict | None,
    friends: pd.DataFrame | None,
) -> str:
    snap = _pmw_runtime_snapshot(state)
    group_count = 0 if groups is None or groups.empty else len(groups)
    third_count = 0 if thirds is None or thirds.empty else len(thirds)
    friends_count = 0 if friends is None or friends.empty else len(friends)
    bracket_status = "Bracket preview redrawn" if bracket else "Bracket preview ready"

    return f"""
    <section class="pmw-ripple-board" aria-label="Scenario ripple effects">
      <div class="pmw-card-kicker">One-click ripple effects</div>
      <h2>Demo scenario recalculated across the whole War Room.</h2>
      <p>
        Selected/latest match: <strong>{_pmw_safe(snap["scoreline"])}</strong>
        · Status: {_pmw_safe(snap["status"])}
        · Source: {_pmw_safe(snap["source"])}
      </p>

      <div class="pmw-ripple-grid">
        <article class="pmw-ripple-card lime">
          <span>01</span>
          <strong>Match Center</strong>
          <p>Runtime score and selected match context updated.</p>
        </article>

        <article class="pmw-ripple-card cyan">
          <span>02</span>
          <strong>Groups</strong>
          <p>{group_count} group rows recalculated from the scenario.</p>
        </article>

        <article class="pmw-ripple-card cyan">
          <span>03</span>
          <strong>Third-place pool</strong>
          <p>{third_count} contenders ranked for knockout slots.</p>
        </article>

        <article class="pmw-ripple-card amber">
          <span>04</span>
          <strong>Bracket</strong>
          <p>{_pmw_safe(bracket_status)} after group movement.</p>
        </article>

        <article class="pmw-ripple-card cyan">
          <span>05</span>
          <strong>AI Scout</strong>
          <p>Pressure, key matchup, and bracket impact cards refreshed.</p>
        </article>

        <article class="pmw-ripple-card amber">
          <span>06</span>
          <strong>Friends League</strong>
          <p>{friends_count} private league rows ready for scoring/export.</p>
        </article>
      </div>
    </section>
    """
```

## 4D. Extend `compute_outputs` or `_ui_payload`

Current likely `_ui_payload` shape:

```python
return (
    state,
    matches,
    planner_filter_html,
    groups,
    group_tracker_html,
    thirds,
    third_places_html,
    bracket,
    bracket_html,
    friends,
    friends_html,
    dashboard_html,
    runtime/status html,
    ai_scout_html,
    impact_panel_html,
    google_sheet_control_panel,
)
```

Required new shape:

```python
return (
    state,
    matches,
    planner_filter_html,
    groups,
    group_tracker_html,
    thirds,
    third_places_html,
    bracket,
    bracket_html,
    friends,
    friends_html,
    dashboard_html,
    runtime/status html,
    ai_scout_html,
    impact_panel_html,
    ripple_review_html,
    google_sheet_control_panel,
)
```

Add:

```python
ripple_html = _pmw_ripple_review_html(
    state=state,
    groups=groups,
    thirds=thirds,
    bracket=bracket,
    friends=friends,
)
```

Then insert `ripple_html` immediately before `google_sheet_control_html(state)`.

After this, update **every outputs list** that uses `_ui_payload` to include `ripple_review_html` before `google_sheet_control_panel`.

Search these bindings:

```text
public_load_demo_button.click
recalc_button.click
refresh_live_button.click
pull_sheet_button.click
pull_sheet_tab_button.click
load_demo_button.click
random_outcomes_button.click
clear_edits_button.click
ask_ai_scout_button.click
open_friends_button.click
ask_ai_scout_tab_button.click
score_friends_button.click
view_full_table_button.click
view_full_standings_button.click
view_bracket_button.click
```

Do not leave any binding with old output length.

## 4E. Replace Public Action Rail

Find the public row where Refresh Runtime / Pull Google Sheet / Load Demo / Recalculate buttons appear.

Replace public rail with:

```python
with gr.Row(elem_classes=["product-button-row", "pmw-action-rail", "pmw-happy-path-rail"]):
    public_load_demo_button = gr.Button(
        "1 · Load Demo Scenario",
        variant="primary",
        elem_classes=["pmw-action-button", "pmw-demo-primary"],
    )

    recalc_button = gr.Button(
        "2 · Recalculate War Room",
        variant="primary",
        elem_classes=["pmw-action-button", "pmw-impact-primary"],
    )

    open_ripple_button = gr.Button(
        "3 · Review Ripple Effects",
        variant="secondary",
        elem_classes=["pmw-action-button"],
    )

    ask_ai_scout_button = gr.Button(
        "Open AI Scout",
        variant="secondary",
        elem_classes=["pmw-action-button"],
    )

    open_friends_button = gr.Button(
        "Open Friends League",
        variant="secondary",
        elem_classes=["pmw-action-button"],
    )
```

Do **not** delete Refresh Runtime or Pull Google Sheet. Move them into Operator Tools.

## 4F. Add Ripple Review Component

Immediately after the main dashboard/impact components, add:

```python
ripple_review_html = gr.HTML(value="", visible=True)
```

If the app has `impact_panel_html`, place `ripple_review_html` directly after it.

If `visible=False` causes Gradio update complexity, keep it `visible=True` with empty initial content. Do not over-engineer visibility.

## 4G. Add Open Ripple Binding

Add:

```python
def open_ripple_review_ui_outputs(state: dict | None, matches: pd.DataFrame | None = None):
    payload = list(_ui_payload(compute_outputs(_ensure_workbook_state(state), matches), "Review Ripple Effects"))
    return tuple(payload)
```

Bind `open_ripple_button.click(...)` to the same shared outputs list as Recalculate.

## 4H. Move Operator Controls Into Accordion

Create one hidden admin area:

```python
with gr.Accordion("Operator Tools", open=False, elem_classes=["pmw-operator-tools"]):
    gr.Markdown(
        "Runtime provider, Google Sheet override, and legacy QA controls. Hidden from the main fan/judge path."
    )

    with gr.Row(elem_classes=["product-button-row"]):
        refresh_live_button = gr.Button(
            "Refresh Runtime",
            variant="secondary",
            elem_classes=["pmw-action-button"],
        )
        pull_sheet_button = gr.Button(
            "Pull Google Sheet",
            variant="secondary",
            elem_classes=["pmw-action-button"],
        )
        pull_sheet_tab_button = gr.Button(
            "Pull Google Sheet from Operator Tools",
            variant="secondary",
        )

    google_sheet_control_panel = gr.HTML(value=google_sheet_control_html())

    with gr.Accordion("Legacy / Debug Surface", open=False):
        # Move previous Judge QA / Debug / legacy surfaces here.
        # Keep existing components and handlers where possible.
```

Important:
- If `google_sheet_control_panel` already exists, do not duplicate it.
- Move its component definition into Operator Tools, but keep it in the shared output tuple.
- If moving component definition causes scope issues, define it in the same outer scope but visually place it inside Operator Tools.

Top-level tabs should be product modules only:
- Match Center
- Groups
- 3RD-PLACE RANKING
- Bracket
- AI Scout Cards
- Private Friends League
- Premium

Google Sheet and Judge QA should not be top-level public tabs.

## 4I. Update AI Scout Labels

Search for these legacy labels and replace:

```text
Match Signal → Match Pressure
Squad Lens → Key Matchup
League Swing → Bracket Impact
```

Also update descriptive copy:

```python
cards = [
    ("Match Pressure", "Reads score state, group stakes, and urgency for the selected fixture.", completed_pct, "Free"),
    ("Key Matchup", "Highlights squad balance, depth, and tactical mismatch notes.", source_pct, "Premium"),
    ("Bracket Impact", "Shows how one result changes knockout path and Friends League swing.", league_pct, "Premium"),
]
```

If there is no `cards = [...]` array, update the equivalent HTML/cards manually.

## 4J. Update Stats Row

Search for any first-screen stat array like:

```python
("Fixtures", ...)
("Completed", ...)
("Live now", ...)
("Next", ...)
```

In the hero/first-screen shell only, replace with exact product stats:

```python
stats = [
    ("Matches", "104", "Complete tournament planner"),
    ("Groups", "12", "Expanded format tracker"),
    ("AI Scout Cards", "156", "Match Pressure · Key Matchup · Bracket Impact"),
    ("Exports", "24", "Friends League + scenario packs"),
]
```

Visible labels must render as:

```text
104 Matches
12 Groups
156 AI Scout Cards
24 Exports
```

Do not remove runtime stats from lower/status modules if they are useful. Only ensure the first screen uses the exact product stats.

## 4K. Add Strong Hero CTA Strip

Inside `_premium_matchday_war_room_shell_html` or equivalent hero function, add CTA row directly under subtitle/copy:

```html
<div class="pmw-hero-actions" aria-label="Primary actions">
  <a class="pmw-action primary" href="{_pmw_safe(GUMROAD_PREMIUM_URL)}" target="_blank" rel="noopener">
    Unlock Premium Matchday Pack — $9
  </a>
  <a class="pmw-action secondary" href="#match-center">Open Match Center</a>
  <a class="pmw-action secondary" href="#ai-scout">Open AI Scout</a>
  <a class="pmw-action secondary" href="#premium">Open Premium</a>
</div>
```

If anchors do not map perfectly to Gradio tabs, they are still acceptable as visual CTA/navigation hints. Do not break app behavior for anchor perfection.

---

# SECTION 5 — Final CSS Override

Append this CSS as the **last** block in `gr.Blocks(css=...)`.

If a final `PHASE_141_PIXEL_PERFECT_PREMIUM_UNIFIED_CSS` already exists, merge this into it and ensure it is last.

```python
PHASE_141_PIXEL_PERFECT_PREMIUM_UNIFIED_CSS = """
/* PHASE 1.41 — final happy-path + pixel-perfect premium command center */
:root {
  --pmw-bg: #071018;
  --pmw-bg-2: #0B1320;
  --pmw-panel: rgba(15, 23, 42, 0.78);
  --pmw-panel-2: rgba(2, 6, 23, 0.70);
  --pmw-line: rgba(148, 163, 184, 0.18);
  --pmw-text: #F8FAFC;
  --pmw-muted: #A9B8C9;
  --pmw-dim: #7D8DA4;
  --pmw-neon: #A7FF00;
  --pmw-gold: #FFD166;
  --pmw-cyan: #35D6E8;
  --pmw-rose: #FB7185;
}

.gradio-container {
  background:
    radial-gradient(circle at 18% 0%, rgba(53,214,232,.18), transparent 32%),
    radial-gradient(circle at 82% 8%, rgba(167,255,0,.12), transparent 28%),
    linear-gradient(180deg, var(--pmw-bg), var(--pmw-bg-2)) !important;
  color: var(--pmw-text) !important;
}

.gradio-container .block,
.gradio-container .form,
.gradio-container .panel,
.gradio-container .contain,
.gradio-container .wrap,
.gradio-container .tabitem,
.gradio-container .gradio-tabs,
.gradio-container .gradio-tabitem {
  background: transparent !important;
  border-color: rgba(148,163,184,.12) !important;
  box-shadow: none !important;
}

.pmw-card,
.pmw-final-card,
.pmw-final-stat,
.sport-card,
.app-card,
.card-shell,
.price-card,
.phase-140-score-card,
.premium-pricing-grid article,
.pmw-ripple-card,
.pmw-final-side,
.pmw-final-data,
.pmw-action-card,
.pmw-group-card,
.pmw-lane {
  border-radius: 24px !important;
  border: 1px solid rgba(148,163,184,.18) !important;
  background:
    linear-gradient(180deg, rgba(15,23,42,.78), rgba(2,6,23,.64)) !important;
  color: #F8FAFC !important;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.055),
    0 18px 60px rgba(0,0,0,.22) !important;
  backdrop-filter: blur(18px) !important;
}

.pmw-happy-path-rail {
  position: sticky !important;
  top: 8px !important;
  z-index: 20 !important;
  border: 1px solid rgba(167,255,0,.28) !important;
  border-radius: 28px !important;
  padding: 12px !important;
  background:
    radial-gradient(circle at 12% 0%, rgba(167,255,0,.16), transparent 32%),
    linear-gradient(180deg, rgba(7,16,24,.96), rgba(11,19,32,.92)) !important;
  box-shadow: 0 18px 70px rgba(0,0,0,.36), 0 0 30px rgba(167,255,0,.10) !important;
}

.gradio-container button,
.gradio-container .gr-button,
.gradio-container a[role="button"],
.gradio-container .premium-button,
.gradio-container .pmw-action,
.gradio-container .pmw-action-button,
.pmw-final-cta,
.pmw-cta {
  border-radius: 999px !important;
  overflow: hidden !important;
  background-clip: padding-box !important;
  min-height: 48px !important;
  font-weight: 950 !important;
}

.pmw-demo-primary button,
.pmw-impact-primary button {
  min-height: 58px !important;
  font-size: 15px !important;
  letter-spacing: .01em !important;
}

.pmw-demo-primary button {
  background: linear-gradient(135deg, #A7FF00, #35D6E8) !important;
  color: #061018 !important;
  border: 0 !important;
  box-shadow: 0 18px 44px rgba(167,255,0,.18) !important;
}

.pmw-impact-primary button {
  background: linear-gradient(135deg, #35D6E8, #FFD166) !important;
  color: #061018 !important;
  border: 0 !important;
  box-shadow: 0 18px 44px rgba(53,214,232,.15) !important;
}

.pmw-action.primary,
.pmw-final-cta.primary,
.pmw-cta.primary,
.premium-button.primary {
  background: linear-gradient(135deg, #A7FF00, #FFD166) !important;
  color: #061018 !important;
  border: 0 !important;
  box-shadow: 0 18px 44px rgba(167,255,0,.20) !important;
}

.pmw-action.secondary,
.pmw-final-cta.secondary,
.pmw-cta.secondary,
.premium-button.secondary {
  background: rgba(53,214,232,.10) !important;
  color: #E6FBFF !important;
  border: 1px solid rgba(53,214,232,.25) !important;
  box-shadow: none !important;
}

.pmw-card-kicker,
.pmw-kicker,
.module-kicker,
.pmw-final-kicker {
  color: #DDE7F3 !important;
  background: rgba(255,255,255,.06) !important;
  border: 1px solid rgba(148,163,184,.16) !important;
  box-shadow: none !important;
}

.pmw-ripple-board {
  margin: 18px auto !important;
  padding: 22px !important;
  max-width: 1480px !important;
  border-radius: 28px !important;
  border: 1px solid rgba(53,214,232,.24) !important;
  background:
    radial-gradient(circle at 100% 0%, rgba(53,214,232,.12), transparent 30%),
    linear-gradient(180deg, rgba(15,23,42,.92), rgba(2,6,23,.88)) !important;
}

.pmw-ripple-board h2 {
  color: #f8fafc !important;
  font-size: clamp(26px, 3vw, 44px) !important;
  margin: 6px 0 10px !important;
}

.pmw-ripple-grid {
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  gap: 14px !important;
  margin-top: 16px !important;
}

.pmw-ripple-card {
  min-height: 150px !important;
  padding: 18px !important;
}

.pmw-ripple-card span {
  display: inline-flex !important;
  width: 34px !important;
  height: 34px !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 999px !important;
  font-weight: 950 !important;
  margin-bottom: 12px !important;
  background: rgba(255,255,255,.08) !important;
  color: #F8FAFC !important;
}

.pmw-ripple-card strong {
  display: block !important;
  color: #f8fafc !important;
  font-size: 18px !important;
}

.pmw-ripple-card p {
  color: #cbd5e1 !important;
  margin: 8px 0 0 !important;
}

.pmw-ripple-card.lime {
  border-color: rgba(167,255,0,.34) !important;
  box-shadow: 0 0 28px rgba(167,255,0,.08) !important;
}

.pmw-ripple-card.cyan {
  border-color: rgba(53,214,232,.32) !important;
  box-shadow: 0 0 28px rgba(53,214,232,.07) !important;
}

.pmw-ripple-card.amber {
  border-color: rgba(255,209,102,.34) !important;
  box-shadow: 0 0 28px rgba(255,209,102,.07) !important;
}

.pmw-operator-tools {
  max-width: 1480px !important;
  margin: 18px auto !important;
  opacity: .84 !important;
}

.pmw-operator-tools:hover {
  opacity: 1 !important;
}

.gradio-container table,
.gradio-container .dataframe,
.gradio-container .gradio-dataframe table {
  background: rgba(2,6,23,.72) !important;
  color: #F8FAFC !important;
  border-color: rgba(148,163,184,.14) !important;
}

.gradio-container th {
  background: rgba(53,214,232,.16) !important;
  color: #E6FBFF !important;
  border-color: rgba(148,163,184,.14) !important;
}

.gradio-container td {
  background: rgba(2,6,23,.54) !important;
  color: #F8FAFC !important;
  border-color: rgba(148,163,184,.12) !important;
}

@media (max-width: 760px) {
  .pmw-ripple-grid {
    grid-template-columns: 1fr !important;
  }

  .pmw-happy-path-rail {
    position: static !important;
  }

  .pmw-ripple-board {
    border-radius: 20px !important;
    padding: 16px !important;
  }

  .pmw-final-stats,
  .pmw-stat-grid,
  .pmw-final-grid,
  .pmw-final-actions,
  .premium-pricing-grid {
    grid-template-columns: 1fr !important;
  }

  .pmw-action,
  .pmw-final-cta,
  .pmw-cta,
  .premium-button,
  .gradio-container button {
    width: 100% !important;
  }
}
"""
```

Then ensure Gradio CSS concatenation ends with:

```python
css=(
    PREMIUM_DARK_SPORT_CSS
    + PHASE_126_INTERACTIVE_CSS
    + ...
    + PHASE_141_PIXEL_PERFECT_PREMIUM_UNIFIED_CSS
)
```

The final CSS override must be last.

---

# SECTION 6 — Gradio Binding Output Template

Use one shared list to prevent mismatch.

If there is no shared list, create it after all components are defined:

```python
shared_ui_outputs = [
    workbook_state,
    matches_df,
    planner_filter_html,
    groups_df,
    group_tracker_html,
    third_places_df,
    third_places_html,
    bracket_json,
    bracket_html,
    friends_df,
    friends_html,
    dashboard_html,
    top_checklist_html,
    ai_scout_html,
    impact_panel_html,
    ripple_review_html,
    google_sheet_control_panel,
]
```

Then bind all `_ui_payload` handlers to this same output list.

---

# SECTION 7 — README Patch

If `README.md` exists, add this near the top:

```markdown
## Judge Demo: 45-second path

1. Open the Space.
2. Click **1 · Load Demo Scenario**.
3. Click **2 · Recalculate War Room**.
4. Review **Ripple Effects**: Match Center, Groups, Third-place pool, Bracket, AI Scout, Friends League.
5. Open **AI Scout Cards** and confirm **Match Pressure / Key Matchup / Bracket Impact**.
6. Open **Private Friends League** and score the demo league.
7. Open **Premium** and confirm Free Core vs Premium Matchday Pack / Ultimate / Source upgrade path.

Expected visible markers:
- **104 Matches**
- **12 Groups**
- **156 AI Scout Cards**
- **24 Exports**
- Verified Cache Mode
- Unofficial fan-made planner
- No gambling
- No official marks or affiliation
```

Remove or demote duplicate legacy judge paths if they conflict.

---

# SECTION 8 — QA Commands

Run these commands from repo root:

```bash
cd /workspaces/wc2026_planner

python -m py_compile app_pixel_perfect_premium.py
```

If the actual HF entrypoint is `app.py`, also run:

```bash
python -m py_compile app.py
```

If test scripts exist, run:

```bash
python scripts/run_hackathon_smoke_tests.py
```

Manual local QA:

```text
[ ] First screen shows premium stadium hero.
[ ] Stats row shows 104 / 12 / 156 / 24 above fold.
[ ] Public path starts with “1 · Load Demo Scenario”.
[ ] Second button says “2 · Recalculate War Room”.
[ ] “3 · Review Ripple Effects” is visible.
[ ] Load Demo updates visible app state.
[ ] Recalculate updates Match Center, Groups, Third-place, Bracket, AI Scout, Friends League.
[ ] Ripple Review cards are visible after click.
[ ] Refresh Runtime is not in public first-screen rail.
[ ] Pull Google Sheet is only inside Operator Tools.
[ ] Google Sheet control panel is not a top-level tab.
[ ] Judge QA / Debug is not a top-level tab.
[ ] AI Scout cards say Match Pressure / Key Matchup / Bracket Impact.
[ ] Friends League opens and scores without page reload.
[ ] Premium CTA says Unlock Premium Matchday Pack — $9.
[ ] Mobile 375px: CTAs full-width, stats readable.
[ ] No default white Gradio cards/panels dominate the UI.
[ ] No gambling language.
[ ] No official affiliation claims.
```

---

# SECTION 9 — Commit Commands

After successful QA:

```bash
git status --short
git diff --stat
git diff -- app_pixel_perfect_premium.py app.py README.md | head -260

git add app_pixel_perfect_premium.py app.py README.md
git commit -m "Phase 1.41 FINAL happy-path pixel-perfect product shell"
git push origin main
```

If only one file changed, stage only that file.

If HF remote is separate and configured:

```bash
git push hf main
```

Then refresh the Space and run the judge demo.

---

# SECTION 10 — Final Output Required From Codex

When finished, output:

```text
FINAL PATCH SUMMARY
- Files changed:
- Core UI changes:
- Output tuple changes:
- Operator Tools demotion:
- CSS final override:
- README changes:

QA RESULT
[PASS/FAIL] py_compile
[PASS/FAIL] smoke tests
[PASS/FAIL] manual judge path
[PASS/FAIL] mobile visual check

FINAL GATE
FINAL — ready for HF push
```

If any check fails, stop and report the exact file/line/error and the minimal patch needed.

---

# SECTION 11 — 60-Second Demo Script After Patch

Use this for final recording/submission:

```text
0–10s:
Show hero: AI Bracket War Room 2026 — One score in. Every consequence out.
Point to 104 Matches / 12 Groups / 156 AI Scout Cards / 24 Exports.

10–20s:
Click 1 · Load Demo Scenario.
Explain: the app loads a judge-safe tournament scenario without credentials.

20–30s:
Click 2 · Recalculate War Room.
Show Ripple Review: Match Center, Groups, Third-place pool, Bracket, AI Scout, Friends League.

30–40s:
Open AI Scout Cards.
Show Match Pressure / Key Matchup / Bracket Impact.

40–50s:
Open Private Friends League.
Click score or show leaderboard/export preview.

50–60s:
Open Premium.
Show Premium Matchday Pack / Ultimate / Source path.
Say: unofficial fan-made, no gambling, no official marks, fully judgeable free core.
```

---

# SECTION 12 — Success Criteria

The patch is accepted only if the public app now communicates this in under 10 seconds:

```text
Change one score.
Recalculate the War Room.
See every consequence:
Groups, third-place pressure, bracket path, AI Scout, Friends League.
Upgrade to Premium exports if you want the full matchday pack.
```

No extra explanation should be needed for a hackathon judge.

Process this file and apply directly to `app_pixel_perfect_premium.py` now.
