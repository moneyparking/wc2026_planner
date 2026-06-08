# QA Phase 1.19 — Judge Value UI

Phase marker: `PHASE_1_19_JUDGE_VALUE_UI`

## Scope

This QA pass verifies the judge-visible causal loop:

`Load Judge Demo Scenario → Change one match result → Recalculate War Room → Tournament Impact Panel → AI Scout Signals → Friends League`

The app remains an unofficial fan-made football tournament planning demo over an offline 104-match spreadsheet engine. No official marks, live scores, betting odds, or paid model/API claims are exposed.

## Button QA Table

| Control Label | Location | Expected Action | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|
| Load Judge Demo Scenario | Top command controls | Applies deterministic demo scenario and populates matches, groups, third-place table, bracket preview, Friends League, AI Scout, and Impact Panel | Callback `load_demo_scenario_outputs` returns non-empty downstream outputs | Pass | Primary CTA, judge-visible |
| Recalculate War Room | Top command controls | Recomputes tournament state from current Match Planner rows | Callback `compute_outputs` refreshes state, Match Planner, Group Tracker, 3rd-Place Ranking, Bracket War Room, Friends League, Dashboard, AI Scout, and Impact Panel | Pass | Secondary CTA, no silent no-op |
| Reset Demo State | Top command controls | Not present | Not shown | Pass | Removed/not added because no stable existing reset callback was required |
| Export/download button | App UI | Not present | Not shown | Pass | No unsupported export promise exposed |
| Sample scenario button | App UI | Load Judge Demo Scenario is the supported sample scenario | Works through deterministic demo callback | Pass | No duplicate sample button |
| DASHBOARD tab | Gradio tabs | Shows status, judge path, workbook counts, and phase marker | Non-empty dashboard HTML after load/recalculate | Pass | Explains why the loop matters |
| MATCH PLANNER tab | Gradio tabs | Shows editable match scenario input | Editable dataframe with explicit “Change this result” guidance | Pass | Recalculation requirement is visible |
| GROUP TRACKER tab | Gradio tabs | Shows recalculated group table | Non-empty dataframe after demo scenario | Pass | Context: group order changes after recalculation |
| 3RD-PLACE RANKING tab | Gradio tabs | Shows recalculated third-place ranking preview | Non-empty dataframe after demo scenario | Pass | Context: important in 48-team format |
| BRACKET WAR ROOM tab | Gradio tabs | Shows bracket summary/preview without exposing raw bracket JSON as the judge path | Non-empty bracket HTML/state after recalculation | Pass | Converts standings into knockout preview slots |
| FRIENDS LEAGUE tab | Gradio tabs | Shows private league leaderboard impact | Non-empty Friends League dataframe after demo scenario | Pass | Private picks gain/lose after scenario changes |
| AI SCOUT tab | Gradio tabs | Shows lightweight AI-style scenario signal cards | Non-empty AI Scout HTML after load/recalculate | Pass | No paid API or large-model claim |
| Internal README/Space link | README/Core files | Documents supporting files and Space metadata | Markdown references retained | Pass | No broken in-app hyperlink exposed |
| Social/demo link | App UI | Not present | Not shown | Pass | No dead social/demo link exposed |
| Modal-related button | App UI | Not present | Not shown | Pass | Modal is not implemented and not advertised |

## QA Rules Checked

- No button silently does nothing.
- No tab is intentionally empty.
- No link exposed in the app UI is broken.
- No outdated `PHASE_1_18H_HONEST_PREVIEW_LABELS` marker remains in first-screen copy.
- No control implies future functionality that does not work now.
- Modal is not implemented and no Modal button is shown.
- Google Sheet/spreadsheet is positioned as the backend offline engine, not as a visible product dependency.

## Manual Judge Path

1. Open Space cold.
2. Confirm first screen contains: `Change one result`, `104-match`, `AI Scout`, `Friends League`, and `No API Key Required`.
3. Click **Load Judge Demo Scenario**.
4. Edit one result in **MATCH_PLANNER — editable scenario input**.
5. Click **Recalculate War Room**.
6. Inspect **Tournament Impact Panel**.
7. Inspect **AI Scout Signals**.
8. Inspect **Friends League**.
9. Open every tab and confirm non-empty output.

## Smoke Test

Expected command:

```bash
python scripts/run_hackathon_smoke_tests.py
```

Expected final output:

```text
HACKATHON_SMOKE_TESTS_PASS
```
