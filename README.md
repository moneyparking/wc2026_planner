---
title: AI Bracket War Room 2026
emoji: ⚽
colorFrom: blue
colorTo: gray
sdk: gradio
sdk_version: 4.44.1
python_version: '3.12'
app_file: app.py
pinned: false
license: mit
short_description: "Fan-made WC2026 scenario planner: predictions, brackets, Friends League, AI Scout, and premium matchday exports."
tags:
  - gradio
  - football
  - sports
  - world-cup
  - bracket
  - predictions
  - hackathon
---
# AI Bracket War Room 2026

Unofficial fan-made 104-match football tournament command center for planning, prediction tracking, private leagues, bracket simulation, and squad-aware scout signals.

Phase 1.30 turns the demo into a production fan app runtime: official fixture seed, optional live score adapter, Google Sheet/manual override control plane, runtime tournament engine, and UI tabs that show source priority.

## One-sentence pitch

Refresh live runtime, pull Google Sheet overrides, load the local demo result, filter the 104-match planner by stage or Group A-L, and watch Group Tracker, Bracket War Room, Friends League, and AI Scout update from runtime scores.

## Phase 1.30 Runtime Sources

Runtime source priority is visible in the app:

```text
Manual override > live provider > static fixture seed
```

- Static fixture seed: `data/wc2026_fixtures.csv`.
- Live score adapter: `src/live_score_adapter.py`.
- Google Sheet control plane: `src/google_sheet_adapter.py`.
- Local override: `data/live_results_override.json` for QA/demo already-played results.

Environment variables:

```bash
LIVE_SCORE_PROVIDER=none
LIVE_SCORE_API_KEY=
LIVE_SCORE_COMPETITION_ID=
GOOGLE_SHEET_ID=
GOOGLE_SERVICE_ACCOUNT_JSON=
GOOGLE_SHEET_ENABLED=false
LIVE_REFRESH_SECONDS=60
```

Supported live providers are `none`, `local_json`, `api_football`, `sportmonks`, and `football_data`. The external providers are safe stubs until endpoint mapping is completed; missing credentials render visible UI warnings instead of stack traces.

## Judge Demo Path

1. Click **Refresh Live Runtime**.
2. Click **Pull Google Sheet**.
3. Click **Load Demo Scenario**.
4. Click **Recalculate War Room**.
5. Review Runtime Status, Match Planner, Group Tracker, Bracket War Room, Friends League, AI Scout, and Google Sheet Control.

## What works now

- 48 teams.
- 12 groups.
- 104 matches.
- Real fixture schedule.
- Squad-aware scout layer.
- 104-match offline tournament state engine.
- Judge demo scenario.
- Runtime recalculation.
- Group standings.
- Third-place ranking.
- Knockout bracket skeleton.
- Friends League fan scoring.
- Unofficial fan-made demo.
- Tournament Impact Panel.
- No paid API key required for the judge demo.
- Runtime Status panel.
- Live score adapter with `local_json` QA/demo mode.
- Google Sheet Control tab explaining manual results, friends picks, league settings, and admin notes.

## 90-second judge verification

1. Open the Hugging Face Space or run the app locally.
2. Confirm the first screen says **Change one result. Watch the tournament path mutate.**
3. Confirm the proof badges show **104-Match Engine**, **Friends League**, **AI Scout Signals**, and **No API Key Required**.
4. Click **Load Judge Demo Scenario**.
5. Edit a score in **MATCH_PLANNER — editable scenario input**.
6. Click **Recalculate War Room**.
7. Confirm **Tournament Impact Panel** shows changed match, before score, after score, group impact, third-place pool impact, bracket slot impact, Friends League impact, and AI Scout summary.
8. Open every tab: Dashboard, Match Planner, Group Tracker, 3rd-Place Ranking, Bracket War Room, Friends League, and AI Scout.

## What is intentionally limited

This is a hackathon vertical slice, not a full production live-score platform. Preview rows are compact judge-readable outputs designed to prove interaction, state flow, recalculation, and downstream scenario impact.

Edits are session-local and are not written back to the source workbook. The app is a planning and demo workflow, not a complete live tournament rules service. Annex C mapping is used as a bracket-planning layer. AI Scout is a lightweight AI-style explanatory layer over deterministic tournament state; it does not use live sports data, external market data, money-staked logic, or real tournament outcome claims.

## Demo Video Script

Use the final 60-second script in `releases/final/DEMO_VIDEO_60_SEC_SCRIPT_PHASE_1_19.md`.

## Demo video / social post

Recommended demo: show the full loop in under 60 seconds. No live sports data, independent fan-made project, no money-staked prediction-market functionality.

## Social Post Copy

Built AI Bracket War Room 2026 for the Hugging Face Build Small Hackathon: an unofficial fan-made Gradio command center over a static 104-match spreadsheet engine. Load a judge scenario, change one result, recalculate groups, rank third-place teams, preview the bracket, compare a Friends League, and review lightweight AI Scout Signals in one narrow vertical slice.

## Local quickstart

```bash
pip install -r requirements.txt
python app.py
python scripts/run_hackathon_smoke_tests.py
python scripts/qa_phase_130_runtime_product.py
```

## Smoke test

```bash
python scripts/run_hackathon_smoke_tests.py
```

Expected result:

```text
HACKATHON_SMOKE_TESTS_PASS
```

## Core files

- `app.py` — Gradio app entry point.
- `requirements.txt` — runtime dependency list.
- `scripts/run_hackathon_smoke_tests.py` — hackathon smoke test.
- `releases/final/artifacts/03_AI_Bracket_War_Room_2026_Spreadsheet_Engine.xlsx` — canonical spreadsheet engine.
- `SPACE_DEPLOYMENT.md` — Hugging Face Space deployment plan.
- `JUDGE_DEMO_SCRIPT.md` — live demo and video script.
- `releases/final/QA_HACKATHON_APP_PHASE_1_16.md` — Phase 1.16 QA record.
- `releases/final/QA_PHASE_1_19_JUDGE_VALUE_UI.md` — Phase 1.19 button/link QA record.
- `releases/final/DEMO_VIDEO_60_SEC_SCRIPT_PHASE_1_19.md` — Phase 1.19 final demo video script.

## Product safety and IP boundary

This is an unofficial fan-made planning demo. It is not affiliated with, endorsed by, or sponsored by FIFA, the FIFA World Cup, host committees, national federations, broadcasters, or sponsors. No official logos, emblems, mascots, player likenesses, or federation crests are used.

This is an unofficial fan-made football tournament planning demo. Not affiliated with FIFA, any football federation, tournament organizer, broadcaster, sponsor, team, or player. It does not include official logos, crests, sponsor marks, player likenesses, protected tournament emblems, money-staked prediction-market functionality, live official predictions, or money-staking functionality.

## Phase 1.28 — Productized User Onboarding + Demo Path Clarity

AI Bracket War Room 2026 is an unofficial fan-made football tournament planning command center for the expanded 48-team format.

### 10-second demo promise

Open the Space and follow the visible 3-step path:

1. Load Demo Scenario / Recalculate War Room.
2. Inspect Match Planner → Group Tracker → Third-Place Ranking → Bracket War Room → Friends League.
3. Select a match for AI Scout, then export the Judge JSON Contract.

### Visible technical proof

- 48 teams
- 12 groups
- 104 matches
- 495 third-place / bracket-combination proof marker
- AI Scout Tactical Slip from selected match context
- Friends League prediction layer
- Judge JSON Contract export proof

### Safety and scope

This is an unofficial fan-made Gradio demo. It has independent fan-made project, no live federation data feed, no protected logos or marks, and no money-staked prediction-market workflow.

### Phase 1.28 QA gates

```bash
python scripts/phase128_marker_harness.py
python -m py_compile app.py
python scripts/run_hackathon_smoke_tests.py
python scripts/judge_ui_walkthrough.py --url https://moneyparking-ai-bracket-war-room-2026.hf.space --timeout 30000
```

Expected markers:

```text
PHASE_1_28_MARKER_HARNESS_PASS
HACKATHON_SMOKE_TESTS_PASS
JUDGE_UI_WALKTHROUGH_PASS
[PASS] Step 7 — Visual contrast audit
```


## Premium Monetization Path

AI Bracket War Room 2026 uses a judge-safe free core with visible premium upgrade paths.

| Tier | Price | Value |
|---|---:|---|
| Free Core | $0 | Runtime demo, 104-match planner, group tracker, third-place ranking, bracket preview, Friends League demo, AI Scout preview |
| Premium Matchday | $9 | Advanced AI Scout cards, export-ready summaries, private league export pack, ad-free planning shell |
| Ultimate Fan Pack | $27 | 184-page GoodNotes/PDF command center, 104 match logs, office-pool kit, printable exports, sticker bundle |
| Source License | $49+ | Deployable Gradio source bundle, templates, private league starter, deployment guide |

Fan-safe boundary: unofficial fan-made planner, no gambling language, no official federation marks, no player likeness dependency, and no paid live-score requirement.
