# AI Bracket War Room 2026 - Build Small App

Phase 1.14 adds a lightweight Gradio app layer on top of the hackathon-ready Spreadsheet Engine XLSX.

## Run

```bash
pip install -r requirements.txt
python app.py
```

The app opens a local Gradio interface with these tabs:

- DASHBOARD
- MATCH PLANNER
- GROUP TRACKER
- 3RD-PLACE RANKING
- BRACKET WAR ROOM
- FRIENDS LEAGUE

## Source Workbook

Canonical source:

```text
releases/final/artifacts/03_AI_Bracket_War_Room_2026_Spreadsheet_Engine.xlsx
```

Fallbacks:

```text
FIX6C_STATIC_ANNEXC_HACKATHON_READY.xlsx
assets/AI_Bracket_War_Room_2026_Planner_FIX7.xlsx
```

Canonical sheets:

```text
START_HERE
BRACKET_WAR_ROOM
MATCH_PLANNER
FRIENDS_LEAGUE
AnnexC_495_STATIC
QA_STATIC_CHECK
```

## Build Small Scope

- Load the static offline Spreadsheet Engine XLSX.
- Let users edit match predictions/results in the app.
- Score predictions with a lightweight exact-score / outcome model.
- Compute a basic group table from completed match results.
- Rank third-place teams with a deterministic Build Small ordering.
- Return a JSON bracket fallback when Annex C is loaded but mapping rules are still pending.

This app has no wagering, paid-prediction, or money-staked gameplay features.

## Phase 2 TODOs

- Implement full official-style tie-breaker sequencing.
- Parse Annex C into a complete bracket mapping engine.
- Add richer validation for team/group assignments.
- Persist edited planner state back to a copy of the workbook.
- Add app-level regression tests for editable recalc flows.

## IP Disclaimer

Unofficial fan-made digital download. Not affiliated with or endorsed by FIFA, World Cup, national teams, leagues, clubs, sponsors, broadcasters, or players. No official logos, crests, sponsor marks, player likenesses, or protected tournament emblems are included.
