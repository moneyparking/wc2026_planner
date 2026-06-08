# V1.23 GitHub Release Asset Upload Commands

The connector committed release metadata into the repository branch.

The connector available in this chat does not expose the GitHub Releases binary asset upload endpoint. Attach buyer binaries to the GitHub Release with GitHub CLI or web UI.

## Recommended CLI command

```bash
gh release create v1.23-premium-jersey-system \
  /mnt/data/WC2026_Matchday_No_Chaos_Ultimate_V1.23_GoodNotes_Hyperlinked.pdf \
  /mnt/data/WC2026_Matchday_No_Chaos_Ultimate_V1.23_Flattened_Compatibility.pdf \
  /mnt/data/WC2026_Matchday_No_Chaos_Ultimate_V1.23_Buyer_Files.zip \
  /mnt/data/WC2026_Matchday_No_Chaos_V1.23_DualTone_Jersey_Sticker_Icon_Pack_300DPI_PNG_SVG.zip \
  /mnt/data/WC2026_Matchday_No_Chaos_Ultimate_V1.23_Quick_Start_Guide.pdf \
  /mnt/data/PHASE_1.23_VISUAL_QA_CONTACT_SHEET.jpg \
  --repo moneyparking/wc2026_planner \
  --title "V1.23 Premium Mobile App Jersey Token System" \
  --notes "V1.23 release package. QA PASS. 128 pages. 1261 hyperlinks. 104/104 match logs clickable. 389/389 PNG stickers alpha and 300 DPI validated."
```
