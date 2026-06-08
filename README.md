---
title: AI Bracket War Room 2026
emoji: 🏟️
colorFrom: blue
colorTo: gray
sdk: gradio
app_file: app.py
pinned: false
---

# AI Bracket War Room 2026

AI Bracket War Room 2026 is a small-model-safe Gradio command center for testing football tournament scenarios and seeing how one result changes groups, third-place qualification, bracket paths, Friends League outcomes, and AI Scout signals.

## One-line pitch

Change one result, filter the 104-match planner by stage or Group A-L, generate a full 104-match random stress scenario, and watch Group Tracker, 3rd-Place Ranking, Bracket War Room, Friends League, and AI Scout update.

## Judge Demo Path

1. Click **Load Judge Demo Scenario**.
2. Change one match result.
3. Click **Recalculate War Room**.
4. Review **Tournament Impact Panel**.
5. Review **Group Tracker**.
6. Review **3rd-Place Ranking**.
7. Review **Bracket War Room**.
8. Review **Friends League**.
9. Review **AI Scout Signals**.

## What works now

- 104-match offline tournament state engine.
- Judge demo scenario.
- Runtime recalculation.
- Group tracker preview.
- Third-place ranking preview.
- Bracket preview.
- Friends League preview.
- AI Scout scenario signals.
- Tournament Impact Panel.
- No paid API key required for the judge demo.

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

Edits are session-local and are not written back to the source workbook. The app is a planning and demo workflow, not a complete live tournament rules service. Annex C mapping is used as a bracket-planning layer. AI Scout is a lightweight AI-style explanatory layer over deterministic tournament state; it does not use live sports data, external market data, betting logic, or real tournament outcome claims.

## Demo Video Script

Use the final 60-second script in `releases/final/DEMO_VIDEO_60_SEC_SCRIPT_PHASE_1_19.md`.

## Demo video / social post

Recommended demo: show the full loop in under 60 seconds. No live sports data, no official affiliation, no gambling or prediction-market functionality.

## Social Post Copy

Built AI Bracket War Room 2026 for the Hugging Face Build Small Hackathon: an unofficial fan-made Gradio command center over a static 104-match spreadsheet engine. Load a judge scenario, change one result, recalculate groups, rank third-place teams, preview the bracket, compare a Friends League, and review lightweight AI Scout Signals in one narrow vertical slice.

## Local quickstart

```bash
pip install -r requirements.txt
python app.py
python scripts/run_hackathon_smoke_tests.py
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

This is an unofficial fan-made football tournament planning demo. Not affiliated with FIFA, any football federation, tournament organizer, broadcaster, sponsor, team, or player. It does not include official logos, crests, sponsor marks, player likenesses, protected tournament emblems, money-staked prediction-market functionality, live official predictions, or odds-style wagering functionality.
