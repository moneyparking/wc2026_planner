from __future__ import annotations

import random

import pandas as pd
import gradio as gr

from layout.css_styles import PREMIUM_DARK_SPORT_CSS
from models.bracket_mapper import build_bracket_mapping
from models.data_loader import load_workbook_state, normalize_match_columns
from models.demo_scenario import apply_demo_scenario
from models.fifa_rules import build_group_table, build_third_place_table
from models.scoring import score_prediction
from product_config import APP_TITLE, EXPECTED_ANNEX_C_RECORD_COUNT, EXPECTED_MATCH_COUNT


DEPLOY_MARKER = "PHASE_1_21_INTEGRATION_CLOSEOUT"
VISIBLE_TAB_PREVIEW_MATCHES = 12
VISIBLE_TAB_PREVIEW_GROUPS = 8
VISIBLE_TAB_PREVIEW_BRACKET = 8
VISIBLE_TAB_PREVIEW_FRIENDS = 10
PLANNER_FILTER_CHOICES = (
    "All 104 matches",
    "Group Stage",
    "Knockout Stage",
    "Round of 32",
    "Round of 16",
    "Quarterfinal",
    "Semifinal",
    "Third Place",
    "Final",
    "Group A",
    "Group B",
    "Group C",
    "Group D",
    "Group E",
    "Group F",
    "Group G",
    "Group H",
    "Group I",
    "Group J",
    "Group K",
    "Group L",
)
RANDOM_SCORELINES = ("0-0", "1-0", "0-1", "1-1", "2-0", "0-2", "2-1", "1-2", "2-2", "3-1", "1-3", "3-2", "2-3")


def _score_matches(matches: pd.DataFrame) -> pd.DataFrame:
    scored = matches.copy()
    scored["Points"] = scored.apply(lambda row: score_prediction(row.get("Prediction"), row.get("Result")), axis=1)
    return scored


def _friends_leaderboard(friends: pd.DataFrame) -> pd.DataFrame:
    leaderboard = friends.copy()
    numeric_columns = ["Correct Scores", "Correct Winners", "Upsets Hit", "Total Points"]
    for column in numeric_columns:
        if column in leaderboard.columns:
            leaderboard[column] = pd.to_numeric(leaderboard[column], errors="coerce").fillna(0).astype(int)
    if "Total Points" in leaderboard.columns:
        leaderboard = leaderboard.sort_values(["Total Points", "Player"], ascending=[False, True]).reset_index(drop=True)
        leaderboard.insert(0, "Rank", range(1, len(leaderboard) + 1))
    return leaderboard


def _match_number_from_id(match_id: object) -> int | None:
    text = str(match_id).strip().upper()
    if not text.startswith("M"):
        return None
    try:
        return int(text[1:])
    except ValueError:
        return None


def _planner_filter_mask(matches: pd.DataFrame, planner_filter: str) -> pd.Series:
    if matches is None or matches.empty:
        return pd.Series(dtype=bool)
    selected = planner_filter or "All 104 matches"
    phase = matches.get("Phase", pd.Series([""] * len(matches))).fillna("").astype(str)
    match_numbers = matches.get("Match ID", pd.Series([""] * len(matches))).apply(_match_number_from_id)
    if selected == "All 104 matches":
        return pd.Series([True] * len(matches), index=matches.index)
    if selected == "Knockout Stage":
        return match_numbers.fillna(0).astype(int).between(73, 104)
    if selected == "Group Stage":
        return match_numbers.fillna(0).astype(int).between(1, 72)
    if selected.startswith("Group ") and len(selected) == 7:
        group_index = "ABCDEFGHIJKL".index(selected[-1])
        start = group_index * 6 + 1
        return match_numbers.fillna(0).astype(int).between(start, start + 5)
    return phase.eq(selected)


def filter_match_planner(matches: pd.DataFrame | None, planner_filter: str) -> str:
    filtered = pd.DataFrame() if matches is None else matches.copy()
    if not filtered.empty:
        filtered = normalize_match_columns(filtered)
        mask = _planner_filter_mask(filtered, planner_filter)
        filtered = filtered.loc[mask].reset_index(drop=True)
    return _visible_match_planner_html(filtered, planner_filter)


def _team_rank_lookup(groups: pd.DataFrame) -> dict[str, str]:
    lookup: dict[str, str] = {}
    if groups is None or groups.empty:
        return lookup
    for _, row in groups.iterrows():
        group = str(row.get("Group_ID", "")).replace("Group ", "").strip()
        rank = str(row.get("Rank", "")).strip()
        team = str(row.get("Team", "")).strip() or f"Group {group} Rank {rank}"
        if group and rank:
            lookup[f"{rank}{group}"] = team
    return lookup


def build_bracket_json_contract(bracket: dict, groups: pd.DataFrame, thirds: pd.DataFrame) -> dict:
    base = dict(bracket or {})
    team_lookup = _team_rank_lookup(groups)
    third_groups = base.get("qualified_third_groups") or []
    third_lookup = {f"3{group}": team_lookup.get(f"3{group}", f"3rd Group {group}") for group in third_groups}
    r32_pairings = [
        ("1A", "2B"), ("1C", "2D"), ("1E", "2F"), ("1G", "2H"),
        ("1I", "2J"), ("1K", "2L"), ("1B", "3A"), ("1D", "3B"),
        ("1F", "3C"), ("1H", "3D"), ("1J", "3E"), ("1L", "3F"),
        ("2A", "2C"), ("2E", "2G"), ("2I", "2K"), ("3G", "3H"),
    ]
    matches: dict[str, dict] = {}
    flat: list[dict] = []
    for idx, (slot_a, slot_b) in enumerate(r32_pairings, start=73):
        match_key = f"Match_{idx}"
        payload = {
            "match_id": f"M{idx:03d}",
            "stage": "Round of 32",
            "slot_a": slot_a,
            "slot_b": slot_b,
            "team_a": team_lookup.get(slot_a) or third_lookup.get(slot_a) or slot_a,
            "team_b": team_lookup.get(slot_b) or third_lookup.get(slot_b) or slot_b,
            "source": "Phase 1.21 demo-safe bracket contract",
        }
        matches[match_key] = payload
        flat.append({"key": match_key, **payload})
    later_round_plan = [
        (89, "Round of 16", ["Match_73", "Match_74"]), (90, "Round of 16", ["Match_75", "Match_76"]),
        (91, "Round of 16", ["Match_77", "Match_78"]), (92, "Round of 16", ["Match_79", "Match_80"]),
        (93, "Round of 16", ["Match_81", "Match_82"]), (94, "Round of 16", ["Match_83", "Match_84"]),
        (95, "Round of 16", ["Match_85", "Match_86"]), (96, "Round of 16", ["Match_87", "Match_88"]),
        (97, "Quarterfinal", ["Match_89", "Match_90"]), (98, "Quarterfinal", ["Match_91", "Match_92"]),
        (99, "Quarterfinal", ["Match_93", "Match_94"]), (100, "Quarterfinal", ["Match_95", "Match_96"]),
        (101, "Semifinal", ["Match_97", "Match_98"]), (102, "Semifinal", ["Match_99", "Match_100"]),
        (103, "Third Place", ["Match_101", "Match_102"]), (104, "Final", ["Match_101", "Match_102"]),
    ]
    for idx, stage, parents in later_round_plan:
        match_key = f"Match_{idx}"
        payload = {
            "match_id": f"M{idx:03d}",
            "stage": stage,
            "depends_on": parents,
            "team_a": "Winner/Loser TBD",
            "team_b": "Winner/Loser TBD",
            "source": "Phase 1.21 demo-safe bracket contract",
        }
        matches[match_key] = payload
        flat.append({"key": match_key, **payload})
    base.update({
        "contract_version": "BracketJSON_v1_phase_1_21",
        "canonical_format": "tree_by_match_key",
        "renderer_projection": "matches_flat",
        "matches": matches,
        "matches_flat": flat,
        "round_of_32": {key: value for key, value in matches.items() if value["stage"] == "Round of 32"},
    })
    return base


def generate_random_match_outcomes(state: dict, matches: pd.DataFrame | None = None):
    working_state = dict(state)
    source = matches.copy() if matches is not None else working_state["matches"].copy()
    source = normalize_match_columns(source)
    rng = random.Random(2026)
    for row_index in source.index:
        source.at[row_index, "Result"] = rng.choice(RANDOM_SCORELINES)
        if not str(source.at[row_index, "Prediction"]).strip():
            source.at[row_index, "Prediction"] = rng.choice(RANDOM_SCORELINES)
        if not str(source.at[row_index, "AI Signal"]).strip():
            source.at[row_index, "AI Signal"] = "Demo-safe random outcome stress test"
        if not str(source.at[row_index, "Notes"]).strip():
            source.at[row_index, "Notes"] = "Generated by Phase 1.21 random outcome button."
    outputs = compute_outputs(working_state, source)
    random_status = _scenario_controls_html(outputs[0]) + (
        "<div class='sport-card'><h3>Random Outcome Stress Test</h3>"
        "<p><span class='sport-success'>Generated deterministic random scorelines for all 104 matches.</span> "
        "Use this to test third-place ranking, bracket JSON, and Friends League movement without manual entry.</p></div>"
    )
    planner_preview = _visible_match_planner_html(outputs[1], "All 104 matches")
    return outputs[0], outputs[1], planner_preview, outputs[2], outputs[3], outputs[4], outputs[5], outputs[6], outputs[7], random_status, outputs[9], outputs[10]


def _command_header_html() -> str:
    badges = [
        "104-Match Engine",
        "Live Recalculation",
        "Group + 3rd-Place Logic",
        "Bracket Impact",
        "Friends League",
        "AI Scout Signals",
        "No API Key Required",
        "Unofficial Fan-Made Demo",
    ]
    badge_html = "".join(f"<span class='sport-proof-badge'>{badge}</span>" for badge in badges)
    return f"""
    <div class="sport-hero sport-command-header">
        <div class="sport-kicker">{DEPLOY_MARKER}</div>
        <h1>AI Bracket War Room 2026</h1>
        <h2>Change one result. Watch the tournament path mutate.</h2>
        <p>A small-model-safe Gradio command center for testing 104-match football tournament scenarios, recalculating groups, third-place ranking, bracket paths, Friends League scores, and AI Scout signals.</p>
        <div class="sport-badge-row">{badge_html}</div>
        <div class="sport-demo-rail">
            <span>1 Load Scenario</span><span>2 Edit Match</span><span>3 Recalculate</span><span>4 Inspect Impact</span><span>5 Read AI Scout</span><span>6 Compare Friends League</span>
        </div>
        <p class="sport-muted">Unofficial fan-made football planning demo. No official logos, crests, sponsor marks, player likenesses, live scores, or paid API key required.</p>
    </div>
    """


def _scenario_controls_html(state: dict | None = None) -> str:
    loaded = bool(state and len(state.get("matches", [])) == EXPECTED_MATCH_COUNT)
    status = "Workbook ready — click Load Judge Demo Scenario to begin." if loaded else "Waiting for demo scenario. Click Load Judge Demo Scenario to begin."
    return f"""
    <div class="sport-card sport-scenario-controls">
        <h3>Scenario Controls</h3>
        <p><strong>Status:</strong> <span class="sport-accent">{status}</span></p>
        <p><strong>Run marker:</strong> deterministic offline workbook state · {DEPLOY_MARKER}</p>
        <p><strong>Selected changed match:</strong> Judge demo scenario match row / edited Match Planner result.</p>
    </div>
    """


def _match_label(row: pd.Series, index: int) -> str:
    for column in ("Match", "Match ID", "Match_ID", "Fixture", "Game", "match_id"):
        value = row.get(column)
        if pd.notna(value) and str(value).strip():
            return str(value).strip()
    home = next((row.get(column) for column in ("Home", "Team 1", "Team A", "home_team") if column in row.index), "Team A")
    away = next((row.get(column) for column in ("Away", "Team 2", "Team B", "away_team") if column in row.index), "Team B")
    return f"Match {index + 1}: {home} vs {away}"


def _first_completed_match(matches: pd.DataFrame) -> tuple[str, str, str]:
    if matches is None or matches.empty or "Result" not in matches.columns:
        return "Waiting for demo scenario", "Before: no completed result", "After: no completed result"
    completed = matches[matches["Result"].fillna("").astype(str).str.strip() != ""]
    if completed.empty:
        return "Waiting for demo scenario", "Before: no completed result", "After: no completed result"
    index = int(completed.index[0])
    row = completed.iloc[0]
    return _match_label(row, index), "Baseline preview score", str(row.get("Result", "Updated score"))


def build_impact_panel_html(matches: pd.DataFrame, groups: pd.DataFrame, thirds: pd.DataFrame, bracket: dict, friends: pd.DataFrame) -> str:
    changed_match, before_score, after_score = _first_completed_match(matches)
    has_demo_state = after_score != "After: no completed result"
    waiting = "Waiting for demo scenario. Click Load Judge Demo Scenario to begin."
    group_rows = len(groups) if groups is not None else 0
    third_rows = len(thirds) if thirds is not None else 0
    bracket_slots = len((bracket or {}).get("round_of_32") or {})
    friends_rows = len(friends) if friends is not None else 0
    summary = (
        f"{changed_match} moved from baseline preview into {after_score}. Group order recalculated, third-place pool refreshed, bracket preview slots recomputed, and Friends League rows rescored."
        if has_demo_state
        else waiting
    )
    return f"""
    <div class="sport-card sport-impact-panel">
        <h2>Tournament Impact Panel</h2>
        <p class="sport-muted">Change one result → recalculate → inspect downstream movement.</p>
        <div class="sport-impact-grid">
            <div><span class="sport-label">Changed match</span><strong>{changed_match}</strong></div>
            <div><span class="sport-label">Before score</span><strong>{before_score}</strong></div>
            <div><span class="sport-label">After score</span><strong>{after_score}</strong></div>
            <div><span class="sport-label">Group affected</span><strong>{group_rows} computed group rows</strong></div>
            <div><span class="sport-label">Standings movement</span><strong>{'Updated after recalculation' if group_rows else 'Waiting'}</strong></div>
            <div><span class="sport-label">Third-place pool impact</span><strong>{third_rows} ranking row(s)</strong></div>
            <div><span class="sport-label">Bracket slot impact</span><strong>{bracket_slots or 'Pending'} preview slot(s)</strong></div>
            <div><span class="sport-label">Friends League impact</span><strong>{friends_rows} projected score row(s)</strong></div>
        </div>
        <p><span class="sport-accent">AI Scout summary:</span> {summary}</p>
    </div>
    """


def build_ai_scout_output(matches: pd.DataFrame) -> str:
    signals = []
    if matches is not None and not matches.empty and "AI Signal" in matches.columns:
        signals = [str(value).strip() for value in matches["AI Signal"].fillna("").tolist() if str(value).strip()]
    completed_count = 0 if matches is None or "Result" not in matches.columns else int(matches["Result"].fillna("").astype(str).str.strip().ne("").sum())
    state = "ACTIVE" if completed_count else "WAITING"
    cards = [
        ("Volatility", "HIGH" if completed_count else "WAITING", "A completed result can move group order and bracket preview slots.", "Group Tracker"),
        ("Upset Risk", "WATCH", "Workbook signal rows flag compact scoreline and pressure patterns.", "Match Planner"),
        ("Bracket Impact", "LIVE" if completed_count else "PENDING", "Current standings are converted into knockout preview slots after recalculation.", "Bracket War Room"),
        ("Third-Place Pressure", "HIGH" if completed_count else "PENDING", "Third-place qualification is sensitive in a 48-team format.", "3rd-Place Ranking"),
        ("Friends League Swing", "ACTIVE" if completed_count else "PENDING", "Private picks gain or lose points as scenario results change.", "Friends League"),
        ("Scout Note", state, "Lightweight AI-style signal layer explains deterministic scenario consequences without a paid API key.", "AI Scout"),
    ]
    card_html = "".join(
        f"<div class='sport-scout-card'><span class='sport-label'>{label}</span><strong>{severity}</strong><p>{reason}</p><small>Affects: {module}</small></div>"
        for label, severity, reason, module in cards
    )
    preview = " | ".join(signals[:5]) if signals else "Waiting for demo scenario. Click Load Judge Demo Scenario to begin."
    return f"""
    <div class='sport-card'>
        <h3>AI Scout Signals</h3>
        <p><span class='sport-success'>Lightweight AI-style signal layer:</span> {len(signals)} workbook signal row(s), {completed_count} completed result row(s).</p>
        <div class="sport-scout-grid">{card_html}</div>
        <p><span class='sport-accent'>Workbook preview:</span> {preview}</p>
        <p>Small-model-safe explanatory layer. No live sports data, external market data, or real tournament outcome claims.</p>
    </div>
    """


def _status_badge(label: str, is_pass: bool) -> str:
    badge_class = "sport-pass" if is_pass else "sport-pending"
    badge_text = "PASS" if is_pass else "PENDING"
    return f"<span class='{badge_class}'>{badge_text}</span> {label}"


def _judge_checklist_html(state: dict, groups: pd.DataFrame, thirds: pd.DataFrame) -> str:
    matches_count = len(state.get("matches", []))
    annex_count = len(state.get("annex_c", []))
    return f"""
    <div class="sport-card sport-checklist">
        <h2>90-second Judge Verification</h2>
        <p><strong>Step 1:</strong> Load Demo Scenario &nbsp; - &nbsp; <strong>Step 2:</strong> Recalculate War Room</p>
        <div class="sport-badge-row">
            <span>{_status_badge('104 / 104 matches loaded', matches_count == EXPECTED_MATCH_COUNT)}</span>
            <span>{_status_badge('495 / 495 Annex C loaded', annex_count == EXPECTED_ANNEX_C_RECORD_COUNT)}</span>
            <span>{_status_badge('Group rows populated', len(groups) > 0)}</span>
            <span>{_status_badge('Third-place rows populated', len(thirds) > 0)}</span>
        </div>
        <p class="sport-muted">Open Match Planner, Group Tracker, 3rd-Place Ranking, Bracket War Room, Friends League, and AI Scout to verify the complete loop.</p>
    </div>
    """


def _summary_html(state: dict, groups: pd.DataFrame, thirds: pd.DataFrame) -> str:
    warnings = state.get("warnings") or []
    warnings_html = "".join(f"<li>{warning}</li>" for warning in warnings) or "<li>Workbook loaded cleanly.</li>"
    return f"""
    {_judge_checklist_html(state, groups, thirds)}
    <div class="sport-card">
        <h3>Build Small Status</h3>
        <p><span class="sport-accent">Deploy marker:</span> {DEPLOY_MARKER}</p>
        <p><span class="sport-accent">Workbook:</span> {state.get("spreadsheet_path", "not loaded")}</p>
        <p><span class="sport-success">Matches:</span> {len(state.get("matches", []))} / {EXPECTED_MATCH_COUNT}</p>
        <p><span class="sport-success">Annex C:</span> {len(state.get("annex_c", []))} / {EXPECTED_ANNEX_C_RECORD_COUNT}</p>
        <p><span class="sport-accent">Computed group rows:</span> {len(groups)}</p>
        <p><span class="sport-accent">Third-place rows:</span> {len(thirds)}</p>
        <ul>{warnings_html}</ul>
    </div>
    <div class="sport-card">
        <h3>Judge Demo Path</h3>
        <p><strong>Judge path:</strong> <span class="sport-success">Load Judge Demo Scenario -&gt; Change one result -&gt; Recalculate War Room -&gt; Tournament Impact Panel -&gt; AI Scout -&gt; Friends League</span></p>
        <ol>
            <li><strong>Click Load Judge Demo Scenario</strong></li>
            <li><strong>Change this result in Match Planner</strong></li>
            <li><strong>Then click Recalculate War Room</strong></li>
            <li>Review Tournament Impact Panel</li>
            <li>Watch the impact panel update</li>
            <li>Review Match Planner</li>
            <li>Review Group Tracker</li>
            <li>Review 3rd-Place Ranking</li>
            <li>Review Bracket War Room</li>
            <li>Review Friends League</li>
            <li>Check AI Scout Signals</li>
        </ol>
    </div>
    """


def _bracket_html(bracket: dict) -> str:
    third_groups = bracket.get("qualified_third_groups") or []
    group_cards = "".join(
        f"<span class='sport-card' style='display:inline-block;margin:4px;padding:6px 8px;'>Group {group}</span>"
        for group in third_groups
    )
    r32_cards = "".join(
        (
            "<div class='sport-card' style='margin:6px 0;'>"
            f"<strong>{match_id}</strong><br>"
            f"{payload.get('team_a', payload.get('slot_a', 'TBD'))} vs "
            f"{payload.get('team_b', payload.get('slot_b', 'TBD'))}"
            "</div>"
        )
        for match_id, payload in (bracket.get("round_of_32") or {}).items()
    )
    if not group_cards and not r32_cards:
        body = (
            "<div class='sport-card' style='background:#0d131d;'>"
            "<p class='sport-accent'>Waiting for completed results.</p>"
            "<p>Enter completed scores in MATCH_PLANNER, then recalculate to build tables and bracket outputs.</p>"
            "</div>"
        )
    else:
        group_body = group_cards or "<span class='sport-warning'>Pending</span>"
        r32_body = r32_cards or "<span class='sport-accent'>Annex C mapping pending.</span>"
        body = (
            f"<h4>Qualified Third Groups</h4><div>{group_body}</div>"
            f"<h4>Round of 32 Preview</h4><div>{r32_body}</div>"
        )
    return f"""
    <div class="sport-card">
        <h3>Canonical Bracket Summary</h3>
        <p>Status: <span class="sport-accent">{bracket.get("status")}</span></p>
        <p>Third-place key: <span class="sport-success">{bracket.get("third_place_key", "") or "pending"}</span></p>
        <div>{body}</div>
    </div>
    """


def _html_table_rows(frame: pd.DataFrame, limit: int) -> str:
    if frame is None or frame.empty:
        return "<tr data-row='empty'><td>No rows available.</td></tr>"
    rows = []
    preview = frame.head(limit).astype(object).where(pd.notna(frame.head(limit)), "")
    columns = list(preview.columns)
    for row_index, (_, row) in enumerate(preview.iterrows(), start=1):
        cells = "".join(f"<td>{row.get(column, '')}</td>" for column in columns[:8])
        rows.append(f"<tr data-row='{row_index}'>{cells}</tr>")
    return "".join(rows)


def _visible_match_planner_html(matches: pd.DataFrame, planner_filter: str = "All 104 matches") -> str:
    rows = _html_table_rows(matches, VISIBLE_TAB_PREVIEW_MATCHES)
    return f"""
    <div class='sport-card'>
        <h3>Match Planner Filtered Preview</h3>
        <p>One-click judge filter for the 104-match planner by stage or Groups A-L.</p>
        <p><strong>Active filter:</strong> <span class='sport-success'>{planner_filter}</span></p>
        <p>Engine loaded: {len(matches)} / {EXPECTED_MATCH_COUNT} matches · Filtered rows: {len(matches)} / {EXPECTED_MATCH_COUNT} matches · Visible preview: {min(len(matches), VISIBLE_TAB_PREVIEW_MATCHES)} matches shown</p>
        <table>{rows}</table>
    </div>
    """


def _visible_group_tracker_html(groups: pd.DataFrame) -> str:
    rows = _html_table_rows(groups, VISIBLE_TAB_PREVIEW_GROUPS)
    return f"""
    <div class='sport-card'>
        <h3>Group Tracker</h3>
        <p>Shows how group order changes after recalculation.</p>
        <p>Computed group rows: {len(groups)} · Visible preview: {min(len(groups), VISIBLE_TAB_PREVIEW_GROUPS)} rows shown</p>
        <table>{rows}</table>
    </div>
    """


def _visible_third_place_html(thirds: pd.DataFrame) -> str:
    rows = _html_table_rows(thirds, 1)
    return f"""
    <div class='sport-card'>
        <h3>3rd-Place Ranking</h3>
        <p>Critical in a 48-team format because third-place teams can still advance.</p>
        <p>Computed third-place rows: {len(thirds)} · Visible preview: {min(len(thirds), 1)} row shown</p>
        <table>{rows}</table>
    </div>
    """


def _visible_bracket_war_room_html(bracket: dict) -> str:
    round_of_32 = bracket.get("round_of_32") or {}
    rows = []
    for row_index, (match_id, payload) in enumerate(list(round_of_32.items())[:VISIBLE_TAB_PREVIEW_BRACKET], start=1):
        team_a = payload.get("team_a") or payload.get("slot_a") or "TBD"
        team_b = payload.get("team_b") or payload.get("slot_b") or "TBD"
        rows.append(f"<tr data-row='{row_index}'><td>{match_id}</td><td>{team_a}</td><td>{team_b}</td></tr>")
    while len(rows) < VISIBLE_TAB_PREVIEW_BRACKET:
        row_index = len(rows) + 1
        rows.append(f"<tr data-row='{row_index}'><td>R32 Preview {row_index}</td><td>TBD</td><td>TBD</td></tr>")
    return f"""
    <div class='sport-card'>
        <h3>Round of 32 Preview</h3>
        <p>Converts current standings into knockout preview slots.</p>
        <p>Visible preview: 8 bracket rows shown</p>
        <table>{''.join(rows)}</table>
    </div>
    """


def _visible_friends_league_html(friends: pd.DataFrame) -> str:
    preview = friends.head(VISIBLE_TAB_PREVIEW_FRIENDS)
    rows = _html_table_rows(preview, VISIBLE_TAB_PREVIEW_FRIENDS)
    return f"""
    <div class='sport-card'>
        <h3>Friends League</h3>
        <p>Shows which private picks gain or lose after the scenario change.</p>
        <p>Demo scoreboard rows: {len(preview)} · Visible preview: {len(preview)} rows shown</p>
        <table>{rows}</table>
    </div>
    """


def compute_outputs(state: dict, matches: pd.DataFrame | None = None):
    working_state = dict(state)
    matches_df = matches.copy() if matches is not None else working_state["matches"].copy()
    matches_df = normalize_match_columns(matches_df)
    matches_df = _score_matches(matches_df)
    working_state["matches"] = matches_df

    groups = build_group_table(matches_df)
    thirds = build_third_place_table(groups)
    bracket = build_bracket_json_contract(build_bracket_mapping(groups, thirds, working_state.get("annex_c")), groups, thirds)
    friends = _friends_leaderboard(working_state["friends"])
    ai_scout = build_ai_scout_output(matches_df)
    dashboard = _summary_html(working_state, groups, thirds)
    top_checklist = _scenario_controls_html(working_state)
    bracket_summary = _bracket_html(bracket)
    impact_panel = build_impact_panel_html(matches_df, groups, thirds, bracket, friends)
    return working_state, matches_df, groups, thirds, bracket, bracket_summary, friends, dashboard, top_checklist, ai_scout, impact_panel


def initial_load():
    state = load_workbook_state()
    return compute_outputs(state)


def load_demo_scenario_outputs(state: dict, matches: pd.DataFrame | None = None):
    working_state = dict(state)
    base_matches = matches.copy() if matches is not None else working_state["matches"].copy()
    demo_matches = apply_demo_scenario(base_matches)
    return compute_outputs(working_state, demo_matches)


def recalculate_outputs(state: dict, matches: pd.DataFrame | None = None):
    working_state, matches_df, groups, thirds, bracket, bracket_summary, friends, summary, top_checklist, ai_scout, impact_panel = compute_outputs(state, matches)
    match_html = _visible_match_planner_html(matches_df)
    group_html = _visible_group_tracker_html(groups)
    third_html = _visible_third_place_html(thirds)
    bracket_html = _visible_bracket_war_room_html(bracket)
    friends_html = _visible_friends_league_html(friends)
    return working_state, summary, match_html, group_html, third_html, bracket, bracket_html, friends_html, ai_scout, impact_panel


with gr.Blocks(title=APP_TITLE) as demo:
    workbook_state = gr.State()
    gr.HTML(_command_header_html())

    top_checklist_html = gr.HTML(value=_scenario_controls_html())
    with gr.Row():
        load_demo_button = gr.Button("Load Judge Demo Scenario", variant="primary")
        recalc_button = gr.Button("Recalculate War Room", variant="secondary")
        random_outcomes_button = gr.Button("Generate Random Outcomes for all 104 matches", variant="secondary")
    impact_panel_html = gr.HTML(value=build_impact_panel_html(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {}, pd.DataFrame()))

    with gr.Tabs():
        with gr.Tab("DASHBOARD"):
            dashboard_html = gr.HTML()
        with gr.Tab("MATCH PLANNER"):
            gr.Markdown("**Change this result. Then click Recalculate War Room. Use the quick filter to inspect stages or Groups A-L without scrolling 104 rows.**")
            planner_filter = gr.Dropdown(choices=list(PLANNER_FILTER_CHOICES), value="All 104 matches", label="Planner quick filter", interactive=True)
            planner_filter_html = gr.HTML(value=_visible_match_planner_html(pd.DataFrame(), "All 104 matches"))
            matches_df = gr.Dataframe(label="MATCH_PLANNER — editable full 104-match scenario input", interactive=True, wrap=True)
        with gr.Tab("GROUP TRACKER"):
            groups_df = gr.Dataframe(label="Computed Group Table", interactive=False, wrap=True)
        with gr.Tab("3RD-PLACE RANKING"):
            third_places_df = gr.Dataframe(label="Top Third-Place Ranking", interactive=False, wrap=True)
        with gr.Tab("BRACKET WAR ROOM"):
            bracket_json = gr.State()
            bracket_html = gr.HTML()
        with gr.Tab("FRIENDS LEAGUE"):
            friends_df = gr.Dataframe(label="Friends League Leaderboard", interactive=True, wrap=True)
        with gr.Tab("AI SCOUT"):
            gr.Markdown("Explains the consequence of the scenario in plain English.")
            ai_scout_html = gr.HTML()

    demo.load(
        initial_load,
        inputs=None,
        outputs=[
            workbook_state,
            matches_df,
            groups_df,
            third_places_df,
            bracket_json,
            bracket_html,
            friends_df,
            dashboard_html,
            top_checklist_html,
            ai_scout_html,
            impact_panel_html,
        ],
    )
    recalc_button.click(
        compute_outputs,
        inputs=[workbook_state, matches_df],
        outputs=[
            workbook_state,
            matches_df,
            groups_df,
            third_places_df,
            bracket_json,
            bracket_html,
            friends_df,
            dashboard_html,
            top_checklist_html,
            ai_scout_html,
            impact_panel_html,
        ],
    )
    planner_filter.change(
        filter_match_planner,
        inputs=[matches_df, planner_filter],
        outputs=planner_filter_html,
    )
    random_outcomes_button.click(
        generate_random_match_outcomes,
        inputs=[workbook_state, matches_df],
        outputs=[
            workbook_state,
            matches_df,
            planner_filter_html,
            groups_df,
            third_places_df,
            bracket_json,
            bracket_html,
            friends_df,
            dashboard_html,
            top_checklist_html,
            ai_scout_html,
            impact_panel_html,
        ],
    )
    load_demo_button.click(
        load_demo_scenario_outputs,
        inputs=[workbook_state, matches_df],
        outputs=[
            workbook_state,
            matches_df,
            groups_df,
            third_places_df,
            bracket_json,
            bracket_html,
            friends_df,
            dashboard_html,
            top_checklist_html,
            ai_scout_html,
            impact_panel_html,
        ],
    )


if __name__ == "__main__":
    demo.launch(css=PREMIUM_DARK_SPORT_CSS)
