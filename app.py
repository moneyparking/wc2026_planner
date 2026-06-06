from __future__ import annotations

import pandas as pd
import gradio as gr

from layout.css_styles import PREMIUM_DARK_SPORT_CSS
from models.bracket_mapper import build_bracket_mapping
from models.data_loader import load_workbook_state, normalize_match_columns
from models.fifa_rules import build_group_table, build_third_place_table
from models.scoring import score_prediction
from product_config import APP_TITLE, EXPECTED_ANNEX_C_RECORD_COUNT, EXPECTED_MATCH_COUNT


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


def _summary_html(state: dict, groups: pd.DataFrame, thirds: pd.DataFrame) -> str:
    warnings = state.get("warnings") or []
    warnings_html = "".join(f"<li>{warning}</li>" for warning in warnings) or "<li>Workbook loaded cleanly.</li>"
    return f"""
    <div class="sport-card">
        <h3>Build Small Status</h3>
        <p><span class="sport-accent">Workbook:</span> {state.get("spreadsheet_path", "not loaded")}</p>
        <p><span class="sport-success">Matches:</span> {len(state.get("matches", []))} / {EXPECTED_MATCH_COUNT}</p>
        <p><span class="sport-success">Annex C:</span> {len(state.get("annex_c", []))} / {EXPECTED_ANNEX_C_RECORD_COUNT}</p>
        <p><span class="sport-accent">Computed group rows:</span> {len(groups)}</p>
        <p><span class="sport-accent">Third-place rows:</span> {len(thirds)}</p>
        <ul>{warnings_html}</ul>
    </div>
    """


def _bracket_html(bracket: dict) -> str:
    third_groups = bracket.get("qualified_third_groups") or []
    chips = "".join(f"<span class='sport-card' style='display:inline-block;margin:4px;padding:6px 8px;'>{group}</span>" for group in third_groups)
    if not chips:
        chips = "<span class='sport-warning'>No completed third-place ranking yet. Enter results and recalc.</span>"
    return f"""
    <div class="sport-card">
        <h3>Canonical Bracket Summary</h3>
        <p>Status: <span class="sport-accent">{bracket.get("status")}</span></p>
        <p>Third-place key: <span class="sport-success">{bracket.get("third_place_key", "") or "pending"}</span></p>
        <div>{chips}</div>
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
    bracket = build_bracket_mapping(groups, thirds, working_state.get("annex_c"))
    friends = _friends_leaderboard(working_state["friends"])
    summary = _summary_html(working_state, groups, thirds)
    bracket_summary = _bracket_html(bracket)
    return working_state, matches_df, groups, thirds, bracket, friends, summary, bracket_summary


def initial_load():
    state = load_workbook_state()
    return compute_outputs(state)


with gr.Blocks(title=APP_TITLE) as demo:
    workbook_state = gr.State()
    gr.HTML(
        f"""
        <div class="sport-hero">
            <h1>{APP_TITLE}</h1>
            <p>Static offline spreadsheet engine, editable match planner, group tracker, and bracket war room.</p>
        </div>
        """
    )

    recalc_button = gr.Button("Recalculate War Room", variant="primary")

    with gr.Tabs():
        with gr.Tab("DASHBOARD"):
            dashboard_html = gr.HTML()
        with gr.Tab("MATCH PLANNER"):
            matches_df = gr.Dataframe(label="MATCH_PLANNER", interactive=True, wrap=True)
        with gr.Tab("GROUP TRACKER"):
            groups_df = gr.Dataframe(label="Computed Group Table", interactive=False, wrap=True)
        with gr.Tab("3RD-PLACE RANKING"):
            third_places_df = gr.Dataframe(label="Top Third-Place Ranking", interactive=False, wrap=True)
        with gr.Tab("BRACKET WAR ROOM"):
            bracket_json = gr.JSON(label="Canonical Bracket Output")
            bracket_html = gr.HTML()
        with gr.Tab("FRIENDS LEAGUE"):
            friends_df = gr.Dataframe(label="Friends League Leaderboard", interactive=True, wrap=True)

    demo.load(
        initial_load,
        inputs=None,
        outputs=[
            workbook_state,
            matches_df,
            groups_df,
            third_places_df,
            bracket_json,
            friends_df,
            dashboard_html,
            bracket_html,
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
            friends_df,
            dashboard_html,
            bracket_html,
        ],
    )


if __name__ == "__main__":
    demo.launch(css=PREMIUM_DARK_SPORT_CSS)
