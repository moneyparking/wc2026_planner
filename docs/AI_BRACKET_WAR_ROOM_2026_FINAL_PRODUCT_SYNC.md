# AI Bracket War Room 2026 — Final Product Sync

Updated: 2026-06-06
Repository: `moneyparking/wc2026_planner`
Commercial status: production sync for Etsy buyer package and listing media pipeline.

## Product identity

**Product name:** AI Bracket War Room 2026  
**Market format:** unofficial fan-made GoodNotes + printable football/soccer tournament planner  
**Primary buyer:** US/UK digital planner users, GoodNotes users, tournament bracket players, private friends-league hosts, football watch-party organizers  
**Positioning:** premium sports-tech command-center planner for prediction tracking, matchday control, private scoring, printable watch-night workflows, and transparent PNG sticker planning.

## Locked IP boundary

Allowed visual language:

- Generic football tournament graphics
- Generic trophy-like / champion / winner icons
- Bracket, pitch-line, goal, VAR, red card, green check, matchday UI language
- Country flags only when drawn generically and without federation crests
- Neutral fan-made football command-center atmosphere

Forbidden visual language:

- FIFA logo, official World Cup emblem, official trophy replica, mascot, official sponsor marks
- National federation crests, club crests, player likenesses, broadcast graphics, official app UI
- Claims of affiliation, endorsement, official access, sportsbook odds, betting-product framing

Required disclaimer:

> Unofficial fan-made digital download. Not affiliated with or endorsed by FIFA, World Cup, national teams, leagues, clubs, sponsors, broadcasters, or players. No official logos, crests, sponsor marks, player likenesses, or protected tournament emblems are included.

## Current buyer package target

Current buyer-facing package name:

```text
AI_Bracket_War_Room_2026_FINAL_BUYER_PACKAGE_UPDATED.zip
```

Expected buyer-facing contents:

```text
01_AI_Bracket_War_Room_2026_GoodNotes_Hyperlinked_PDF.pdf
02_AI_Bracket_War_Room_2026_Printable_Backup_PDF.pdf
03_AI_Bracket_War_Room_2026_Google_Sheets_Tracker_Access_Guide.pdf
04_AI_Bracket_War_Room_2026_Sticker_Pack_300DPI_PNG.zip
05_AI_Bracket_War_Room_2026_Quick_Start_Guide.pdf
```

Packaging target:

- Etsy-compatible digital delivery
- Buyer ZIP below 20 MB when possible
- If buyer package exceeds Etsy single-file limit, split into clean numbered upload files with buyer-readable names
- No placeholder PDFs
- No blank planner pages
- No broken internal navigation

## Sticker pack decision

Preferred included sticker pack:

```text
04_AI_Bracket_War_Room_2026_FIX9_FINAL_APPROVED_Sticker_Pack_300DPI_PNG.zip
```

Decision logic:

- Use the most recent approved sticker ZIP as the package source of truth.
- If an older sticker ZIP contains stronger individual assets, merge only after duplicate-name and alpha-channel QA.
- Do not ship two competing sticker ZIPs in the buyer package; buyer delivery should contain one final sticker pack.
- Listing copy should state the exact final count only after ZIP-level file count QA.

Sticker technical standard:

```text
/flags/
/jerseys/
/icons/
```

Required sticker QA:

- PNG format
- Transparent alpha channel
- 300 DPI export target
- No official federation crests
- No official tournament marks
- Consistent naming: `category_color_number.png` or clear buyer-readable equivalent
- No duplicate filenames across folders
- No hidden macOS/system files shipped as buyer-facing content

## Etsy video specs — planner listing

Output target:

```text
AI_Bracket_War_Room_2026_Planner_Etsy_Video.mp4
```

Container package target:

```text
AI_Bracket_War_Room_2026_Etsy_Videos.zip
```

Technical constraints:

- Duration: 15 seconds maximum
- Aspect ratio: 1:1 square
- Resolution: 1080 × 1080 px
- Format: MP4, H.264
- Audio: none
- File size: under Etsy video limit
- Style: realistic iPad 13 / GoodNotes-like screen presentation
- Interaction style: depressed-button tap animation only; no pointer circles, no AI dots, no fake official app UI

Planner video sequence:

1. Hero screen: planner open on realistic iPad 13
2. Tap/depress navigation button into main planner dashboard
3. Tap/depress Google Sheets access button
4. Tap/depress 104 matches section
5. Tap/depress Friends League section
6. End frame: full product stack with buyer value copy

## Etsy video specs — PNG sticker listing

Output target:

```text
AI_Bracket_War_Room_2026_Sticker_Pack_Etsy_Video.mp4
```

Technical constraints:

- Duration: 15 seconds maximum
- Aspect ratio: 1:1 square
- Resolution: 1080 × 1080 px
- Format: MP4, H.264
- Audio: none
- File size: under Etsy video limit
- Style: realistic iPad 13 or MacBook screen with clean sports-tech UI
- Interaction style: depressed-button tap animation only; no circular click indicators

Sticker video sequence:

1. Sticker inventory preview on realistic device
2. Tap/depress Icons tab
3. Tap/depress Jerseys tab
4. Tap/depress Flags tab
5. Tap/depress Form / Kit tab
6. End frame: transparent PNG, GoodNotes ready, instant download

## Mockup production state

Locked listing image system:

- Canvas: 3000 × 3000 px
- Color profile: sRGB
- Safe area: central 2400 × 2400 px
- Background: clean off-white / light sports-tech studio
- Device: realistic iPad / MacBook only where needed
- Text: high-contrast navy/charcoal, readable at thumbnail scale
- Design language: premium flat sports-tech, no official branding

Image batches:

- Batch A: hero, value stack, bracket proof
- Batch B: AI Scout slip, Friends League, stickers
- Batch C: group tracker, watch-party printable, delivery, compatibility

## QA gate before Etsy upload

PDF QA:

- All pages rendered
- No blank-like pages
- Hyperlinks tested
- Sticky navigation hotspots consistent across pages
- Touch targets at least 25 px
- Dark/readable writing zones with sufficient contrast
- File size controlled for Etsy delivery

Sticker QA:

- One final sticker ZIP selected
- 300 DPI PNG target
- Transparent backgrounds
- Folder structure clean
- No official IP assets
- File count verified before listing copy is finalized

Listing QA:

- SEO title starts with primary keyword
- 5+ value bullets
- 8+ mockup slots
- IP disclaimer included
- Digital download/no physical item statement included
- Personalization confirmation: buyer types YES to acknowledge digital download

## Connector limitation note

This sync patch updates repository documentation/state. Binary artifacts such as final buyer ZIPs, sticker ZIPs, MP4 videos, and rendered PDFs must be attached or generated in the build environment before they can be uploaded as release assets or committed through a binary-capable workflow.

## Final production artifact lock

Generated: 2026-06-06T16:47:29Z

- Buyer ZIP: `AI_Bracket_War_Room_2026_FINAL_BUYER_PACKAGE_UPDATED.zip` - 20353596 bytes, SHA256 `014c5bf335131776...`, QA PASS.
- Sticker ZIP: `04_AI_Bracket_War_Room_2026_Sticker_Pack_300DPI_PNG.zip` - 306 valid transparent PNG stickers, SHA256 `9fce7391d2d1c5d8...`, QA PASS.
- Etsy video ZIP: `AI_Bracket_War_Room_2026_Etsy_Videos.zip` - 1099909 bytes, SHA256 `7eb5b79ab7ad214b...`, QA PASS.
- Release folder: `releases/final/`

The buyer ZIP is below 20 MiB and above 20,000,000 bytes. If Etsy's upload UI enforces a strict decimal threshold, use a release asset or split-upload workflow documented by the seller before upload.
