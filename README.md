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

Unofficial fan-made football tournament planning demo built as a Gradio command center over a 104-match spreadsheet engine.

## What the demo shows

AI Bracket War Room 2026 turns a fan tournament workbook into a visible app loop: match result input -> runtime recalculation -> group tracker -> third-place ranking -> bracket JSON/HTML preview -> Friends League -> AI Scout.

## How to run the judge demo

1. Open the Hugging Face Space or run the app locally.
2. Confirm the blank boot state loads without requiring an uploaded workbook.
3. Open MATCH PLANNER.
4. Click Load Demo Scenario.
5. Click Recalculate War Room after edits.
6. Show GROUP TRACKER.
7. Show 3RD-PLACE RANKING.
8. Show BRACKET WAR ROOM JSON and HTML preview.
9. Show FRIENDS LEAGUE.
10. Show AI Scout text in the dashboard.

## Local quickstart

pip install -r requirements.txt
python app.py
python scripts/run_hackathon_smoke_tests.py

## Smoke test

python scripts/run_hackathon_smoke_tests.py

Expected result:

HACKATHON_SMOKE_TESTS_PASS

## Core files

- app.py — Gradio app entry point.
- requirements.txt — runtime dependency list.
- scripts/run_hackathon_smoke_tests.py — hackathon smoke test.
- releases/final/artifacts/03_AI_Bracket_War_Room_2026_Spreadsheet_Engine.xlsx — canonical spreadsheet engine.
- SPACE_DEPLOYMENT.md — Hugging Face Space deployment plan.
- JUDGE_DEMO_SCRIPT.md — live demo and video script.
- releases/final/QA_HACKATHON_APP_PHASE_1_16.md — Phase 1.16 QA record.

## Product safety and IP boundary

This is an unofficial fan-made football tournament planning demo. It is not affiliated with or endorsed by FIFA, the World Cup, national teams, leagues, clubs, sponsors, broadcasters, or players. It does not include official logos, crests, sponsor marks, player likenesses, protected tournament emblems, or money-staked prediction-market functionality.

## Known limitations

- Edits are session-local and are not written back to the source workbook.
- The app is a planning and demo workflow, not a complete tournament rules engine.
- Annex C mapping is used as a bracket-planning layer.
- AI Scout output is product-safe explanatory text, not an external live-data integration.
