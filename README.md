---
title: AI Bracket War Room 2026
emoji: 🏟️
colorFrom: blue
colorTo: gray
sdk: gradio
app_file: app.py
pinned: false
---

# WC2026 Matchday No Chaos Planner

Production codebase for a 3-SKU Etsy digital planner system.

## SKU ladder

- Premium: 184-page master GoodNotes bundle, $27.99
- Standard: 144-page derived bundle, $17.99
- Minimal: 84-page condensed tracker, $9.99

## Current phase coverage

Implemented through **Phase 1.13**:

- Phase 1.1: product config
- Phase 1.2: premium blueprint / registry contract
- Phase 1.3: modular rendering engine skeleton
- Phase 1.4: layout geometry contract
- Phase 1.5: renderer shell + smoke test
- Phase 1.6: controlled 184-page skeleton render
- Phase 1.7: global components
- Phase 1.8: core pages 1-9
- Phase 1.9: group trackers + match indexes
- Phase 1.10: dedicated match log template
- Phase 1.11: team + stats pages
- Phase 1.12: party + bingo + office pool pages
- Phase 1.13: sticker catalog + notes/legal + dark notes pages
- Phase 1.14: Build Small hackathon Gradio app foundation over the static Spreadsheet Engine XLSX
- Phase 1.15: deterministic demo scenario, bracket preview cards, and hackathon smoke tests

## Run

```bash
pip install -r requirements.txt
python -m skeleton_tests.run_phase_1_6_skeleton
```

Expected output:

```text
output/premium/phase_1_6_premium_skeleton_184_pages.pdf
output/premium/phase_1_6_skeleton_report.json
```

## Hackathon app

```bash
pip install -r requirements.txt
python app.py
```

The app uses `releases/final/artifacts/03_AI_Bracket_War_Room_2026_Spreadsheet_Engine.xlsx` as the canonical workbook source. Use `Load Demo Scenario` for a fast visible demo, then `Recalculate War Room` after edits. See `HACKATHON_APP_README.md` for tabs, scope, Phase 2 TODOs, and demo notes.

This project is a fan-made planner/tracker. It has no money-staked gameplay or paid-prediction features.

## Judge Demo Flow

AI Bracket War Room 2026 turns a 104-match fan spreadsheet into a live Gradio tournament command center: edit results, recalculate standings, rank third-place teams, map the bracket, update a Friends League, and get a product-safe AI Scout explanation.

1. Open the app.
2. Confirm the blank boot state loads cleanly.
3. Click `Load Demo Scenario`.
4. Show GROUP TRACKER.
5. Show 3RD-PLACE RANKING.
6. Show BRACKET WAR ROOM preview.
7. Show FRIENDS LEAGUE.
8. Show AI Scout status in the dashboard.

## Known Limitations

- Edits are session-local and are not written back to the source workbook.
- The app does not claim a full official tiebreaker engine.
- Annex C mapping is a bracket-planning layer, not an official rules claim.

## Unofficial Fan-Made Disclaimer

Unofficial fan-made digital planner. Not affiliated with or endorsed by FIFA, World Cup, national teams, leagues, clubs, sponsors, broadcasters, or players. No official logos, crests, sponsor marks, player likenesses, or protected tournament emblems are included. No money-staked prediction-market, probability-market, or bookmaking functionality is included.

## IP disclaimer

Unofficial fan-made digital planner. Not affiliated with or endorsed by FIFA, World Cup, national teams, leagues, clubs or players. No official logos, crests or trademarks are included.
