# AI Bracket War Room 2026 - Build Small App

Phase 1.15 adds a lightweight Gradio app layer and deterministic demo scenario on top of the hackathon-ready Spreadsheet Engine XLSX.

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

## Controls

- `Load Demo Scenario`: fills generic group-stage teams, predictions, and results so judges can immediately see group standings, third-place ranking, bracket JSON, bracket preview, and Friends League state update.
- `Recalculate War Room`: recomputes the app from the current editable MATCH PLANNER table.

The blank workbook remains valid. If no `Result` values are completed, the app shows empty schema-valid group and third-place tables plus a neutral bracket waiting state.

## 90-Second Demo Flow

1. Start the app with `python app.py`.
2. Show DASHBOARD to confirm the workbook, 104 matches, and 495 Annex C rows loaded.
3. Click `Load Demo Scenario`.
4. Open GROUP TRACKER and show non-empty standings.
5. Open 3RD-PLACE RANKING and show the qualified third-place groups.
6. Open BRACKET WAR ROOM and show the canonical JSON plus lightweight bracket cards / mapping-pending state.
7. Edit one result in MATCH PLANNER, click `Recalculate War Room`, and show the affected tables update.

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
- Load a deterministic demo scenario for a fast judge walkthrough.

This app has no money-staked gameplay, paid-prediction, or prize-market features.

## Phase 2 TODOs

- Implement full tournament tie-breaker sequencing.
- Parse Annex C into a complete bracket mapping engine.
- Add richer validation for team/group assignments.
- Persist edited planner state back to a copy of the workbook.
- Add app-level regression tests for editable recalc flows.
- Parse Annex C into complete Round of 32 cards.

## IP Disclaimer

Unofficial fan-made digital download. Not affiliated with or endorsed by FIFA, World Cup, national teams, leagues, clubs, sponsors, broadcasters, or players. No official logos, crests, sponsor marks, player likenesses, or protected tournament emblems are included.
