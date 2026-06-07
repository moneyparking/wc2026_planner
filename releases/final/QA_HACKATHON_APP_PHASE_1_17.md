# QA Report — Phase 1.17

## Phase summary

Phase 1.17 adds CI-backed hackathon smoke testing and prepares the project for live Hugging Face Space verification. It does not rewrite app logic.

## Base state

Phase 1.16 is merged into main.

## Changed files

- .github/workflows/hackathon-smoke.yml
- releases/final/QA_HACKATHON_APP_PHASE_1_17.md

## Non-goals

- No core app logic rewrite.
- No scoring logic rewrite.
- No bracket logic rewrite.
- No workbook loading rewrite.
- No Friends League logic rewrite.
- No AI Scout behavior rewrite.
- No product UI rewrite.

## CI contract

GitHub Actions must run on:

- pull_request
- push to main

The workflow must:

1. Checkout repository.
2. Set up Python 3.11.
3. Install dependencies from requirements.txt.
4. Run python -m compileall .
5. Run python scripts/run_hackathon_smoke_tests.py.

## Local QA command

python scripts/run_hackathon_smoke_tests.py

## Expected local QA result

HACKATHON_SMOKE_TESTS_PASS
phase_1_16_docs=PASS

## GitHub Actions expected result

Hackathon Smoke Test: PASS

## Live Space verification checklist

- Public Space page opens.
- README metadata is parsed.
- App launches without traceback.
- Blank boot remains waiting_for_completed_results.
- Load Demo Scenario works.
- Recalculate War Room works.
- Group tracker is visible.
- Third-place ranking is visible.
- Bracket JSON is visible.
- Bracket HTML preview is visible.
- Friends League shows 25 rows.
- AI Scout returns non-empty product-safe text.

## Product safety/IP QA

- Public docs state unofficial fan-made positioning.
- No official affiliation claim.
- No money-staked gameplay claim.
- No external live-data claim.
- No guaranteed outcome claim.

## Final decision

Phase 1.17 status: CI added, live Space verification pending after merge.
Blockers: none before PR.
