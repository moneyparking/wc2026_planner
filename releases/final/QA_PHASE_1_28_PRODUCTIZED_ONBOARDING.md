# Phase 1.28 QA — Productized User Onboarding + Demo Path Clarity

## Objective

Make AI Bracket War Room 2026 understandable to hackathon judges and normal users in under 10 seconds without changing the core engine.

## Scope

Changed scope is intentionally additive:
- First-screen onboarding card.
- KPI strip: 48 teams, 12 groups, 104 matches, 495 combos.
- 3-step demo path.
- Clear unofficial fan-made disclaimer.
- Clear no live official data / no betting workflow safety note.
- Marker extraction harness.
- README release note alignment.

## Preserved invariants

- Canonical working loop remains: Load Demo Scenario → Recalculate War Room → Match Planner → Group Tracker → Third-Place Ranking → Bracket War Room → Friends League → AI Scout → Export / Submission Proof.
- Phase 1.26T contrast selectors remain locked.
- Existing smoke tests remain.
- Existing judge UI walkthrough remains.
- No official affiliation claim.
- No betting, odds, sportsbook, wagering, or gambling language.

## Required acceptance markers

- PHASE_1_28_MARKER_HARNESS_PASS
- HACKATHON_SMOKE_TESTS_PASS
- JUDGE_UI_WALKTHROUGH_PASS
- [PASS] Step 7 — Visual contrast audit

## Manual QA

- Product name visible above the fold.
- Value proposition visible above the fold.
- Unofficial fan-made positioning visible.
- One primary CTA is obvious.
- KPI strip visible.
- 3-step demo path visible.
- Status starts in Ready state.
- Tables remain readable.
- AI Scout row-select still works.
- JSON export path remains clear.
