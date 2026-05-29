from __future__ import annotations

from dataclasses import dataclass
from reportlab.pdfgen.canvas import Canvas

from layout.geometry import rect_from_xywh
from models.specs import PageSpec, Rect, RenderManifest
from rendering.global_components import GlobalComponents
from rendering.text_utils import draw_label


@dataclass(frozen=True, slots=True)
class TrackerRow:
    label: str
    slot_a: str
    slot_b: str
    slot_c: str


@dataclass(frozen=True, slots=True)
class StatTile:
    title: str
    value: str
    note: str


TEAM_ROWS = (
    TrackerRow("Favorite team", "USA", "Primary", "Full route"),
    TrackerRow("Rival watch", "TBD", "Danger", "Avoid path"),
    TrackerRow("Dark horse", "MAR", "Upset", "Momentum"),
    TrackerRow("Final pick", "BRA", "Champion", "Legacy"),
    TrackerRow("Bias check", "Emotion", "Risk", "Fix"),
)

RATING_ROWS = (
    TrackerRow("Attack", "Finishing", "Chance creation", "Set pieces"),
    TrackerRow("Midfield", "Control", "Press resistance", "Transitions"),
    TrackerRow("Defense", "Back line", "Keeper", "Clean sheets"),
    TrackerRow("Depth", "Bench", "Rotation", "Injuries"),
    TrackerRow("Pressure", "Experience", "Crowd", "Knockout nerve"),
)

SQUAD_ROWS = (
    TrackerRow("Star player", "Name", "Role", "Form"),
    TrackerRow("Breakout pick", "Name", "Role", "Why"),
    TrackerRow("Set-piece threat", "Name", "Foot/head", "Target zone"),
    TrackerRow("Impact sub", "Name", "Minute", "Game state"),
    TrackerRow("Penalty taker", "Name", "Confidence", "Notes"),
)

WATCHLIST_ROWS = (
    TrackerRow("Golden Boot watch", "Player", "Team", "Goals"),
    TrackerRow("Golden Glove watch", "Keeper", "Team", "Clean sheets"),
    TrackerRow("Young star", "Player", "Team", "Moment"),
    TrackerRow("Veteran leader", "Player", "Team", "Impact"),
    TrackerRow("Chaos player", "Player", "Team", "Cards / VAR"),
)

PATH_ROWS = (
    TrackerRow("Group finish", "1st", "2nd", "3rd path"),
    TrackerRow("R32 opponent", "Seed", "Style", "Risk"),
    TrackerRow("R16 opponent", "Seed", "Style", "Risk"),
    TrackerRow("Quarterfinal", "Opponent", "Key matchup", "Pick"),
    TrackerRow("Semifinal", "Opponent", "Pressure", "Pick"),
)

STATS_TILES = (
    StatTile("Goals", "0", "Tournament total"),
    StatTile("Clean sheets", "0", "Keeper + defense"),
    StatTile("Upsets", "0", "Underdog results"),
    StatTile("Cards", "0", "Discipline notes"),
    StatTile("VAR moments", "0", "Controversy tracker"),
    StatTile("Correct picks", "0", "Prediction accuracy"),
)


class TeamStatsPageRenderer:
    def __init__(self, globals_: GlobalComponents) -> None:
        self.globals = globals_

    def can_render(self, page: PageSpec) -> bool:
        return page.template_id in {
            "team_hub",
            "rating_sheet",
            "sports_cards",
            "watchlist",
            "path_tracker",
            "rival_watch",
            "dark_horse_board",
            "stats_dashboard",
            "leaderboard_tracker",
            "prediction_log",
            "accuracy_tracker",
            "upset_tracker",
            "moment_log",
            "best_goals",
            "mvp_race",
            "prediction_review",
        }

    def render(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        active_nav = "teams" if page.section_id.value == "team_fan_identity" else "stats"
        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id=active_nav)
        self._draw_title_block(canvas, page, "Teams" if active_nav == "teams" else "Stats")

        if page.template_id == "stats_dashboard":
            self.render_stats_dashboard(canvas)
            return

        rows = self._rows_for_template(page.template_id)
        headers = self._headers_for_template(page.template_id)
        self._draw_tracker_table(canvas, rect_from_xywh(48, 112, 688, 326), page.title, headers, rows)

    def _rows_for_template(self, template_id: str) -> tuple[TrackerRow, ...]:
        if template_id == "team_hub":
            return TEAM_ROWS
        if template_id == "rating_sheet":
            return RATING_ROWS
        if template_id == "sports_cards":
            return SQUAD_ROWS
        if template_id == "watchlist":
            return WATCHLIST_ROWS
        if template_id == "path_tracker":
            return PATH_ROWS
        if template_id in {"rival_watch", "dark_horse_board"}:
            return (
                TrackerRow("Pick 1", "Team", "Group", "Why"),
                TrackerRow("Pick 2", "Team", "Group", "Why"),
                TrackerRow("Upset spot", "Match", "Opponent", "Trigger"),
                TrackerRow("Ceiling", "R16", "QF", "SF"),
                TrackerRow("Risk", "Depth", "Cards", "Keeper"),
            )
        if template_id == "leaderboard_tracker":
            return tuple(TrackerRow(str(i), "Player", "Team", "Total") for i in range(1, 7))
        if template_id == "prediction_log":
            return (
                TrackerRow("Opening match", "Winner", "Score", "Confidence"),
                TrackerRow("Group winner", "Team", "Group", "Confidence"),
                TrackerRow("Top scorer", "Player", "Team", "Goals"),
                TrackerRow("Champion", "Team", "Path", "Reason"),
                TrackerRow("Biggest upset", "Match", "Pick", "Reason"),
            )
        if template_id == "accuracy_tracker":
            return (
                TrackerRow("Match picks", "Correct", "Missed", "%"),
                TrackerRow("Exact scores", "Correct", "Missed", "%"),
                TrackerRow("Group winners", "Correct", "Missed", "%"),
                TrackerRow("Knockout picks", "Correct", "Missed", "%"),
                TrackerRow("Champion pick", "Alive", "Out", "Result"),
            )
        if template_id in {"upset_tracker", "moment_log", "best_goals", "mvp_race", "prediction_review"}:
            return (
                TrackerRow("1", "Player / match", "Team / call", "Why"),
                TrackerRow("2", "Player / match", "Team / call", "Why"),
                TrackerRow("3", "Player / match", "Team / call", "Why"),
                TrackerRow("Wildcard", "Moment", "Impact", "Note"),
                TrackerRow("Final answer", "Pick", "Result", "Lesson"),
            )
        return TEAM_ROWS

    def _headers_for_template(self, template_id: str) -> tuple[str, str, str, str]:
        if template_id in {"leaderboard_tracker", "mvp_race"}:
            return ("Rank", "Player", "Team", "Total")
        if template_id == "prediction_log":
            return ("Pick", "Selection", "Detail", "Confidence")
        if template_id == "accuracy_tracker":
            return ("Category", "Correct", "Missed", "Rate")
        return ("Category", "Primary", "Secondary", "Notes")

    def _draw_title_block(self, canvas: Canvas, page: PageSpec, kicker: str) -> None:
        canvas.setFillColor("#A7FF00")
        draw_label(canvas, kicker.upper(), 48, 518, self.globals.fonts["body_bold"], 8)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, page.title, 48, 490, self.globals.fonts["display"], 30)
        canvas.setFillColor("#AAB3C2")
        draw_label(canvas, page.subtitle, 50, 468, self.globals.fonts["body"], 9.5)

    def _draw_tracker_table(
        self,
        canvas: Canvas,
        rect: Rect,
        title: str,
        headers: tuple[str, str, str, str],
        rows: tuple[TrackerRow, ...],
    ) -> None:
        self.globals.draw_card_panel(canvas, rect)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, title.upper(), rect.x + 18, rect.y + rect.height - 30, self.globals.fonts["body_bold"], 9)

        xs = (rect.x + 18, rect.x + 180, rect.x + 338, rect.x + 496)

        canvas.setFillColor("#AAB3C2")
        for index, header in enumerate(headers):
            draw_label(canvas, header.upper(), xs[index], rect.y + rect.height - 56, self.globals.fonts["body_bold"], 6.5)

        for row_index, row in enumerate(rows):
            y = rect.y + rect.height - 88 - row_index * 38
            plate = rect_from_xywh(rect.x + 14, y - 9, rect.width - 28, 28)
            self.globals.draw_write_plate(canvas, plate, radius=8)

            values = (row.label, row.slot_a, row.slot_b, row.slot_c)
            for col_index, value in enumerate(values):
                canvas.setFillColor("#F4F7FB" if col_index == 0 else "#AAB3C2")
                font = self.globals.fonts["body_bold"] if col_index == 0 else self.globals.fonts["body"]
                draw_label(canvas, value, xs[col_index], y, font, 7.2)

    def render_stats_dashboard(self, canvas: Canvas) -> None:
        for index, tile in enumerate(STATS_TILES):
            x = 48 + (index % 3) * 238
            y = 302 - (index // 3) * 126
            card = rect_from_xywh(x, y, 214, 104)
            self.globals.draw_card_panel(canvas, card)

            canvas.setFillColor("#A7FF00")
            draw_label(canvas, tile.value, x + 18, y + 58, self.globals.fonts["body_bold"], 20)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, tile.title, x + 18, y + 38, self.globals.fonts["body_bold"], 10)
            canvas.setFillColor("#AAB3C2")
            draw_label(canvas, tile.note, x + 18, y + 20, self.globals.fonts["body"], 7.2)
