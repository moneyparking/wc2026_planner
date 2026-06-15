---
title: AI Bracket War Room 2026
emoji: ⚽
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.34.2
python_version: '3.12'
app_file: app.py
pinned: false
license: mit
short_description: Premium WC2026 bracket and scout command center.
tags:
  - gradio
  - huggingface-spaces
  - world-cup-2026
  - football
  - bracket
  - ai-scout
  - friends-league
  - hackathon
  - premium-ui
  - gumroad
  - track:backyard
  - sponsor:openai
  - achievement:offbrand
  - achievement:fieldnotes
---
<!-- FINAL_PMW2026_SUBMISSION_COPY -->

## Final Build Small Submission

### Final Submission Links

- Demo video ZIP: [Download judge walkthrough](releases/final/ai_bracket_war_room_2026_hackathon_demo_video.zip)
- Live app: https://huggingface.co/spaces/Moneyparking/ai-bracket-war-room-2026
- Social post: https://x.com/moneyparking/status/2066602528884580615
- Team HF usernames: @Moneyparking


**Short description:** Premium World Cup 2026 matchday command center for scenario picks, brackets, squad analytics, Friends League scoring, and share-ready fan exports.

**Tags:** `gradio`, `agents`, `sports`, `football`, `world-cup-2026`, `bracket`, `scenario-planning`, `fan-tools`, `premium`, `gumroad`, `hackathon`

### Submission Copy

AI Bracket War Room 2026 turns a football fan’s matchday into a live command center: inspect runtime match results, recompute group impact, preview the bracket path, score a private Friends League, and ask AI Scout for tactical context. The free core is fully judgeable without credentials. Premium is a fan-safe monetization layer for exports, advanced scout cards, printable planning assets, ad-free matchday UX, and a Gumroad source bundle.

### Judge Path

1. Open the Space.
2. Confirm the first screen shows the neon stadium hero, dashboard stats, AI Scout Cards, Friends League Exports, and Free vs Premium funnel.
3. Follow the final judge path: **Open Space -> Load Demo Scenario -> Recalculate War Room -> Match Center -> AI Scout -> Friends League -> Premium CTA**.

### Monetization Funnel

Free core + Premium Matchday Pack $9 / League Pack $27 / Source $49+.

### Safety Boundary

Unofficial fan-made project. Not affiliated with FIFA, tournament organizers, teams, sponsors, broadcasters, or official platforms. Built for fan scenario planning, private leagues, match context, and share-ready exports. No real-money contest logic.

### Final QA Commands

```bash
python -m py_compile app.py
python -m compileall app.py models src layout scripts
python scripts/run_hackathon_smoke_tests.py
python scripts/qa_phase_130_runtime_product.py
```

Expected markers:

```text
HACKATHON_SMOKE_TESTS_PASS
PHASE_1_30_RUNTIME_PRODUCT_QA_PASS
```

# AI Bracket War Room 2026

AI Bracket War Room 2026 is a premium Gradio fan command center for World Cup 2026 planning: 104-match runtime planner, 12-group standings, third-place bubble watch, knockout bracket, Friends League scoring, Advanced AI Scout Cards, Google Sheet control plane, and visible Gumroad monetization.

## Judge Path

Open Space -> Load Demo Scenario -> Recalculate War Room -> Match Center -> AI Scout -> Friends League -> Premium CTA.

## Premium Funnel

Free core + Premium Matchday Pack $9 / League Pack $27 / Source $49+.

## Safety Boundary

Unofficial fan-made project. Not affiliated with FIFA, tournament organizers, teams, sponsors, broadcasters, or official platforms.

PremiumMatchdayWarRoom2026 is an unofficial fan-made Gradio command center for the expanded 48-team 2026 football tournament format. It turns a 104-match planner into a premium matchday surface: runtime results, group tables, third-place ranking, bracket preview, Friends League scoring, AI Scout context, and a clear Gumroad upgrade funnel.

## PremiumMatchdayWarRoom2026 Ontology

**core_loop:** Refresh runtime, inspect a selected match, recalculate tournament impact, then move through Match Center, Groups, 3rd-Place Ranking, Bracket, Friends League, AI Scout, Google Sheet, Premium, and Judge QA.

**premium_tiers:** Free Core stays fully judgeable. Premium Matchday sells advanced AI Scout cards and exports. Ultimate Fan Pack sells PDFs, stickers, and planning assets. Gumroad Source sells the app source and templates.

**design_language:** Neon stadium, dark glass cards, lime/cyan/amber highlights, mobile-first one-column fallback, judge-readable stats above the tabs, and premium conversion visible without blocking the demo.

## Runtime Data Mode

Runtime truth note: **Real-time provider secrets are not configured** by default. The public demo should show Verified Cache Mode unless a live provider and API secret are configured in Hugging Face Space Settings.

The public Space is safe-by-default: it uses `LIVE_SCORE_PROVIDER=verified_cache` unless live-provider secrets are configured in Hugging Face. That means the free judge demo can always run from verified cache, static fixtures, and manual override rows without exposing credentials or depending on a paid feed.

For production live updates after matches are played, configure these HF Space variables/secrets:

```bash
LIVE_SCORE_PROVIDER=football_data  # or api_football, sportmonks, live_score_api
LIVE_SCORE_API_KEY=<provider key when used>
LIVE_SCORE_COMPETITION_ID=<provider competition or league id>
LIVE_REFRESH_SECONDS=60
```

Provider-specific adapters may also require their own secret names, for example `FOOTBALL_DATA_API_KEY`, `API_FOOTBALL_KEY`, `SPORTMONKS_API_KEY`, or `LIVE_SCORE_API_SECRET`. Google Sheet manual overrides remain available through `GOOGLE_SHEET_ENABLED`, `GOOGLE_SHEET_ID`, and `GOOGLE_SERVICE_ACCOUNT_JSON`.

Runtime data context remains:

```text
Manual override > live provider > verified public cache > static fixture seed
```

## One-Sentence Pitch

Open the Space, refresh the runtime, select one match, and watch a fan-made World Cup 2026 War Room update groups, bracket paths, Friends League scoring, and AI Scout context from the same runtime engine.

## Judge Path

1. Open the Hugging Face Space or run `python app.py`.
2. Click **Load Demo Scenario**.
3. Click **Recalculate War Room**.
4. Open **Match Center**.
5. Open **AI Scout**.
6. Open **Friends League**.
7. Confirm the **Premium Matchday Pack** CTA is visible and non-blocking.

## What Works Now

- 48 teams.
- 12 groups.
- 104 matches.
- 495 third-place combination proof marker.
- Static fixture seed with optional live-score adapter.
- Google Sheet/manual override control plane.
- Runtime tournament state engine.
- Match Center with selected-match inspection.
- Group table and third-place ranking.
- Bracket preview.
- Friends League demo scoring.
- AI Scout context layer.
- PremiumMatchdayWarRoom2026 first screen with visible dashboard stats, AI Scout Cards, Friends League Exports, and Free vs Premium rail.
- Judge QA path remains accessible.

## Legacy QA Compatibility

This remains an unofficial fan-made football tournament planning demo. The original judge promise still works: Change one result, recalculate the 104-match runtime, inspect the Tournament Impact Panel, compare Friends League impact, and review AI Scout context.

Required Phase 1.16 / Phase 1.19 docs remain part of the submission package:

- `SPACE_DEPLOYMENT.md`
- `JUDGE_DEMO_SCRIPT.md`
- `releases/final/QA_HACKATHON_APP_PHASE_1_16.md`

## Monetization Funnel

Gumroad links are controlled by environment variables in `app.py`:

```bash
GUMROAD_PREMIUM_URL=https://gumroad.com/l/ai-bracket-war-room-2026-premium
GUMROAD_SOURCE_URL=https://gumroad.com/l/ai-bracket-war-room-2026-source
```

| Tier | Price | Buyer | Value |
|---|---:|---|---|
| Free Core | $0 | Judges and casual fans | Runtime match center, groups, third-place ranking, bracket preview, basic AI Scout, Friends League demo, Judge QA path |
| Premium Matchday Pack | $9 | Matchday fans and private league hosts | Advanced AI Scout cards, scenario summaries, Friends League export pack, ad-free matchday mode |
| Ultimate Fan Pack | $27 | Digital planners and watch-party hosts | GoodNotes/PDF command center, printable tournament sheets, sticker pack, watch-party planning assets |
| Gumroad Source | $49-99 | Builders and indie sellers | Full Gradio source, templates, customization license, deployment notes, monetization kit |

### Gumroad Premium Pitch

AI Bracket War Room 2026 Premium turns the free fan-made tournament planner into a complete matchday command center. Free users can judge the full runtime. Premium buyers get advanced AI Scout cards, scenario exports, private Friends League packs, ad-free planning mode, and fan-ready assets for watch parties.

### Gumroad Source Pitch

The source bundle gives builders a deployable Gradio app, premium templates, runtime architecture, monetization copy, and setup notes so they can customize their own fan-made tournament planner without rebuilding the engine from scratch.

## Safety Boundary

Unofficial fan-made project. Not affiliated with FIFA, tournament organizers, teams, sponsors, broadcasters, or official platforms.
Fan-only scenario planning with no real-money contest logic. Uses no official logos, crests, sponsor marks, player likenesses, protected emblems, or mascots.

## Local Quickstart

```bash
pip install -r requirements.txt
python app.py
```

## Pre-Push QA

```bash
python -m py_compile app.py
python -m compileall app.py models src layout scripts
python scripts/run_hackathon_smoke_tests.py
python scripts/qa_phase_130_runtime_product.py
```

Expected markers:

```text
HACKATHON_SMOKE_TESTS_PASS
PHASE_1_30_RUNTIME_PRODUCT_QA_PASS
```

## 10-Point PremiumMatchdayWarRoom2026 QA Checklist

1. Neon stadium hero and title are visible first.
2. Dashboard stats row shows Fixtures, Completed, Live now, and Next.
3. Advanced AI Scout Cards show three cards with progress bars.
4. Friends League Exports are visible above tabs.
5. Free vs Premium rail highlights Premium Matchday.
6. Navigation anchors work: `#match-center`, `#ai-scout`, `#premium`.
7. Existing tabs still work: Match Center, Groups, 3RD-PLACE RANKING, Bracket, Friends League, AI Scout, Google Sheet, Premium, Judge QA.
8. Mobile 375-760px collapses to one column with full-width buttons.
9. Judge path works: Open Space -> Load Demo Scenario -> Recalculate War Room -> Match Center -> AI Scout -> Friends League -> Premium CTA.
10. Safety copy is clear: unofficial fan-made project, no affiliation claims, no official marks.

## 60-Second Demo Video Script

**0-8s:** "This is AI Bracket War Room 2026, a fan-made PremiumMatchdayWarRoom2026 command center for the expanded 104-match tournament."

**8-18s:** "The first screen is the premium matchday dashboard: live status, Google Sheet readiness, selected match, fixtures, completed results, live count, and next match."

**18-30s:** "The free core is fully judgeable. I refresh runtime, load the demo scenario, and recalculate the War Room."

**30-42s:** "One runtime state powers Match Center, Groups, third-place ranking, Bracket, Friends League, and AI Scout."

**42-52s:** "Premium is the business model: advanced AI Scout cards, CSV exports, private league packs, fan PDFs, stickers, and the Gumroad source bundle."

**52-60s:** "It is an unofficial fan-made project with no affiliation claims and no official marks. Free judges the engine. Premium sells planning and exports."

## Core Files

- `app.py` - Gradio app entry point and PremiumMatchdayWarRoom2026 shell.
- `layout/css_styles.py` - base sport UI styling.
- `models/` - tournament scoring, data loading, bracket mapping, and demo scenario helpers.
- `src/` - runtime data loader, live-score adapter, Google Sheet adapter, and runtime engine.
- `scripts/run_hackathon_smoke_tests.py` - hackathon smoke QA.
- `scripts/qa_phase_130_runtime_product.py` - runtime product QA.
- `requirements.txt` - runtime dependencies.


## Phase 1.39 - Final Premium Lower Modules

The lower app surface now matches the premium mockups: Match Center, Groups, Bracket, Friends League, and AI Scout use the same neon stadium product system with card-first hierarchy, mobile-first grids, visible premium exports, and Gumroad CTAs. Tables remain available for judge verification, but every module now opens with a product-quality summary surface.

Judge path: Open Space -> Load Demo Scenario -> Recalculate War Room -> Match Center -> AI Scout -> Friends League -> Premium CTA.


## Phase 1.39 - Final PremiumMatchdayWarRoom2026 Release Candidate

**short_description:** Premium AI bracket, matchday, Friends League, and scout-card command center for World Cup 2026 fans.

**Submission copy:** AI Bracket War Room 2026 is a Gradio-powered premium fan command center: 104-match runtime planner, 12-group standings, third-place bubble watch, knockout bracket, Friends League scoring, Advanced AI Scout Cards, Google Sheet control plane, and visible Gumroad monetization. The free judge path stays fully open while Premium Matchday, Ultimate Fan Pack, and Source Bundle rails show a realistic sales funnel.

**Tags:** gradio, huggingface-spaces, world-cup-2026, football, bracket, ai-scout, friends-league, hackathon, premium-ui, gumroad

**Judge path:** Open Space -> Load Demo Scenario -> Recalculate War Room -> Match Center -> AI Scout -> Friends League -> Premium CTA.

**Safety boundary:** Unofficial fan-made project. Not affiliated with FIFA, tournament organizers, teams, sponsors, broadcasters, or official platforms.

**Premium funnel:** Free core + Premium Matchday Pack $9 / League Pack $27 / Source $49+.
