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

## IP disclaimer

Unofficial fan-made digital planner. Not affiliated with or endorsed by FIFA, World Cup, national teams, leagues, clubs or players. No official logos, crests or trademarks are included.
