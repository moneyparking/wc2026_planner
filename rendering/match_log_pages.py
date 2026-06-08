from __future__ import annotations

from dataclasses import dataclass
from reportlab.pdfgen.canvas import Canvas

from layout.geometry import rect_from_xywh
from models.specs import PageSpec, RenderManifest
from registries.fixture_registry import FixtureRef, get_fixture
from rendering.global_components import GlobalComponents
from rendering.text_utils import draw_centered_label, draw_label, draw_right_label


@dataclass(frozen=True, slots=True)
class MatchField:
    label: str
    hint: str


@dataclass(frozen=True, slots=True)
class TimelineEvent:
    minute: str
    label: str
    icon: str


PREDICTION_FIELDS = (
    MatchField("Winner pick", "Team / draw"),
    MatchField("Exact score", "0–0"),
    MatchField("Confidence", "1–5"),
    MatchField("First scorer", "Player"),
)

RECAP_FIELDS = (
    MatchField("MVP", "Player"),
    MatchField("Turning point", "Minute + moment"),
    MatchField("Best goal", "Player / minute"),
    MatchField("Group chat quote", "Best reaction"),
)

TIMELINE_EVENTS = (
    TimelineEvent("00", "Kickoff", "icons_whistle_001.png"),
    TimelineEvent("15", "Pressure", "icons_tactics_001.png"),
    TimelineEvent("30", "Chance", "icons_goal_001.png"),
    TimelineEvent("45", "Halftime", "icons_clock_001.png"),
    TimelineEvent("60", "Card", "icons_card_001.png"),
    TimelineEvent("75", "VAR", "icons_var_001.png"),
    TimelineEvent("90+", "Drama", "icons_star_001.png"),
)


class MatchLogPageRenderer:
    def __init__(self, globals_: GlobalComponents) -> None:
        self.globals = globals_

    def can_render(self, page: PageSpec) -> bool:
        return page.template_id == "dedicated_match_log"

    def render(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id="match")
        match_id = self._match_id_from_page(page)
        fixture = get_fixture(match_id)
        self._draw_header(canvas, fixture, page)
        self._draw_score_prediction_zone(canvas, fixture)
        self._draw_pitch_zone(canvas)
        self._draw_timeline(canvas)
        self._draw_recap_zone(canvas)
        self._draw_back_link_hint(canvas, match_id, page)

    def _match_id_from_page(self, page: PageSpec) -> int:
        if page.page_id.startswith("match_log_"):
            return int(page.page_id.split("_")[-1])
        if page.page_id.startswith("condensed_match_log_"):
            return int(page.page_id.split("_")[-2])
        if page.data_ref and page.data_ref.startswith("fixtures.match_"):
            return int(page.data_ref.replace("fixtures.match_", "").split("_")[0])
        return max(1, min(104, page.page_number - 70))

    def _draw_header(self, canvas: Canvas, fixture: FixtureRef, page: PageSpec) -> None:
        canvas.setFillColor("#A7FF00")
        draw_label(canvas, f"MATCH {fixture.match_id:03d}", 48, 518, self.globals.fonts["body_bold"], 8)

        canvas.setFillColor("#F4F7FB")
        title = f"{fixture.team_a.code} vs {fixture.team_b.code}" if not page.page_id.startswith("condensed") else page.title
        draw_label(canvas, title, 48, 490, self.globals.fonts["display"], 32)

        canvas.setFillColor("#AAB3C2")
        draw_label(canvas, f"{fixture.round_label} • Group {fixture.group}", 50, 468, self.globals.fonts["body"], 9.5)

        self.globals.draw_write_plate(canvas, rect_from_xywh(588, 524, 148, 30), radius=8)
        canvas.setFillColor("#A7FF00")
        draw_centered_label(canvas, "BACK TO INDEX", 662, 535, self.globals.fonts["body_bold"], 7)

    def _draw_score_prediction_zone(self, canvas: Canvas, fixture: FixtureRef) -> None:
        score_panel = rect_from_xywh(48, 338, 282, 106)
        prediction_panel = rect_from_xywh(48, 200, 282, 112)

        self.globals.draw_card_panel(canvas, score_panel)
        self.globals.draw_card_panel(canvas, prediction_panel)

        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "LIVE SCORE", score_panel.x + 18, score_panel.y + score_panel.height - 28, self.globals.fonts["body_bold"], 9)

        for box, label in (
            (rect_from_xywh(score_panel.x + 18, score_panel.y + 24, 96, 48), fixture.team_a.code),
            (rect_from_xywh(score_panel.x + 168, score_panel.y + 24, 96, 48), fixture.team_b.code),
        ):
            self.globals.draw_write_plate(canvas, box, radius=10)
            canvas.setFillColor("#A7FF00")
            draw_centered_label(canvas, label, box.x + box.width / 2, box.y + 29, self.globals.fonts["body_bold"], 11)
            canvas.setFillColor("#F4F7FB")
            draw_centered_label(canvas, "0", box.x + box.width / 2, box.y + 10, self.globals.fonts["body_bold"], 14)

        canvas.setFillColor("#AAB3C2")
        draw_centered_label(canvas, "VS", score_panel.x + 141, score_panel.y + 42, self.globals.fonts["body_bold"], 8)

        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "PREDICTION SLIP", prediction_panel.x + 18, prediction_panel.y + prediction_panel.height - 28, self.globals.fonts["body_bold"], 9)

        for index, field in enumerate(PREDICTION_FIELDS):
            x = prediction_panel.x + 18 + (index % 2) * 132
            y = prediction_panel.y + 56 - (index // 2) * 42
            plate = rect_from_xywh(x, y, 116, 28)
            self.globals.draw_write_plate(canvas, plate, radius=8)

            canvas.setFillColor("#FFD166")
            draw_label(canvas, field.label.upper(), plate.x + 8, plate.y + 15, self.globals.fonts["body_bold"], 5.8)
            canvas.setFillColor("#AAB3C2")
            draw_label(canvas, field.hint, plate.x + 8, plate.y + 5, self.globals.fonts["body"], 6.2)

    def _draw_pitch_zone(self, canvas: Canvas) -> None:
        pitch = rect_from_xywh(354, 250, 382, 194)
        self.globals.draw_card_panel(canvas, pitch)

        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "TACTICS / MOMENTUM MAP", pitch.x + 18, pitch.y + pitch.height - 28, self.globals.fonts["body_bold"], 9)

        field = rect_from_xywh(pitch.x + 32, pitch.y + 30, pitch.width - 64, pitch.height - 72)
        canvas.setStrokeColor("#394457")
        canvas.setLineWidth(1.0)
        canvas.roundRect(field.x, field.y, field.width, field.height, 12, fill=0, stroke=1)
        canvas.line(field.x + field.width / 2, field.y, field.x + field.width / 2, field.y + field.height)
        canvas.circle(field.x + field.width / 2, field.y + field.height / 2, 22, stroke=1, fill=0)

    def _draw_timeline(self, canvas: Canvas) -> None:
        panel = rect_from_xywh(48, 104, 688, 72)
        self.globals.draw_card_panel(canvas, panel)

        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "0–90+ TIMELINE", panel.x + 18, panel.y + panel.height - 24, self.globals.fonts["body_bold"], 9)

        axis_y = panel.y + 28
        canvas.setStrokeColor("#394457")
        canvas.line(panel.x + 36, axis_y, panel.x + panel.width - 36, axis_y)

        step = (panel.width - 92) / (len(TIMELINE_EVENTS) - 1)
        for index, event in enumerate(TIMELINE_EVENTS):
            x = panel.x + 46 + index * step
            self.globals.icons.draw_icon(canvas, event.icon, x - 8, axis_y + 8, size=16, allow_missing=True)
            canvas.setFillColor("#A7FF00")
            draw_centered_label(canvas, event.minute, x, axis_y - 12, self.globals.fonts["mono"], 6.5)
            canvas.setFillColor("#AAB3C2")
            draw_centered_label(canvas, event.label, x, axis_y - 24, self.globals.fonts["body"], 5.6)

    def _draw_recap_zone(self, canvas: Canvas) -> None:
        recap_panel = rect_from_xywh(354, 188, 382, 46)
        self.globals.draw_write_plate(canvas, recap_panel, radius=10)

        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "FULL-TIME RECAP", recap_panel.x + 14, recap_panel.y + 26, self.globals.fonts["body_bold"], 7.5)
        canvas.setFillColor("#AAB3C2")
        draw_label(canvas, "MVP, turning point, best goal, group-chat quote.", recap_panel.x + 14, recap_panel.y + 10, self.globals.fonts["body"], 7)

        mini_panel = rect_from_xywh(354, 104, 382, 64)
        self.globals.draw_card_panel(canvas, mini_panel)

        for index, field in enumerate(RECAP_FIELDS):
            x = mini_panel.x + 14 + index * 90
            y = mini_panel.y + 28
            canvas.setFillColor("#FFD166")
            draw_label(canvas, field.label.upper(), x, y + 14, self.globals.fonts["body_bold"], 5.2)
            canvas.setFillColor("#AAB3C2")
            draw_label(canvas, field.hint, x, y, self.globals.fonts["body"], 5.6)

    def _draw_back_link_hint(self, canvas: Canvas, match_id: int, page: PageSpec) -> None:
        target = "001–036" if match_id <= 36 else "037–072" if match_id <= 72 else "073–104"
        if page.page_id.startswith("condensed"):
            target = "condensed tracker"
        canvas.setFillColor("#AAB3C2")
        draw_right_label(canvas, f"Index block: {target}", 736, 86, self.globals.fonts["mono"], 6.5)
