# Hugging Face Space Deployment Plan

## Deployment contract

AI Bracket War Room 2026 deploys as a Gradio Space from repository root app.py.

Required README metadata:

---
title: AI Bracket War Room 2026
emoji: 🏟️
colorFrom: blue
colorTo: gray
sdk: gradio
app_file: app.py
pinned: false
---

The YAML block must be the first content in README.md.

## Required repository files

- README.md
- app.py
- requirements.txt
- scripts/run_hackathon_smoke_tests.py
- SPACE_DEPLOYMENT.md
- JUDGE_DEMO_SCRIPT.md
- releases/final/QA_HACKATHON_APP_PHASE_1_16.md
- releases/final/artifacts/03_AI_Bracket_War_Room_2026_Spreadsheet_Engine.xlsx

## Requirements policy

requirements.txt must contain runtime dependencies only. Do not add notebook, GPU, or dev-only packages for Phase 1.16.

## Secrets and variables policy

Phase 1.16 requires no secrets. Do not commit tokens, private keys, .env files, private links, claim codes, or credentials. Future external integrations must read optional values from environment variables only.

## Persistent storage policy

Phase 1.16 does not require persistent storage. The judge demo is session-local. User edits are not written back to the repository.

## Public Space verification checklist

- Public page opens.
- Space builds successfully.
- App launches without traceback.
- Blank boot remains waiting_for_completed_results.
- Demo scenario loads.
- Recalculate path updates visible outputs.
- Group tracker is visible.
- Third-place ranking is visible.
- Bracket JSON is visible.
- Bracket HTML preview is visible.
- Friends League shows rows.
- AI Scout returns non-empty product-safe text.
- README renders the demo instructions.

## Common failure modes and fixes

- Space cannot find app: keep YAML at the top and set app_file: app.py.
- App imports fail: add the missing runtime package to requirements.txt.
- Blank boot fails: restore blank boot waiting state.
- Canonical workbook missing: verify exact file path under releases/final/artifacts.
- README metadata ignored: move YAML block to byte 1 of README.md.

## Final deployment signoff

Run before final release:

python -m compileall .
python scripts/run_hackathon_smoke_tests.py

Expected result:

HACKATHON_SMOKE_TESTS_PASS
