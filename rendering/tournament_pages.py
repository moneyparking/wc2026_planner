from __future__ import annotations

from dataclasses import dataclass
from reportlab.pdfgen.canvas import Canvas

from layout.geometry import rect_from_xywh
from models.specs import PageSpec, Rect, RenderManifest
from registries.fixture_registry import FixtureRef, TeamRef, get_group_fixtures, get_group_teams, get_index_fixtures
from rendering.global_components import GlobalComponents
from rendering.text_utils import draw_centered_label, draw_label, draw_right_label


@dataclass(frozen=True, slots=True)
class BracketSlot:
    label: str
    seed: str
    note: str


@dataclass(frozen=True, slots=True)
class KnockoutStage:
    label: str
    matches: str
    note: str


GROUP_TABLE_COLUMNS = ("Team", "P", "W", "D", "L", "GD", "PTS")

BRACKET_SLOTS = (
    BracketSlot("R32 Pick 1", "1A / 3rd", "Upset watch"),
    BracketSlot("R32 Pick 2", "2B / 2C", "Form pick"),
    BracketSlot("R16 Pick", "Winner path", "Momentum"),
    BracketSlot("QF Pick", "Elite test", "Depth"),
    BracketSlot("SF Pick", "Title case", "Pressure"),
    BracketSlot("Champion", "Final", "Legacy"),
)

KNOCKOUT_STAGES = (
    KnockoutStage("Round of 32", "16 matches", "First full elimination wave."),
    KnockoutStage("Round of 16", "8 matches", "Favorites start colliding."),
    KnockoutStage("Quarterfinals", "4 matches", "Tournament identity games."),
    KnockoutStage("Semifinals", "2 matches", "Pressure, tactics, legacies."),
    KnockoutStage("Third Place", "1 match", "Rotation and pride tracker."),
    KnockoutStage("Final", "1 match", "Champion, MVP, memory page."),
)


class TournamentPageRenderer:
    def __init__(self, globals_: GlobalComponents) -> None:
        self.globals = globals_

    def can_render(self, page: PageSpec) -> bool:
        return page.template_id in {"group_tracker", "match_index", "bracket_prediction", "knockout_tracker"}

    def render(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        active_nav = "groups"
        if page.template_id == "match_index":
            active_nav = "match"
        if page.template_id in {"bracket_prediction", "knockout_tracker"}:
            active_nav = "bracket"

        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id=active_nav)

        if page.template_id == "group_tracker":
            self.render_group_tracker(canvas, page)
        elif page.template_id == "match_index":
            self.render_match_index(canvas, page)
        elif page.template_id == "bracket_prediction":
            self.render_bracket_prediction(canvas, page)
        elif page.template_id == "knockout_tracker":
            self.render_live_knockout_tracker(canvas, page)
        else:
            raise ValueError(f"TournamentPageRenderer cannot render template {page.template_id}")

    def _draw_title_block(self, canvas: Canvas, page: PageSpec, kicker: str) -> None:
        canvas.setFillColor("#A7FF00")
        draw_label(canvas, kicker.upper(), 48, 518, self.globals.fonts["body_bold"], 8)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, page.title, 48, 490, self.globals.fonts["display"], 30)
        canvas.setFillColor("#AAB3C2")
        draw_label(canvas, page.subtitle, 50, 468, self.globals.fonts["body"], 9.5)

    def _draw_wrapped(
        self,
        canvas: Canvas,
        text: str,
        x: float,
        y: float,
        width: float,
        max_lines: int = 2,
        font_size: float = 7.2,
    ) -> None:
        words = text.split()
        lines: list[str] = []
        current = ""

        for word in words:
            candidate = word if not current else f"{current} {word}"
            if canvas.stringWidth(candidate, self.globals.fonts["body"], font_size) <= width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        for index, line in enumerate(lines[:max_lines]):
            draw_label(canvas, line, x, y - index * 10, self.globals.fonts["body"], font_size)

    def render_group_tracker(self, canvas: Canvas, page: PageSpec) -> None:
        group = page.page_id.split("_")[1].upper() if page.page_id.startswith("group_") else "A"
        teams = get_group_teams(group)
        fixtures = get_group_fixtures(group)

        self._draw_title_block(canvas, page, f"Group {group}")

        table = rect_from_xywh(48, 248, 414, 196)
        fixtures_panel = rect_from_xywh(486, 132, 250, 312)
        notes = rect_from_xywh(48, 132, 414, 82)

        self.globals.draw_card_panel(canvas, table)
        self.globals.draw_card_panel(canvas, fixtures_panel)
        self.globals.draw_write_plate(canvas, notes)

        self._draw_group_table(canvas, table, teams)
        self._draw_group_fixture_links(canvas, fixtures_panel, fixtures)

        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "GROUP CHAOS NOTES", notes.x + 16, notes.y + 52, self.globals.fonts["body_bold"], 8)
        canvas.setFillColor("#AAB3C2")
        self._draw_wrapped(
            canvas,
            f"Group {group}: update standings after each full-time result, then mark tiebreaker pressure before Round 3.",
            notes.x + 16,
            notes.y + 32,
            notes.width - 32,
            2,
            7.5,
        )

    def _draw_group_table(self, canvas: Canvas, rect: Rect, teams: tuple[TeamRef, TeamRef, TeamRef, TeamRef]) -> None:
        x_positions = (
            rect.x + 18,
            rect.x + 198,
            rect.x + 236,
            rect.x + 274,
            rect.x + 312,
            rect.x + 350,
            rect.x + 384,
        )

        canvas.setFillColor("#AAB3C2")
        for index, header in enumerate(GROUP_TABLE_COLUMNS):
            draw_label(canvas, header.upper(), x_positions[index], rect.y + rect.height - 30, self.globals.fonts["body_bold"], 6.7)

        for row_index, team in enumerate(teams):
            y = rect.y + rect.height - 66 - row_index * 36
            self.globals.draw_write_plate(canvas, rect_from_xywh(rect.x + 12, y - 9, rect.width - 24, 28), radius=8)

            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, f"{team.code}  {team.name}", x_positions[0], y, self.globals.fonts["body_bold"], 8)
            canvas.setFillColor("#AAB3C2")
            for stat_index in range(1, len(GROUP_TABLE_COLUMNS)):
                draw_centered_label(canvas, "0", x_positions[stat_index] + 8, y, self.globals.fonts["mono"], 7)

    def _draw_group_fixture_links(self, canvas: Canvas, rect: Rect, fixtures: tuple[FixtureRef, ...]) -> None:
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "GROUP FIXTURES", rect.x + 16, rect.y + rect.height - 30, self.globals.fonts["body_bold"], 9)

        for index, fixture in enumerate(fixtures[:6]):
            y = rect.y + rect.height - 70 - index * 38
            row = rect_from_xywh(rect.x + 22, y - 10, rect.width - 44, 30)
            self.globals.draw_write_plate(canvas, row, radius=8)

            canvas.setFillColor("#A7FF00")
            draw_label(canvas, f"{fixture.match_id:03d}", row.x + 10, y, self.globals.fonts["mono"], 7)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, f"{fixture.team_a.code} vs {fixture.team_b.code}", row.x + 52, y, self.globals.fonts["body_bold"], 8)
            canvas.setFillColor("#AAB3C2")
            draw_right_label(canvas, fixture.round_label, row.x + row.width - 10, y, self.globals.fonts["body"], 6.8)

    def render_match_index(self, canvas: Canvas, page: PageSpec) -> None:
        fixtures = get_index_fixtures(page.page_number) if page.page_number in {22, 23, 24} else tuple()
        self._draw_title_block(canvas, page, "Match index")

        panel = rect_from_xywh(48, 84, 688, 360)
        self.globals.draw_card_panel(canvas, panel)

        canvas.setFillColor("#AAB3C2")
        for x, header in (
            (panel.x + 16, "MATCH"),
            (panel.x + 84, "FIXTURE"),
            (panel.x + 306, "STAGE"),
            (panel.x + 560, "LOG"),
        ):
            draw_label(canvas, header, x, panel.y + panel.height - 28, self.globals.fonts["body_bold"], 6.5)

        if not fixtures:
            canvas.setFillColor("#AAB3C2")
            draw_label(canvas, "Derived SKU compact index. Use navigation tabs for match sections.", panel.x + 20, panel.y + 260, self.globals.fonts["body"], 9)
            return

        row_h = 9.0 if len(fixtures) > 32 else 10.0
        start_y = panel.y + panel.height - 50

        for index, fixture in enumerate(fixtures):
            y = start_y - index * row_h
            canvas.setFillColor("#1A2230" if index % 2 == 0 else "#101722")
            canvas.roundRect(panel.x + 10, y - 3, panel.width - 20, 8, 2, fill=1, stroke=0)

            canvas.setFillColor("#A7FF00")
            draw_label(canvas, f"{fixture.match_id:03d}", panel.x + 16, y, self.globals.fonts["mono"], 5.2)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, f"{fixture.team_a.code} vs {fixture.team_b.code}", panel.x + 84, y, self.globals.fonts["body_bold"], 5.4)
            canvas.setFillColor("#AAB3C2")
            draw_label(canvas, fixture.round_label, panel.x + 306, y, self.globals.fonts["body"], 5.1)
            draw_right_label(canvas, f"PAGE {fixture.page_number}", panel.x + panel.width - 18, y, self.globals.fonts["mono"], 5.1)

    def render_bracket_prediction(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title_block(canvas, page, "Bracket")

        panel = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, panel)

        for index, slot in enumerate(BRACKET_SLOTS):
            x = panel.x + 26 + (index % 3) * 214
            y = panel.y + panel.height - 122 - (index // 3) * 132
            card = rect_from_xywh(x, y, 180, 96)
            self.globals.draw_write_plate(canvas, card, radius=10)

            canvas.setFillColor("#A7FF00")
            draw_label(canvas, slot.label.upper(), x + 14, y + 64, self.globals.fonts["body_bold"], 7)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, slot.seed, x + 14, y + 42, self.globals.fonts["body_bold"], 12)
            canvas.setFillColor("#AAB3C2")
            draw_label(canvas, slot.note, x + 14, y + 22, self.globals.fonts["body"], 7)

    def render_live_knockout_tracker(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title_block(canvas, page, "Knockout")

        panel = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, panel)

        for index, stage in enumerate(KNOCKOUT_STAGES):
            x = panel.x + 20 + (index % 2) * 334
            y = panel.y + panel.height - 72 - (index // 2) * 84
            row = rect_from_xywh(x, y - 16, 300, 58)
            self.globals.draw_write_plate(canvas, row, radius=10)

            canvas.setFillColor("#A7FF00")
            draw_label(canvas, stage.matches.upper(), row.x + 12, y + 18, self.globals.fonts["body_bold"], 6.5)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, stage.label, row.x + 12, y, self.globals.fonts["body_bold"], 10)
            canvas.setFillColor("#AAB3C2")
            self._draw_wrapped(canvas, stage.note, row.x + 144, y + 12, 136, 2, 6.8)
