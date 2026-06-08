from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.py"
GITIGNORE = ROOT / ".gitignore"
TEST = ROOT / "scripts" / "run_phase_124_integration_acceptance.py"

APP_SNIPPET = r'''

# ==============================================================================
# Phase 1.24: safe scout, CSS Grid bracket, and runtime report artifact
# ==============================================================================
import os
import time
from datetime import datetime
from html import escape
from pathlib import Path as _Path

PHASE_124_MARKER = "PHASE_1_24_SAFE_SCOUT_GRID_EXPORT"
OUTPUT_DIR = _Path("output")
REPORT_PATH = OUTPUT_DIR / "simulation_report.txt"
FORBIDDEN_SCOUT_TERMS = (
    "betting",
    "odds",
    "bookmaker",
    "bookmakers",
    "wager",
    "gambling",
    "ставки",
    "коэффициенты",
    "букмекер",
    "тотализатор",
)


def build_safe_scout_prompt(team_a: str, team_b: str, stage: str, group_id: str = "") -> str:
    context_stage = f"Group {group_id}" if stage == "Group" and group_id else stage or "Tournament"
    return (
        "[SYSTEM]\n"
        "You are a football tactical analyst for AI Bracket War Room 2026. "
        "Write only football tactics: shape, pressing, midfield control, transitions, flanks, and compactness. "
        "Do not mention betting, odds, bookmakers, wagering, gambling, or winner-probability language.\n\n"
        "[MATCH]\n"
        f"Context: {context_stage}\n"
        f"Fixture: {team_a} vs {team_b}\n\n"
        "[TACTICAL SLIP]\n"
        "Return 3 concise bullet points."
    )


def _sanitize_scout_text(text: str) -> str:
    clean = text or ""
    lowered = clean.lower()
    if any(term in lowered for term in FORBIDDEN_SCOUT_TERMS):
        return ""
    return clean.strip()


def fetch_ai_scout_slip(team_a: str, team_b: str, stage: str, group_id: str = "") -> str:
    prompt = build_safe_scout_prompt(team_a, team_b, stage, group_id)
    endpoint = os.getenv("MODAL_LLM_URL", "").strip()
    if endpoint:
        try:
            import requests
            response = requests.post(endpoint, json={"prompt": prompt, "temperature": 0.3, "max_tokens": 180}, timeout=3.5)
            if response.status_code == 200:
                payload = response.json()
                remote_text = _sanitize_scout_text(str(payload.get("text", "")))
                if remote_text:
                    return remote_text
        except Exception:
            pass
    return (
        f"Tactical Slip: {team_a} vs {team_b} ({stage or 'Tournament'}). "
        "Expect a compact midfield battle, with progression decided by pressing triggers, second-ball control, "
        "and the speed of wide transitions. The key coaching focus is rest-defense discipline after turnovers."
    )


def check_modal_gpu_health() -> str:
    endpoint = os.getenv("MODAL_LLM_URL", "").strip()
    if not endpoint:
        return (
            "<div class='sport-card'><h3>AI Infrastructure</h3>"
            "<p><span class='sport-warning'>LOCAL FALLBACK ACTIVE</span> — MODAL_LLM_URL is not configured. "
            "Safe tactical slips remain available through the deterministic local scout.</p></div>"
        )
    started = time.time()
    try:
        import requests
        response = requests.get(endpoint, timeout=2.5)
        latency = int((time.time() - started) * 1000)
        if response.status_code < 500:
            return (
                "<div class='sport-card'><h3>AI Infrastructure</h3>"
                f"<p><span class='sport-success'>MODAL GPU ACTIVE</span> — health check responded in {latency}ms.</p></div>"
            )
    except Exception:
        pass
    return (
        "<div class='sport-card'><h3>AI Infrastructure</h3>"
        "<p><span class='sport-warning'>MODAL GPU COLD START</span> — remote node unavailable; "
        "safe local tactical fallback is serving the demo.</p></div>"
    )


def export_simulation_artifact(matches_df, bracket) -> str:
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        completed = 0
        if matches_df is not None and "Result" in matches_df.columns:
            completed = int(matches_df["Result"].fillna("").astype(str).str.strip().ne("").sum())
        combination = "".join(bracket.get("qualified_third_groups") or []) if isinstance(bracket, dict) else "pending"
        with REPORT_PATH.open("w", encoding="utf-8") as handle:
            handle.write("AI BRACKET WAR ROOM 2026 SIMULATION REPORT\n")
            handle.write(f"Marker: {PHASE_124_MARKER}\n")
            handle.write(f"Timestamp UTC: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n")
            handle.write(f"Completed matches: {completed} / 104\n")
            handle.write(f"Detected third-place combination: {combination or 'pending'}\n")
            handle.write("\nTop planner snapshot:\n")
            if matches_df is not None and not matches_df.empty:
                handle.write(matches_df.head(30).to_string(index=False))
        return str(REPORT_PATH)
    except Exception as exc:
        return f"artifact_export_failed:{exc}"


def _bracket_card(match_id: str, stage: str, team_a: str, team_b: str, highlight: bool = False) -> str:
    border = " style='border-color:#eab308;background:#1c1917;'" if highlight else ""
    return (
        f"<div class='bracket-match-card'{border}>"
        f"<div class='match-header'><span>{escape(match_id)}</span><span>{escape(stage)}</span></div>"
        f"<div class='team-row'><span class='team-name'>{escape(str(team_a))}</span><span class='team-score'>-</span></div>"
        f"<div class='team-row'><span class='team-name'>{escape(str(team_b))}</span><span class='team-score'>-</span></div>"
        "</div>"
    )


def render_css_grid_bracket_view(bracket: dict) -> str:
    matches = (bracket or {}).get("matches", {})
    r32 = [value for value in matches.values() if value.get("stage") == "Round of 32"][:16]
    if not r32:
        r32 = [{"match_id": f"M{idx:03d}", "team_a": "TBD", "team_b": "TBD"} for idx in range(73, 89)]
    r32_cards = "".join(_bracket_card(item.get("match_id", "R32"), "R32", item.get("team_a", "TBD"), item.get("team_b", "TBD")) for item in r32[:8])
    r16_cards = "".join(_bracket_card(f"M{idx:03d}", "R16", f"Winner M{a:03d}", f"Winner M{b:03d}") for idx, a, b in [(89,73,74),(90,75,76),(91,77,78),(92,79,80)])
    qf_cards = "".join(_bracket_card(f"M{idx:03d}", "QF", f"Winner M{a:03d}", f"Winner M{b:03d}") for idx, a, b in [(97,89,90),(98,91,92)])
    sf_cards = _bracket_card("M101", "SF", "Winner M097", "Winner M098") + _bracket_card("M102", "SF", "Winner M099", "Winner M100")
    final_cards = _bracket_card("M104", "FINAL", "Winner M101", "Winner M102", True) + _bracket_card("M103", "3RD", "Loser M101", "Loser M102")
    combination = "".join((bracket or {}).get("qualified_third_groups") or []) or "pending"
    return f"""
    <style>
    .warroom-bracket-container {{display:grid;grid-template-columns:repeat(5,minmax(190px,1fr));gap:20px;background:#09090b;padding:22px;border-radius:14px;overflow-x:auto;border:1px solid #27272a;font-family:monospace;}}
    .bracket-round-column {{display:flex;flex-direction:column;justify-content:space-around;min-height:680px;gap:10px;}}
    .bracket-match-card {{background:#18181b;border:1px solid #27272a;border-radius:8px;padding:10px;box-shadow:0 4px 12px rgba(0,0,0,.45);}}
    .bracket-match-card:hover {{border-color:#3b82f6;background:#202024;}}
    .match-header {{font-size:11px;color:#a1a1aa;margin-bottom:7px;border-bottom:1px solid #27272a;padding-bottom:5px;display:flex;justify-content:space-between;}}
    .team-row {{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:#f4f4f5;padding:3px 0;}}
    .team-name {{font-weight:650;}}
    .team-score {{font-weight:800;color:#60a5fa;}}
    .active-combination-badge {{background:#1e1b4b;color:#c4b5fd;padding:8px 12px;border-radius:8px;border:1px solid #312e81;margin-bottom:12px;font-size:13px;font-weight:700;}}
    </style>
    <div class='active-combination-badge'>FIFA Annex C third-place combination: {escape(combination)}</div>
    <div class='warroom-bracket-container'>
      <div class='bracket-round-column'>{r32_cards}</div>
      <div class='bracket-round-column'>{r16_cards}</div>
      <div class='bracket-round-column'>{qf_cards}</div>
      <div class='bracket-round-column'>{sf_cards}</div>
      <div class='bracket-round-column'>{final_cards}</div>
    </div>
    """


def build_tactical_slip_from_selection(evt, matches_df):
    try:
        row_index = evt.index[0] if isinstance(evt.index, (list, tuple)) else evt.index
        row = matches_df.iloc[int(row_index)]
        team_a = str(row.get("Home", row.get("Team A", row.get("Team_A", "Team A"))))
        team_b = str(row.get("Away", row.get("Team B", row.get("Team_B", "Team B"))))
        stage = str(row.get("Phase", row.get("Stage", "Group")))
        group_id = str(row.get("Group_ID", row.get("Group", "")))
        return f"Selected fixture: {team_a} vs {team_b}\n\n" + fetch_ai_scout_slip(team_a, team_b, stage, group_id)
    except Exception as exc:
        return f"Tactical Slip unavailable: {exc}"
'''

TEST_CONTENT = '''from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import app


def main() -> None:
    assert hasattr(app, "PHASE_124_MARKER")
    assert app.PHASE_124_MARKER == "PHASE_1_24_SAFE_SCOUT_GRID_EXPORT"
    prompt = app.build_safe_scout_prompt("Team A", "Team B", "Group", "A")
    lowered_prompt = prompt.lower()
    assert "betting" in lowered_prompt and "odds" in lowered_prompt
    slip = app.fetch_ai_scout_slip("Team A", "Team B", "Group", "A")
    for forbidden in app.FORBIDDEN_SCOUT_TERMS:
        assert forbidden not in slip.lower(), f"forbidden term leaked: {forbidden}"
    state = app.initial_load()[0]
    outputs = app.load_demo_scenario_outputs(state)
    bracket = outputs[4]
    html = app.render_css_grid_bracket_view(bracket)
    assert "warroom-bracket-container" in html
    assert "FIFA Annex C third-place combination" in html
    path = app.export_simulation_artifact(outputs[1], bracket)
    assert Path(path).exists(), path
    assert app.PHASE_124_MARKER in Path(path).read_text(encoding="utf-8")
    print("PHASE_124_INTEGRATION_ACCEPTANCE_PASS")


if __name__ == "__main__":
    main()
'''


def insert_once(text: str, marker: str, snippet: str) -> str:
    if marker in text:
        return text
    return text + snippet


def patch_app() -> None:
    text = APP.read_text(encoding="utf-8")
    text = insert_once(text, "PHASE_1_24_SAFE_SCOUT_GRID_EXPORT", APP_SNIPPET)
    text = text.replace(
        "bracket_summary = _bracket_html(bracket)",
        "bracket_summary = render_css_grid_bracket_view(bracket)",
    )
    text = text.replace(
        "impact_panel = build_impact_panel_html(matches_df, groups, thirds, bracket, friends)\n    return working_state, matches_df, groups, thirds, bracket, bracket_summary, friends, dashboard, top_checklist, ai_scout, impact_panel",
        "export_simulation_artifact(matches_df, bracket)\n    impact_panel = build_impact_panel_html(matches_df, groups, thirds, bracket, friends)\n    return working_state, matches_df, groups, thirds, bracket, bracket_summary, friends, dashboard, top_checklist, ai_scout, impact_panel",
    )
    text = text.replace(
        "top_checklist_html = gr.HTML(value=_scenario_controls_html())",
        "top_checklist_html = gr.HTML(value=_scenario_controls_html())\n    modal_gpu_status_html = gr.HTML(value=check_modal_gpu_health())\n    tactical_slip_box = gr.Textbox(label=\"AI Scout Tactical Slip — click any Match Planner row\", lines=5, interactive=False)",
    )
    if "matches_df.select(" not in text:
        text = text.replace(
            "load_demo_button.click(\n        load_demo_scenario_outputs,",
            "matches_df.select(\n        build_tactical_slip_from_selection,\n        inputs=[matches_df],\n        outputs=[tactical_slip_box],\n    )\n    load_demo_button.click(\n        load_demo_scenario_outputs,",
        )
    APP.write_text(text, encoding="utf-8")


def patch_gitignore() -> None:
    existing = GITIGNORE.read_text(encoding="utf-8") if GITIGNORE.exists() else ""
    additions = [
        "output/**/*.txt",
        "*.zip",
        "*.mp4",
        "*.mov",
        "*.avi",
        "*.mkv",
        "*.psd",
        "*.ai",
        "*.fig",
    ]
    lines = existing.splitlines()
    for item in additions:
        if item not in lines:
            lines.append(item)
    GITIGNORE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    if not APP.exists():
        raise SystemExit("app.py not found; run this script from repository root.")
    patch_app()
    patch_gitignore()
    TEST.parent.mkdir(parents=True, exist_ok=True)
    TEST.write_text(TEST_CONTENT, encoding="utf-8")
    print("PHASE_124_PATCH_APPLIED")


if __name__ == "__main__":
    main()
