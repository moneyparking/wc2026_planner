# V1.25 GitHub Release Asset Upload Commands

The connector committed V1.25 release metadata into the repository branch and main. The available GitHub connector does not expose the GitHub Releases binary asset upload endpoint.

Create the release in GitHub UI or with GitHub CLI.

## Release settings

- Tag: `v1.25-final-commercial-release`
- Target: `main`
- Title: `V1.25 Final Commercial Layer Fix`
- Pre-release: unchecked
- Latest: checked

## Assets

Attach these files:

1. `01_WC2026_Matchday_No_Chaos_Ultimate_V1.25_GoodNotes_Hyperlinked.pdf`
2. `02_WC2026_Matchday_No_Chaos_Ultimate_V1.25_Flattened_Compatibility.pdf`
3. `03_WC2026_Watch_Party_Bingo_Bonus_V1.25.pdf`
4. `04_WC2026_Matchday_No_Chaos_V1.25_DualTone_Jersey_Sticker_Icon_Pack_300DPI_PNG_SVG.zip`
5. `05_WC2026_Matchday_No_Chaos_Ultimate_V1.25_Quick_Start_Guide.pdf`
6. `WC2026_Matchday_No_Chaos_Ultimate_V1.25_Buyer_Files.zip`
7. `PHASE_1.25_VALIDATION_REPORT.json`
8. `PHASE_1.25_VISUAL_QA_CONTACT_SHEET.jpg`
9. `PHASE_1.25_CHANGELOG_QA.md`

## GitHub CLI

```bash
gh release create v1.25-final-commercial-release \
  /mnt/data/01_WC2026_Matchday_No_Chaos_Ultimate_V1.25_GoodNotes_Hyperlinked.pdf \
  /mnt/data/02_WC2026_Matchday_No_Chaos_Ultimate_V1.25_Flattened_Compatibility.pdf \
  /mnt/data/03_WC2026_Watch_Party_Bingo_Bonus_V1.25.pdf \
  /mnt/data/04_WC2026_Matchday_No_Chaos_V1.25_DualTone_Jersey_Sticker_Icon_Pack_300DPI_PNG_SVG.zip \
  /mnt/data/05_WC2026_Matchday_No_Chaos_Ultimate_V1.25_Quick_Start_Guide.pdf \
  /mnt/data/WC2026_Matchday_No_Chaos_Ultimate_V1.25_Buyer_Files.zip \
  /mnt/data/PHASE_1.25_VALIDATION_REPORT.json \
  /mnt/data/PHASE_1.25_VISUAL_QA_CONTACT_SHEET.jpg \
  /mnt/data/PHASE_1.25_CHANGELOG_QA.md \
  --repo moneyparking/wc2026_planner \
  --title "V1.25 Final Commercial Layer Fix" \
  --notes "V1.25 final commercial release. QA PASS. 128 pages. 1261 GoodNotes hyperlinks. 104 match logs preserved. PNG alpha and 300 DPI validated. Bracket layer bleed, stats HUD collision and awards title collision fixed."
```
