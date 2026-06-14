#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


FINAL_CSS = r'''
FINAL_PMW2026_PRODUCTION_CSS = r"""
/* ==========================================================================
   FINAL PRODUCTION POLISH — PremiumMatchdayWarRoom2026
   SF Design Elite + Build Small Judge Readiness
   ========================================================================== */

:root {
  --pmw-final-bg: #071018;
  --pmw-final-bg-2: #020617;
  --pmw-final-neon: #A7FF00;
  --pmw-final-gold: #FFD166;
  --pmw-final-cyan: #35D6E8;
  --pmw-final-text: #F8FAFC;
  --pmw-final-muted: #B6C3D8;
  --pmw-final-dim: #7B8AA4;
  --pmw-final-line: rgba(53, 214, 232, 0.22);
  --pmw-final-shadow: 0 28px 90px rgba(0, 0, 0, 0.48);
}

/* Canvas */
.gradio-container {
  max-width: 100% !important;
  color: var(--pmw-final-text) !important;
  background:
    radial-gradient(circle at 12% -8%, rgba(53, 214, 232, 0.22), transparent 32%),
    radial-gradient(circle at 86% 2%, rgba(167, 255, 0, 0.16), transparent 30%),
    radial-gradient(circle at 46% 105%, rgba(255, 209, 102, 0.12), transparent 38%),
    linear-gradient(180deg, #071018 0%, #071018 46%, #020617 100%) !important;
}

.gradio-container::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  opacity: 0.22;
  background-image:
    linear-gradient(rgba(53, 214, 232, 0.065) 1px, transparent 1px),
    linear-gradient(90deg, rgba(53, 214, 232, 0.065) 1px, transparent 1px);
  background-size: 44px 44px;
  mask-image: radial-gradient(circle at 50% 16%, black, transparent 76%);
}

.gradio-container > .main,
.gradio-container .contain,
.gradio-container .wrap {
  position: relative;
  z-index: 1;
}

/* Absolute button hardening: removes white/light Gradio corners */
.gradio-container button,
.gradio-container a.pmw-action,
.gradio-container a.premium-button,
.gradio-container .premium-button,
.gradio-container .pmw-button,
.gradio-container [role="button"] {
  position: relative !important;
  isolation: isolate !important;
  overflow: hidden !important;
  border-radius: 999px !important;
  min-height: 46px !important;
  padding: 11px 18px !important;
  border: 0 !important;
  outline: 0 !important;
  background-clip: border-box !important;
  box-shadow: none !important;
  font-weight: 950 !important;
  letter-spacing: -0.01em !important;
  text-decoration: none !important;
}

.gradio-container button::before,
.gradio-container button::after,
.gradio-container [role="button"]::before,
.gradio-container [role="button"]::after {
  border-radius: inherit !important;
  border: 0 !important;
  box-shadow: none !important;
}

.gradio-container button *,
.gradio-container [role="button"] *,
.gradio-container a.pmw-action *,
.gradio-container a.premium-button * {
  border-radius: inherit !important;
  background: transparent !important;
}

.gradio-container button.primary,
.gradio-container .primary,
.gradio-container a.pmw-action.primary,
.gradio-container .premium-button.primary {
  background: linear-gradient(135deg, var(--pmw-final-neon), var(--pmw-final-gold)) !important;
  color: #071018 !important;
  border: 0 !important;
  box-shadow: 0 18px 46px rgba(167, 255, 0, 0.22) !important;
}

.gradio-container button.secondary,
.gradio-container a.pmw-action.secondary,
.gradio-container .premium-button.secondary {
  background: rgba(53, 214, 232, 0.13) !important;
  color: #E6FBFF !important;
  border: 1px solid rgba(53, 214, 232, 0.32) !important;
  box-shadow: inset 0 0 0 1px rgba(53, 214, 232, 0.04) !important;
}

.gradio-container button:hover,
.gradio-container a.pmw-action:hover,
.gradio-container a.premium-button:hover {
  transform: translateY(-1px);
  filter: saturate(1.05);
}

.gradio-container button:focus-visible,
.gradio-container a:focus-visible {
  outline: 2px solid rgba(167, 255, 0, 0.72) !important;
  outline-offset: 3px !important;
}

/* Inputs */
.gradio-container input,
.gradio-container textarea,
.gradio-container select {
  background: rgba(2, 6, 23, 0.76) !important;
  color: var(--pmw-final-text) !important;
  border: 1px solid rgba(53, 214, 232, 0.22) !important;
  border-radius: 18px !important;
  box-shadow: none !important;
}

.gradio-container label,
.gradio-container .label-wrap span {
  color: #E6FBFF !important;
  font-weight: 850 !important;
}

/* Tabs */
.gradio-container button[role="tab"] {
  min-height: 42px !important;
  border-radius: 999px !important;
  background: rgba(7, 16, 24, 0.78) !important;
  color: var(--pmw-final-muted) !important;
  border: 1px solid rgba(148, 163, 184, 0.12) !important;
}

.gradio-container button[role="tab"][aria-selected="true"] {
  background: linear-gradient(135deg, var(--pmw-final-cyan), var(--pmw-final-neon)) !important;
  color: #071018 !important;
  border: 0 !important;
  box-shadow: 0 14px 38px rgba(53, 214, 232, 0.20) !important;
}

.product-button-row {
  margin: 8px auto 16px !important;
  max-width: 1480px !important;
}

.product-button-row button {
  width: auto !important;
}

/* Premium shell */
.pmw-shell {
  position: relative;
  isolation: isolate;
  max-width: 1480px;
  margin: 0 auto 22px auto;
  padding: clamp(12px, 2vw, 26px);
}

.pmw-stadium-hero {
  position: relative;
  overflow: hidden;
  border-radius: 34px;
  border: 1px solid rgba(53, 214, 232, 0.22);
  background:
    radial-gradient(circle at 18% 0%, rgba(53, 214, 232, 0.26), transparent 32%),
    radial-gradient(circle at 88% 10%, rgba(167, 255, 0, 0.18), transparent 28%),
    radial-gradient(circle at 50% 120%, rgba(255, 209, 102, 0.12), transparent 44%),
    linear-gradient(135deg, rgba(7, 16, 24, 0.98), rgba(9, 22, 34, 0.94) 48%, rgba(2, 6, 23, 0.99));
  box-shadow: var(--pmw-final-shadow);
}

.pmw-stadium-hero::before {
  content: "";
  position: absolute;
  inset: -58% -10% auto -10%;
  height: 430px;
  background:
    repeating-radial-gradient(ellipse at center, rgba(53, 214, 232, 0.18) 0 1px, transparent 1px 18px);
  transform: perspective(900px) rotateX(62deg);
  transform-origin: center bottom;
  opacity: 0.52;
}

.pmw-stadium-hero::after {
  content: "";
  position: absolute;
  left: 8%;
  right: 8%;
  bottom: -1px;
  height: 44%;
  border-radius: 50% 50% 0 0 / 18% 18% 0 0;
  background:
    linear-gradient(90deg, transparent 0 49%, rgba(248, 250, 252, 0.14) 49% 51%, transparent 51%),
    linear-gradient(0deg, rgba(52, 211, 153, 0.16), rgba(52, 211, 153, 0.035));
  border: 1px solid rgba(167, 255, 0, 0.16);
  opacity: 0.62;
}

.pmw-hero-inner {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: minmax(0, 1.18fr) minmax(320px, 0.82fr);
  gap: clamp(16px, 2vw, 28px);
  padding: clamp(22px, 4.6vw, 52px);
}

.pmw-kicker,
.pmw-card-kicker {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--pmw-final-cyan) !important;
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.pmw-kicker::before,
.pmw-card-kicker::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--pmw-final-neon);
  box-shadow: 0 0 20px rgba(167, 255, 0, 0.78);
}

.pmw-title {
  margin: 12px 0 12px;
  color: var(--pmw-final-text) !important;
  font-size: clamp(42px, 7.2vw, 92px);
  line-height: 0.86;
  letter-spacing: -0.078em;
  font-weight: 1000;
}

.pmw-gradient-text {
  background: linear-gradient(135deg, #FFFFFF 0%, #DFFBFF 34%, var(--pmw-final-neon) 70%, var(--pmw-final-gold) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.pmw-subtitle {
  max-width: 780px;
  color: #C9D6EA !important;
  font-size: clamp(15px, 1.55vw, 19px);
  line-height: 1.6;
  margin: 0;
}

.pmw-chip-row,
.pmw-hero-actions,
.pmw-buy-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.pmw-chip-row {
  margin-top: 18px;
}

.pmw-hero-actions,
.pmw-buy-row {
  margin-top: 22px;
}

.pmw-chip {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.68);
  color: #DCEBFF !important;
  border: 1px solid rgba(148, 163, 184, 0.16);
  font-size: 12px;
  font-weight: 900;
  backdrop-filter: blur(12px);
}

.pmw-chip.live {
  color: #071018 !important;
  background: linear-gradient(135deg, var(--pmw-final-neon), #34D399);
  border: 0;
}

.pmw-chip.premium {
  color: #1F1300 !important;
  background: linear-gradient(135deg, var(--pmw-final-gold), #FFF3BD);
  border: 0;
}

.pmw-action {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  min-height: 48px;
  padding: 12px 18px;
  border-radius: 999px;
  text-decoration: none !important;
  font-weight: 950;
}

.pmw-action.primary,
.pmw-action.gumroad {
  background: linear-gradient(135deg, var(--pmw-final-neon), var(--pmw-final-gold));
  color: #071018 !important;
  box-shadow: 0 18px 46px rgba(167, 255, 0, 0.22);
}

.pmw-action.secondary,
.pmw-action.source {
  background: rgba(53, 214, 232, 0.13);
  color: #E6FBFF !important;
  border: 1px solid rgba(53, 214, 232, 0.32);
}

.pmw-live-panel {
  border: 1px solid rgba(53, 214, 232, 0.24);
  border-radius: 26px;
  background: rgba(2, 6, 23, 0.70);
  backdrop-filter: blur(18px);
  padding: 18px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06);
}

.pmw-score-card,
.pmw-card,
.app-card,
.card-shell,
.sport-card,
.runtime-card,
.price-card,
.premium-export-card,
.submission-card,
.premium-disclaimer,
.table-card,
.module-card,
.status-card,
.nav-card,
.mini-module,
.table-skeleton-card {
  border-radius: 24px !important;
  border: 1px solid rgba(148, 163, 184, 0.14) !important;
  background:
    linear-gradient(180deg, rgba(15, 23, 42, 0.80), rgba(2, 6, 23, 0.70)) !important;
  color: var(--pmw-final-text) !important;
  box-shadow: 0 18px 58px rgba(0, 0, 0, 0.24) !important;
}

.pmw-score-card {
  padding: 18px;
}

.pmw-score-label {
  color: var(--pmw-final-dim) !important;
  text-transform: uppercase;
  letter-spacing: 0.10em;
  font-size: 11px;
  font-weight: 950;
}

.pmw-scoreline {
  margin-top: 8px;
  color: var(--pmw-final-text) !important;
  font-size: clamp(24px, 3vw, 38px);
  line-height: 1.0;
  font-weight: 1000;
  letter-spacing: -0.048em;
}

.pmw-source {
  margin-top: 10px;
  color: var(--pmw-final-muted) !important;
  font-size: 13px;
  line-height: 1.45;
}

.pmw-stat-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-top: 12px;
}

.pmw-live-panel .pmw-stat-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.pmw-stat {
  min-height: 92px;
  padding: 14px;
  border-radius: 20px;
  background: rgba(15, 23, 42, 0.60);
  border: 1px solid rgba(148, 163, 184, 0.13);
}

.pmw-stat span {
  display: block;
  color: var(--pmw-final-dim) !important;
  font-size: 11px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.pmw-stat strong {
  display: block;
  margin-top: 8px;
  color: var(--pmw-final-text) !important;
  font-size: 25px;
  line-height: 1;
  font-weight: 1000;
}

.pmw-stat p {
  margin: 8px 0 0;
  color: var(--pmw-final-muted) !important;
  font-size: 12px;
  line-height: 1.35;
}

.pmw-dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 16px;
  margin-top: 18px;
}

.pmw-card {
  position: relative;
  overflow: hidden;
  border-radius: 26px !important;
  backdrop-filter: blur(16px);
  padding: 18px;
}

.pmw-card::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.06), transparent 40%);
}

.pmw-card > * {
  position: relative;
  z-index: 1;
}

.pmw-card h2,
.pmw-card h3,
.pmw-card li,
.pmw-card p {
  color: inherit !important;
}

.pmw-wide { grid-column: span 7; }
.pmw-side { grid-column: span 5; }
.pmw-full { grid-column: 1 / -1; }

.pmw-scout-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.pmw-scout-card {
  min-height: 170px;
  border-radius: 20px;
  padding: 15px;
  background:
    radial-gradient(circle at 100% 0%, rgba(53, 214, 232, 0.13), transparent 38%),
    rgba(2, 6, 23, 0.48);
  border: 1px solid rgba(53, 214, 232, 0.18);
}

.pmw-scout-card strong {
  display: block;
  color: var(--pmw-final-text) !important;
  font-size: 18px;
  font-weight: 950;
  letter-spacing: -0.02em;
}

.pmw-meter {
  overflow: hidden;
  margin: 12px 0 8px;
  height: 8px;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.18);
}

.pmw-meter span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--pmw-final-cyan), var(--pmw-final-neon));
  box-shadow: 0 0 22px rgba(53, 214, 232, 0.38);
}

.pmw-export-list {
  display: grid;
  gap: 10px;
  margin-top: 12px;
}

.pmw-export-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: center;
  padding: 12px;
  border-radius: 18px;
  background: rgba(15, 23, 42, 0.56);
  border: 1px solid rgba(148, 163, 184, 0.14);
}

.pmw-export-row b {
  color: var(--pmw-final-text) !important;
}

.pmw-export-row span {
  color: var(--pmw-final-muted) !important;
  font-size: 13px;
}

.pmw-pill {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  min-height: 28px;
  padding: 6px 10px;
  border-radius: 999px;
  color: #071018 !important;
  background: linear-gradient(135deg, var(--pmw-final-gold), var(--pmw-final-neon));
  font-size: 11px;
  font-weight: 950;
  white-space: nowrap;
}

.pmw-plan-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-top: 14px;
}

.pmw-plan {
  border-radius: 22px;
  padding: 18px;
  background: rgba(2, 6, 23, 0.56);
  border: 1px solid rgba(148, 163, 184, 0.15);
}

.pmw-plan.featured {
  border-color: rgba(167, 255, 0, 0.38);
  background:
    radial-gradient(circle at 100% 0%, rgba(167, 255, 0, 0.16), transparent 36%),
    rgba(2, 6, 23, 0.72);
  box-shadow: 0 18px 54px rgba(167, 255, 0, 0.10);
}

.pmw-price {
  color: var(--pmw-final-text) !important;
  font-size: 36px;
  line-height: 1;
  font-weight: 1000;
  letter-spacing: -0.055em;
}

.pmw-final-buy-strip {
  margin-top: 14px;
  padding: 16px;
  border-radius: 24px;
  background:
    radial-gradient(circle at 8% 0%, rgba(255, 209, 102, 0.12), transparent 36%),
    rgba(7, 16, 24, 0.76);
  border: 1px solid rgba(255, 209, 102, 0.20);
}

.module-kicker,
.sport-label {
  color: var(--pmw-final-cyan) !important;
  font-weight: 950 !important;
  letter-spacing: 0.10em !important;
}

.today-scoreline,
.sport-card h2,
.sport-card h3,
.card-shell h2,
.card-shell h3,
.price-card h3 {
  color: var(--pmw-final-text) !important;
}

.today-meta,
.sport-muted,
.card-shell p,
.price-card p,
.premium-disclaimer,
.premium-export-card p {
  color: var(--pmw-final-muted) !important;
}

/* No bright table blocks */
.gradio-container table,
.gradio-container .dataframe,
.gradio-container .gradio-dataframe {
  background: rgba(2, 6, 23, 0.76) !important;
  color: var(--pmw-final-text) !important;
  border-radius: 18px !important;
  overflow: hidden !important;
}

.gradio-container th {
  background: rgba(15, 23, 42, 0.96) !important;
  color: #E6FBFF !important;
  font-weight: 950 !important;
}

.gradio-container td {
  background: rgba(2, 6, 23, 0.72) !important;
  color: #DBEAFE !important;
  border-color: rgba(148, 163, 184, 0.10) !important;
}

/* Mobile: 375px+ */
@media (max-width: 1020px) {
  .pmw-hero-inner {
    grid-template-columns: 1fr;
  }

  .pmw-wide,
  .pmw-side,
  .pmw-full {
    grid-column: 1 / -1;
  }

  .pmw-scout-grid {
    grid-template-columns: 1fr;
  }

  .pmw-plan-grid,
  .premium-pricing-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 760px) {
  .pmw-shell {
    padding: 10px;
  }

  .pmw-hero-inner {
    padding: 18px;
  }

  .pmw-title {
    font-size: clamp(40px, 14vw, 58px);
  }

  .pmw-stat-grid,
  .pmw-live-panel .pmw-stat-grid,
  .pmw-plan-grid,
  .premium-pricing-grid {
    grid-template-columns: 1fr !important;
  }

  .pmw-hero-actions,
  .pmw-buy-row,
  .premium-strip-actions {
    flex-direction: column;
  }

  .pmw-action,
  .premium-button,
  .gradio-container button {
    width: 100% !important;
  }

  .product-button-row button {
    width: 100% !important;
  }

  .pmw-export-row {
    grid-template-columns: 1fr;
  }

  .pmw-stadium-hero {
    border-radius: 26px;
  }
}

@media (max-width: 390px) {
  .pmw-title {
    font-size: 39px;
  }

  .pmw-subtitle {
    font-size: 14px;
  }

  .pmw-card,
  .pmw-live-panel,
  .pmw-score-card {
    padding: 14px;
  }
}
"""
'''

FINAL_HERO = r'''
def _premium_matchday_war_room_shell_html(state: dict | None = None) -> str:
    """Production first screen for PremiumMatchdayWarRoom2026.

    Ontology:
    - Free core remains fully judgeable.
    - Premium sells advanced scout cards, exports, fan packs, and source access.
    - Safety: no gambling, no official marks, no paid live-score dependency.
    """
    snap = _pmw_runtime_snapshot(state)
    live_chip_class = "live" if snap["live_enabled"] or snap["live_count"] else ""
    sheet_chip_class = "live" if snap["sheet_connected"] else ""

    return f"""
    <main class="pmw-shell" aria-label="Premium Matchday War Room 2026">
      <section class="pmw-stadium-hero">
        <div class="pmw-hero-inner">
          <div>
            <div class="pmw-kicker">PremiumMatchdayWarRoom2026</div>
            <h1 class="pmw-title">
              AI Bracket<br>
              <span class="pmw-gradient-text">War Room</span>
            </h1>
            <p class="pmw-subtitle">
              A finished premium matchday command center for predictions, brackets,
              squad intelligence, private Friends Leagues, and share-ready exports.
              Built for fans, judgeable without credentials, and safe for sales.
            </p>

            <div class="pmw-chip-row" aria-label="Runtime chips">
              <span class="pmw-chip {live_chip_class}">Live scores: {'ON' if snap["live_enabled"] else 'cache-ready'}</span>
              <span class="pmw-chip {sheet_chip_class}">Google Sheet: {'connected' if snap["sheet_connected"] else 'ready'}</span>
              <span class="pmw-chip">Source: {_pmw_escape(snap["source"])}</span>
              <span class="pmw-chip premium">Premium funnel: $9 / $27 / $49+</span>
            </div>

            <div class="pmw-hero-actions" aria-label="Primary actions">
              <a class="pmw-action primary" href="#match-center">Scroll to Match Center</a>
              <a class="pmw-action secondary" href="#ai-scout">Scroll to AI Scout</a>
              <a class="pmw-action secondary" href="#premium">Scroll to Premium</a>
            </div>
          </div>

          <aside class="pmw-live-panel" aria-label="Live dashboard panel">
            <div class="pmw-score-card">
              <div class="pmw-score-label">Selected / latest match</div>
              <div class="pmw-scoreline">{_pmw_escape(snap["scoreline"])}</div>
              <div class="pmw-source">
                Status: {_pmw_escape(snap["status"])}
                · Last refresh: {_pmw_escape(snap["last_refresh"] or "ready")}
              </div>
            </div>
            {_pmw_dashboard_stats_html(state)}
          </aside>
        </div>
      </section>

      <section class="pmw-dashboard-grid" aria-label="Production dashboard modules">
        {_pmw_ai_scout_cards_html(state)}
        {_pmw_friends_exports_html()}
        {_pmw_free_vs_premium_html()}
      </section>

      <section class="pmw-final-buy-strip" aria-label="Gumroad premium funnel">
        <div class="pmw-card-kicker">Gumroad Funnel</div>
        <h3>Free core for judges. Premium packs for matchday fans.</h3>
        <p>
          Premium Matchday $9 unlocks advanced scout cards and exports.
          Ultimate $27 adds printable and GoodNotes fan assets.
          Source $49+ gives builders the deployable Gradio app bundle.
        </p>
        <div class="pmw-buy-row">
          <a class="pmw-action primary" href="{_pmw_escape(GUMROAD_PREMIUM_URL)}" target="_blank" rel="noopener">Buy Premium Matchday $9</a>
          <a class="pmw-action secondary" href="{_pmw_escape(GUMROAD_PREMIUM_URL)}" target="_blank" rel="noopener">Get Ultimate $27</a>
          <a class="pmw-action secondary" href="{_pmw_escape(GUMROAD_SOURCE_URL)}" target="_blank" rel="noopener">Source Bundle $49+</a>
        </div>
      </section>
    </main>
    """
'''

README_FINAL = r'''
## Final Build Small Submission

**Short description:** Premium World Cup 2026 matchday command center for predictions, brackets, squad analytics, Friends League scoring, and share-ready fan exports.

**Tags:** `gradio`, `agents`, `sports`, `football`, `world-cup-2026`, `bracket`, `predictions`, `fan-tools`, `premium`, `gumroad`, `hackathon`

### Submission Copy

AI Bracket War Room 2026 turns a football fan’s matchday into a live command center: inspect runtime match results, recompute group impact, preview the bracket path, score a private Friends League, and ask AI Scout for tactical context. The free core is fully judgeable without credentials. Premium is a fan-safe monetization layer for exports, advanced scout cards, printable planning assets, ad-free matchday UX, and a Gumroad source bundle.

### Judge Path

1. Open the Space.
2. Confirm the first screen shows the neon stadium hero, dashboard stats, AI Scout Cards, Friends League Exports, and Free vs Premium funnel.
3. Click **Open Match Center**.
4. Inspect a selected match and runtime source.
5. Click **Refresh Runtime** and **Recalculate Impact / War Room**.
6. Open **AI Scout** and generate/preview selected-match context.
7. Open **Friends League** and score demo picks.
8. Open **Premium** and verify Gumroad funnel and locked export previews.
9. Open **Judge QA / Debug** and run demo scenario checks.

### Monetization Funnel

- **Free Core — $0:** runtime match center, group table, third-place ranking, bracket preview, Friends League demo, AI Scout preview, judge QA.
- **Premium Matchday Pack — $9:** advanced AI Scout match cards, scenario CSV exports, Friends League export pack, ad-free matchday mode, share-ready summaries.
- **Ultimate Fan Pack — $27:** GoodNotes/PDF command center, printable sheets, office pool kit, watch-party assets, sticker bundle.
- **Source Bundle — $49+:** deployable Gradio source, premium templates, private league starter kit, commercial setup notes.

### Safety Boundary

This is an unofficial football fan planning and analytics app. It does not provide gambling advice, wagering prices, book integrations, official federation marks, player likeness dependencies, paid live-score requirements, or real-money contest logic. Premium sells planning tools, exports, templates, ad-free UX, and source access.

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
'''


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def insert_final_css(text: str) -> str:
    if "FINAL_PMW2026_PRODUCTION_CSS = r" not in text:
        marker = "SF_PREMIUM_WAR_ROOM_CSS = r"
        idx = text.find(marker)
        if idx == -1:
            raise RuntimeError("SF_PREMIUM_WAR_ROOM_CSS not found")
        start = text.find('"""', idx)
        end = text.find('"""', start + 3)
        if start == -1 or end == -1:
            raise RuntimeError("Cannot locate end of SF_PREMIUM_WAR_ROOM_CSS")
        end += 3
        text = text[:end] + "\n\n" + FINAL_CSS.strip() + "\n" + text[end:]

    old = 'css=PREMIUM_DARK_SPORT_CSS + "\\n" + SF_PREMIUM_WAR_ROOM_CSS'
    new = 'css=PREMIUM_DARK_SPORT_CSS + "\\n" + SF_PREMIUM_WAR_ROOM_CSS + "\\n" + FINAL_PMW2026_PRODUCTION_CSS'
    if old in text and new not in text:
        text = text.replace(old, new, 1)

    for inline_css in (
        '    gr.HTML("<style>" + SF_PREMIUM_WAR_ROOM_CSS + "</style>")\n',
        '    gr.HTML("<style>" + FINAL_PMW2026_PRODUCTION_CSS + "</style>")\n',
    ):
        text = text.replace(inline_css, "")

    return text


def replace_function(text: str, name: str, replacement: str) -> str:
    match = re.search(rf"\ndef {name}\(.*?\n(?=def |\nwith gr\.Blocks|\Z)", text, flags=re.S)
    if not match:
        raise RuntimeError(f"{name} not found")
    return text[:match.start()] + "\n" + replacement.strip() + "\n\n" + text[match.end():]


def patch_buttons_and_labels(text: str) -> str:
    replacements = {
        'ask_ai_scout_button = gr.Button("Ask AI Scout", variant="secondary")':
            'ask_ai_scout_button = gr.Button("Ask AI Scout", variant="secondary")',
        'open_friends_button = gr.Button("Open Friends League", variant="secondary")':
            'open_friends_button = gr.Button("Open Friends League", variant="secondary")',
        'pull_sheet_button = gr.Button("Pull Google Sheet", variant="secondary")':
            'pull_sheet_button = gr.Button("Pull Google Sheet", variant="secondary")',
        'ask_ai_scout_button = gr.Button("Ask AI Scout", variant="secondary", visible=False)':
            'ask_ai_scout_button = gr.Button("Ask AI Scout", variant="secondary")',
        'open_friends_button = gr.Button("Open Friends League", variant="secondary", visible=False)':
            'open_friends_button = gr.Button("Open Friends League", variant="secondary")',
        'pull_sheet_button = gr.Button("Pull Google Sheet", variant="secondary", visible=False)':
            'pull_sheet_button = gr.Button("Pull Google Sheet", variant="secondary")',
        'refresh_live_button = gr.Button("Refresh Runtime", variant="primary")':
            'refresh_live_button = gr.Button("Refresh Runtime", variant="primary", elem_classes=["pmw-primary-action"])',
        'recalc_button = gr.Button("Recalculate Impact / War Room", variant="primary")':
            'recalc_button = gr.Button("Recalculate Impact / War Room", variant="primary", elem_classes=["pmw-primary-action"])',
        'with gr.Tab("️ Match Center", elem_id="match-center"):':
            'with gr.Tab("🏟️ Match Center", elem_id="match-center"):',
        'with gr.Tab(" Match Center", elem_id="match-center"):':
            'with gr.Tab("🏟️ Match Center", elem_id="match-center"):',
        'with gr.Tab(" Groups"):':
            'with gr.Tab("📊 Groups"):',
        'with gr.Tab(" 3RD-PLACE RANKING"):':
            'with gr.Tab("🥉 3RD-PLACE RANKING"):',
        'with gr.Tab(" Bracket"):':
            'with gr.Tab("🧬 Bracket"):',
        'with gr.Tab(" Friends League"):':
            'with gr.Tab("👥 Friends League"):',
        'with gr.Tab(" AI Scout", elem_id="ai-scout"):':
            'with gr.Tab("🤖 AI Scout", elem_id="ai-scout"):',
        'with gr.Tab(" Google Sheet"):':
            'with gr.Tab("🔌 Google Sheet"):',
        'with gr.Tab(" Premium", elem_id="premium"):':
            'with gr.Tab("💎 Premium", elem_id="premium"):',
    }
    for old, new in replacements.items():
        if old in text and new not in text:
            text = text.replace(old, new, 1)
    return text


def patch_readme(path: Path) -> None:
    if not path.exists():
        return
    text = read(path)
    marker = "<!-- FINAL_PMW2026_SUBMISSION_COPY -->"
    block = marker + "\n\n" + README_FINAL.strip() + "\n"
    if marker in text:
        start = text.find(marker)
        tail = text.find("\n# ", start)
        if tail == -1:
            tail = len(text)
        text = text[:start] + block + "\n" + text[tail:].lstrip("\n")
    else:
        if text.startswith("---\n"):
            close = text.find("\n---\n", 4)
            if close == -1:
                raise RuntimeError("README frontmatter does not close cleanly")
            insert_at = close + len("\n---\n")
            text = text[:insert_at] + block + "\n" + text[insert_at:].lstrip("\n")
        else:
            text = block + "\n\n" + text
    write(path, text)


def main() -> int:
    app_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("app.py")
    if not app_path.exists():
        raise SystemExit(f"ERROR: {app_path} not found")

    original = read(app_path)
    text = original

    text = insert_final_css(text)
    text = replace_function(text, "_premium_matchday_war_room_shell_html", FINAL_HERO)
    text = patch_buttons_and_labels(text)

    if text != original:
        backup = app_path.with_suffix(app_path.suffix + ".pre_final_pmw2026.bak")
        if not backup.exists():
            write(backup, original)
        write(app_path, text)
        print(f"Patched {app_path}")
        print(f"Backup: {backup}")
    else:
        print("app.py already patched")

    patch_readme(app_path.with_name("README.md"))

    print("Run:")
    print("  python -m py_compile app.py")
    print("  python -m compileall app.py models src layout scripts")
    print("  python scripts/run_hackathon_smoke_tests.py")
    print("  python scripts/qa_phase_130_runtime_product.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
