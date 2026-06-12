PREMIUM_DARK_SPORT_CSS = """
/* PHASE 1.30B Visual Surface + AppStore Shell */
:root {
    --abw-navy: #07111F;
    --abw-surface: #F8FAFC;
    --abw-card: #FFFFFF;
    --abw-live: #10B981;
    --abw-pending: #F59E0B;
    --abw-alert: #EF4444;
    --abw-text: #0F172A;
    --abw-muted: #64748B;
    --abw-border: #CBD5E1;
    --abw-soft-border: #E2E8F0;
    --abw-shadow: 0 14px 34px rgba(15, 23, 42, 0.10);
}

body,
.gradio-container {
    background: var(--abw-navy) !important;
    color: var(--abw-text) !important;
}

.gradio-container {
    max-width: 1180px !important;
    margin: 0 auto !important;
    padding: 18px !important;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

.gradio-container > .main,
.gradio-container .contain {
    background: var(--abw-surface) !important;
}

.abw-app-shell,
.sport-card,
.table-card,
.app-card,
.card-shell {
    background: var(--abw-card) !important;
    border: 1px solid var(--abw-border) !important;
    border-radius: 16px !important;
    box-shadow: var(--abw-shadow) !important;
    color: var(--abw-text) !important;
    margin: 0 0 16px !important;
    opacity: 1 !important;
}

.abw-app-shell {
    overflow: hidden;
}

.abw-topbar {
    align-items: center;
    background: var(--abw-navy) !important;
    color: #FFFFFF !important;
    display: flex;
    gap: 12px;
    justify-content: space-between;
    padding: 14px 18px;
}

.abw-brand {
    align-items: center;
    display: flex;
    gap: 12px;
    min-width: 0;
}

.abw-mark {
    align-items: center;
    background: #FFFFFF !important;
    border-radius: 12px;
    color: var(--abw-navy) !important;
    display: inline-flex;
    flex: 0 0 auto;
    font-size: 15px;
    font-weight: 900;
    height: 42px;
    justify-content: center;
    letter-spacing: 0;
    width: 42px;
}

.abw-title {
    color: #FFFFFF !important;
    font-size: 16px;
    font-weight: 900;
    line-height: 1.15;
}

.abw-subtitle {
    color: #CBD5E1 !important;
    font-size: 12px;
    font-weight: 700;
    line-height: 1.2;
}

.abw-phase-marker {
    background: rgba(16, 185, 129, 0.14) !important;
    border: 1px solid rgba(16, 185, 129, 0.55) !important;
    border-radius: 999px;
    color: #D1FAE5 !important;
    flex: 0 0 auto;
    font-size: 12px;
    font-weight: 900;
    padding: 7px 10px;
}

.abw-shell-body,
.sport-card,
.table-card {
    padding: 20px !important;
}

.abw-hero-grid {
    display: grid;
    gap: 16px;
    grid-template-columns: minmax(0, 1.5fr) minmax(280px, 0.85fr);
}

.abw-kicker,
.sport-kicker,
.sport-label {
    color: var(--abw-muted) !important;
    font-size: 12px !important;
    font-weight: 900 !important;
    letter-spacing: 0 !important;
    text-transform: uppercase;
}

.abw-app-shell h1,
.sport-hero h1,
.sport-card h1 {
    color: var(--abw-text) !important;
    font-size: 30px !important;
    font-weight: 900 !important;
    letter-spacing: 0 !important;
    line-height: 1.08 !important;
    margin: 6px 0 8px !important;
}

.abw-app-shell h2,
.sport-card h2,
.sport-card h3,
.sport-card h4,
.table-card h3,
.table-card h4 {
    color: var(--abw-text) !important;
    font-weight: 900 !important;
    letter-spacing: 0 !important;
    margin: 0 0 8px !important;
}

.abw-app-shell p,
.sport-card p,
.sport-card li,
.sport-card ol,
.sport-card ul,
.sport-card strong,
.sport-card span,
.table-card p,
.table-card span,
.table-card strong {
    color: var(--abw-text) !important;
    opacity: 1 !important;
}

.sport-muted,
.abw-muted {
    color: var(--abw-muted) !important;
}

.abw-chip-row,
.sport-badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 14px 0 0;
}

.abw-chip,
.sport-proof-badge,
.sport-badge-row span {
    background: #F1F5F9 !important;
    border: 1px solid var(--abw-border) !important;
    border-radius: 999px !important;
    color: var(--abw-text) !important;
    display: inline-flex !important;
    font-size: 12px !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    padding: 7px 10px !important;
}

.abw-chip.live,
.sport-pass,
.sport-success {
    background: rgba(16, 185, 129, 0.12) !important;
    border-color: rgba(16, 185, 129, 0.35) !important;
    color: #047857 !important;
    font-weight: 900 !important;
}

.abw-chip.pending,
.sport-pending,
.sport-accent {
    background: rgba(245, 158, 11, 0.12) !important;
    border-color: rgba(245, 158, 11, 0.35) !important;
    color: #92400E !important;
    font-weight: 900 !important;
}

.abw-chip.alert,
.sport-warning {
    background: rgba(239, 68, 68, 0.12) !important;
    border-color: rgba(239, 68, 68, 0.35) !important;
    color: #B91C1C !important;
    font-weight: 900 !important;
}

.abw-runtime-strip {
    display: grid;
    gap: 8px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.abw-runtime-tile {
    background: #F8FAFC !important;
    border: 1px solid var(--abw-soft-border) !important;
    border-radius: 12px;
    padding: 12px;
}

.abw-runtime-tile b {
    color: var(--abw-text) !important;
    display: block;
    font-size: 18px;
    line-height: 1.1;
}

.abw-runtime-tile span {
    color: var(--abw-muted) !important;
    font-size: 12px;
    font-weight: 800;
}

.sport-hero {
    background: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: var(--abw-text) !important;
    margin: 0 !important;
    padding: 0 !important;
}

.phase126-metrics,
.sport-impact-grid {
    display: grid;
    gap: 8px;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    margin-top: 14px;
}

.phase126-metric,
.sport-impact-grid > div {
    background: #F8FAFC !important;
    border: 1px solid var(--abw-soft-border) !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

.phase126-metric b,
.sport-impact-grid strong {
    color: var(--abw-text) !important;
}

.phase126-metric span {
    color: var(--abw-muted) !important;
}

.sport-demo-rail {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 14px 0;
}

.sport-demo-rail span {
    background: #F8FAFC !important;
    border: 1px solid var(--abw-border) !important;
    border-radius: 999px;
    color: var(--abw-text) !important;
    font-size: 12px;
    font-weight: 800;
    padding: 7px 10px;
}

.app-icon-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 16px 0 0;
}

.app-nav-pill {
    align-items: center;
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 999px;
    color: #0F172A !important;
    display: inline-flex;
    font-size: 13px;
    font-weight: 900;
    min-height: 36px;
    padding: 8px 12px;
}

.appstore-first-screen {
    background: #F8FAFC !important;
    display: grid;
    gap: 16px;
    margin: 0 0 16px !important;
}

.app-card,
.card-shell {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 16px !important;
    box-shadow: var(--abw-shadow) !important;
    color: #0F172A !important;
    margin-bottom: 16px !important;
    min-height: 120px !important;
    overflow: visible !important;
    padding: 20px !important;
}

.today-match-center {
    display: grid;
    gap: 12px;
}

.module-kicker {
    color: #64748B !important;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 0 !important;
    text-transform: uppercase;
}

.today-scoreline {
    color: #0F172A !important;
    font-size: 28px;
    font-weight: 950;
    letter-spacing: 0;
    line-height: 1.08;
}

.today-meta {
    color: #047857 !important;
    font-size: 14px;
    font-weight: 900;
}

.today-module-grid,
.product-module-grid {
    display: grid;
    gap: 16px;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.mini-module,
.module-card {
    background: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 16px;
    padding: 16px;
}

.mini-module span,
.module-card p {
    color: #64748B !important;
    font-size: 13px;
    font-weight: 750;
}

.mini-module strong,
.module-card h3 {
    color: #0F172A !important;
    display: block;
    font-size: 16px;
    font-weight: 900;
    margin: 4px 0 0;
}

.next-action-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.next-action-row span {
    background: #10B981 !important;
    border: 1px solid #10B981 !important;
    border-radius: 999px;
    color: #FFFFFF !important;
    font-size: 12px;
    font-weight: 900;
    padding: 8px 12px;
}

.table-card {
    overflow: hidden;
}

.table-card .table-scroll {
    background: #FFFFFF !important;
    border: 1px solid var(--abw-border) !important;
    border-radius: 12px;
    overflow-x: auto;
}

.runtime-skeleton {
    background: #F8FAFC !important;
    border: 1px dashed var(--abw-border) !important;
    border-radius: 12px;
    color: var(--abw-muted) !important;
    font-weight: 800;
    margin: 10px 0 12px;
    padding: 12px;
}

.lower-surface-card,
.table-skeleton-card,
.runtime-card,
.gradio-container .phase126-shell,
.gradio-container .phase126-card,
.gradio-container .phase126-match-card,
.gradio-container .phase126r-card {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 16px !important;
    color: #0F172A !important;
    margin-bottom: 16px !important;
    min-height: 120px !important;
    overflow: visible !important;
    padding: 16px !important;
}

.table-skeleton-card {
    background: #F8FAFC !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
    margin: 0 0 16px !important;
}

.table-skeleton-card strong {
    color: #0F172A !important;
    font-size: 15px !important;
    font-weight: 900 !important;
}

.table-skeleton-card span {
    color: #64748B !important;
    font-size: 13px !important;
    font-weight: 800 !important;
}

.runtime-skeleton {
    min-height: 0 !important;
}

.gradio-container .gap,
.gradio-container .form,
.gradio-container .block,
.gradio-container .tabitem {
    margin-bottom: 24px !important;
}

table,
.table-wrap,
.gradio-dataframe,
.dataframe,
.ag-root-wrapper,
.ag-root,
.ag-center-cols-viewport,
.ag-center-cols-container,
.ag-body-viewport,
.ag-body-horizontal-scroll-viewport {
    background: #FFFFFF !important;
    color: var(--abw-text) !important;
}

table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    min-width: 100%;
}

th {
    background: #F1F5F9 !important;
    border-bottom: 1px solid var(--abw-border) !important;
    color: var(--abw-text) !important;
    font-weight: 900 !important;
    padding: 10px !important;
    text-align: left !important;
}

td {
    background: #FFFFFF !important;
    border-bottom: 1px solid #E2E8F0 !important;
    color: var(--abw-text) !important;
    padding: 10px !important;
}

.ag-header,
.ag-header-cell,
.ag-header-cell-label,
.ag-header-cell-text {
    background: #F1F5F9 !important;
    color: var(--abw-text) !important;
    font-weight: 900 !important;
}

.ag-row,
.ag-cell {
    background: #FFFFFF !important;
    color: var(--abw-text) !important;
}

.block,
.form,
.panel,
.tabitem,
.tabs {
    background: var(--abw-surface) !important;
}

button.primary,
.gr-button-primary,
button[variant='primary'] {
    background: var(--abw-live) !important;
    border-color: var(--abw-live) !important;
    color: #FFFFFF !important;
    font-weight: 900 !important;
}

button,
.gr-button {
    border-radius: 12px !important;
    font-weight: 800 !important;
}

.tab-nav button,
.tabitem button,
[role='tab'] {
    color: var(--abw-muted) !important;
    font-weight: 800 !important;
}

.tab-nav button.selected,
[role='tab'][aria-selected='true'] {
    color: var(--abw-text) !important;
}

input,
textarea,
select {
    background: #FFFFFF !important;
    border-color: var(--abw-border) !important;
    color: var(--abw-text) !important;
}

@media (max-width: 760px) {
    .gradio-container {
        padding: 10px !important;
    }

    .abw-topbar,
    .abw-hero-grid {
        align-items: flex-start;
        flex-direction: column;
        grid-template-columns: 1fr;
    }

    .abw-runtime-strip {
        grid-template-columns: 1fr;
    }
}
"""
