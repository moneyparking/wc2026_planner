from __future__ import annotations

from dataclasses import dataclass
from reportlab.pdfgen.canvas import Canvas

from layout.geometry import rect_from_xywh
from models.specs import PageSpec, Rect, RenderManifest
from rendering.global_components import GlobalComponents
from rendering.text_utils import draw_centered_label, draw_label


@dataclass(frozen=True, slots=True)
class PartyTask:
    title: str
    owner: str
    timing: str
    note: str


@dataclass(frozen=True, slots=True)
class PoolRow:
    rank: str
    player: str
    picks: str
    score: str


WATCH_PARTY_TASKS = (
    PartyTask("Screen setup", "Host", "T-60", "TV, tablet, charger, backup stream."),
    PartyTask("Snack table", "Co-host", "T-45", "Sweet, salty, drinks, napkins."),
    PartyTask("Bingo cards", "Host", "T-30", "Share cards 1–8 or printed sheets."),
    PartyTask("Prediction lock", "Everyone", "T-10", "Winner, exact score, first scorer."),
    PartyTask("Halftime reset", "Host", "HT", "Update pool score and refill snacks."),
)

CHECKLIST_TASKS = (
    PartyTask("Open match log", "Host", "Before KO", "Score boxes and timeline ready."),
    PartyTask("Start group chat", "Everyone", "Before KO", "Drop first prediction prompt."),
    PartyTask("Track bingo", "Players", "Live", "Use dot stickers or printed tokens."),
    PartyTask("Update office pool", "Scorekeeper", "FT", "Correct pick, score, bonus."),
    PartyTask("Save best moment", "Host", "FT+5", "Move one moment to memory log."),
)

POOL_ROWS = (
    PoolRow("1", "Alex", "BRA / USA / MEX", "0"),
    PoolRow("2", "Jamie", "ARG / CAN / ENG", "0"),
    PoolRow("3", "Taylor", "FRA / MAR / JPN", "0"),
    PoolRow("4", "Morgan", "ESP / GER / KOR", "0"),
    PoolRow("5", "Casey", "POR / URU / SEN", "0"),
    PoolRow("6", "Riley", "NED / COL / AUS", "0"),
)

GROUP_CHAT_PROMPTS = (
    "Lock your winner pick before kickoff.",
    "First scorer prediction: safe pick or chaos pick?",
    "Which player changes the match before halftime?",
    "VAR check: correct call or robbery?",
    "Post-match: one word to describe the game.",
)

BINGO_TERMS = (
    "Early goal",
    "VAR check",
    "Yellow card",
    "Post hit",
    "Big save",
    "Coach rage",
    "Offside goal",
    "Penalty shout",
    "Crowd shot",
    "Free space",
    "90+ drama",
    "Set piece",
    "Sub scores",
    "Keeper punch",
    "Commentator curse",
    "Tactical foul",
    "Long shot",
    "Captain talk",
    "Dark horse moment",
    "Upset alert",
    "Rain game",
    "Fan costume",
    "National anthem",
    "Group chat chaos",
    "MVP moment",
)

BINGO_VARIANTS = (
    tuple(range(25)),
    (4, 7, 10, 13, 16, 19, 22, 0, 3, 9, 12, 15, 18, 21, 24, 2, 5, 8, 11, 14, 17, 20, 23, 1, 6),
    (8, 3, 14, 19, 24, 1, 6, 11, 16, 21, 0, 5, 9, 13, 17, 22, 2, 7, 12, 18, 23, 4, 10, 15, 20),
    (12, 18, 4, 20, 6, 22, 8, 14, 0, 16, 2, 24, 9, 10, 3, 15, 21, 7, 13, 1, 5, 11, 17, 23, 19),
    (16, 11, 6, 1, 21, 7, 2, 22, 17, 12, 3, 23, 9, 18, 13, 4, 24, 19, 14, 8, 0, 20, 15, 10, 5),
    (20, 15, 10, 5, 0, 21, 16, 11, 6, 1, 22, 17, 9, 7, 2, 23, 18, 13, 8, 3, 24, 19, 14, 4, 12),
    (24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 9, 12, 11, 10, 8, 7, 6, 5, 4, 3, 2, 1, 0),
    (2, 9, 16, 23, 5, 12, 19, 1, 8, 15, 22, 4, 9, 11, 18, 0, 7, 14, 21, 3, 10, 17, 24, 6, 13),
)


class PartyBingoPageRenderer:
    def __init__(self, globals_: GlobalComponents) -> None:
        self.globals = globals_

    def can_render(self, page: PageSpec) -> bool:
        return page.template_id in {"party_tool", "bingo_card"}

    def render(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id="party")

        if page.template_id == "bingo_card":
            self.render_bingo_card(canvas, page)
            return

        if "Checklist" in page.title:
            self.render_task_page(canvas, page, "Checklist", "Matchday operating checklist", CHECKLIST_TASKS)
        elif "Scoreboard" in page.title:
            self.render_scoreboard(canvas, page)
        elif "Group Chat" in page.title:
            self.render_group_chat(canvas, page)
        elif "Rules" in page.title:
            self.render_bingo_rules(canvas, page)
        elif "Office Pool" in page.title:
            self.render_pool_setup(canvas, page)
        else:
            self.render_task_page(canvas, page, "Watch party", "Party timeline", WATCH_PARTY_TASKS)

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

    def render_task_page(self, canvas: Canvas, page: PageSpec, kicker: str, title: str, tasks: tuple[PartyTask, ...]) -> None:
        self._draw_title_block(canvas, page, kicker)

        rect = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, rect)

        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, title.upper(), rect.x + 18, rect.y + rect.height - 30, self.globals.fonts["body_bold"], 9)

        xs = (rect.x + 18, rect.x + 184, rect.x + 300, rect.x + 382)
        for index, header in enumerate(("Task", "Owner", "Time", "Note")):
            canvas.setFillColor("#AAB3C2")
            draw_label(canvas, header.upper(), xs[index], rect.y + rect.height - 56, self.globals.fonts["body_bold"], 6.5)

        for row_index, task in enumerate(tasks):
            y = rect.y + rect.height - 88 - row_index * 38
            plate = rect_from_xywh(rect.x + 14, y - 9, rect.width - 28, 28)
            self.globals.draw_write_plate(canvas, plate, radius=8)

            values = (task.title, task.owner, task.timing, task.note)
            for col_index, value in enumerate(values):
                canvas.setFillColor("#F4F7FB" if col_index == 0 else "#AAB3C2")
                width = 150 if col_index == 0 else 96 if col_index in {1, 2} else 248
                self._draw_wrapped(canvas, value, xs[col_index], y, width, 1, 6.8)

    def render_pool_setup(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title_block(canvas, page, "Office pool")

        left = rect_from_xywh(48, 112, 328, 326)
        right = rect_from_xywh(408, 112, 328, 326)
        self.globals.draw_card_panel(canvas, left)
        self.globals.draw_card_panel(canvas, right)

        panels = (
            (left, "SCORING RULES", ("Correct winner +3", "Exact score +5", "First scorer +2", "Upset pick +4", "Champion pick +10")),
            (right, "POOL SETTINGS", ("Entry: free / $5 / bragging rights", "Pick lock: kickoff", "Tie-breaker: final score", "Prize: lunch or group chat fame")),
        )

        for panel, title, items in panels:
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, title, panel.x + 18, panel.y + panel.height - 30, self.globals.fonts["body_bold"], 9)

            for index, item in enumerate(items):
                y = panel.y + panel.height - 72 - index * 48
                self.globals.draw_write_plate(canvas, rect_from_xywh(panel.x + 18, y - 12, panel.width - 36, 34))
                canvas.setFillColor("#AAB3C2")
                self._draw_wrapped(canvas, item, panel.x + 34, y + 4, panel.width - 68, 2, 7.3)

    def render_scoreboard(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title_block(canvas, page, "Scoreboard")

        panel = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, panel)
        xs = (panel.x + 18, panel.x + 96, panel.x + 282, panel.x + 604)

        for index, header in enumerate(("Rank", "Player", "Picks", "Score")):
            canvas.setFillColor("#AAB3C2")
            draw_label(canvas, header.upper(), xs[index], panel.y + panel.height - 40, self.globals.fonts["body_bold"], 6.5)

        for row_index, row_data in enumerate(POOL_ROWS):
            y = panel.y + panel.height - 78 - row_index * 42
            self.globals.draw_write_plate(canvas, rect_from_xywh(panel.x + 14, y - 11, panel.width - 28, 30))

            values = (row_data.rank, row_data.player, row_data.picks, row_data.score)
            for col_index, value in enumerate(values):
                canvas.setFillColor("#A7FF00" if col_index == 0 else "#F4F7FB" if col_index == 1 else "#AAB3C2")
                font = self.globals.fonts["body_bold"] if col_index in {0, 1, 3} else self.globals.fonts["body"]
                draw_label(canvas, value, xs[col_index], y, font, 8)

    def render_group_chat(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title_block(canvas, page, "Group chat")

        panel = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, panel)

        for index, prompt in enumerate(GROUP_CHAT_PROMPTS):
            y = panel.y + panel.height - 76 - index * 54
            row = rect_from_xywh(panel.x + 24, y - 14, panel.width - 48, 38)
            self.globals.draw_write_plate(canvas, row)
            self.globals.draw_section_chip(canvas, str(index + 1), row.x + 12, y - 5, 30, color="#FFD166")
            canvas.setFillColor("#F4F7FB")
            self._draw_wrapped(canvas, prompt, row.x + 58, y + 6, row.width - 74, 2, 8)

    def render_bingo_rules(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title_block(canvas, page, "Bingo rules")

        panel = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, panel)

        rules = (
            "Pick any bingo card 1–8 before kickoff.",
            "Use digital dot stickers or printed tokens.",
            "Free space is live from kickoff.",
            "First full row, column or diagonal wins.",
            "Screenshot the winning card.",
        )

        for index, rule in enumerate(rules):
            x = panel.x + 30 + (index % 2) * 320
            y = panel.y + panel.height - 82 - (index // 2) * 84
            card = rect_from_xywh(x, y - 22, 286, 54)
            self.globals.draw_write_plate(canvas, card)
            self.globals.draw_section_chip(canvas, str(index + 1), card.x + 14, card.y + 16, 34, color="#A7FF00")
            canvas.setFillColor("#F4F7FB")
            self._draw_wrapped(canvas, rule, card.x + 62, card.y + 26, 196, 2, 7.8)

    def render_bingo_card(self, canvas: Canvas, page: PageSpec) -> None:
        card_number = max(1, min(8, int("".join(ch for ch in page.title if ch.isdigit()) or "1")))
        self._draw_title_block(canvas, page, f"Bingo card {card_number}")

        board = rect_from_xywh(176, 108, 440, 330)
        self.globals.draw_card_panel(canvas, board)

        canvas.setFillColor("#A7FF00")
        draw_centered_label(canvas, f"WATCH PARTY BINGO #{card_number}", board.x + board.width / 2, board.y + board.height - 30, self.globals.fonts["body_bold"], 10)

        grid_x = board.x + 34
        grid_y = board.y + 34
        cell = 68
        variant = BINGO_VARIANTS[card_number - 1]

        for row in range(5):
            for col in range(5):
                index = row * 5 + col
                term = BINGO_TERMS[variant[index]]
                x = grid_x + col * cell
                y = grid_y + (4 - row) * cell
                fill = "#A7FF00" if row == 2 and col == 2 else "#181A20"
                text_color = "#070A0F" if fill == "#A7FF00" else "#F4F7FB"

                canvas.setFillColor(fill)
                canvas.roundRect(x, y, cell - 6, cell - 6, 8, fill=1, stroke=0)
                canvas.setFillColor(text_color)
                self._draw_centered_wrapped(canvas, term, x + (cell - 6) / 2, y + 34, cell - 16, 2, 6.2)

        canvas.setFillColor("#AAB3C2")
        draw_centered_label(canvas, "Use bingo dot stickers from /bingo/ or printed tokens.", board.x + board.width / 2, board.y + 14, self.globals.fonts["body"], 7)

    def _draw_centered_wrapped(
        self,
        canvas: Canvas,
        text: str,
        x_center: float,
        y: float,
        width: float,
        max_lines: int,
        font_size: float,
    ) -> None:
        words = text.split()
        lines: list[str] = []
        current = ""

        for word in words:
            candidate = word if not current else f"{current} {word}"
            if canvas.stringWidth(candidate, self.globals.fonts["body_bold"], font_size) <= width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        start_y = y + (len(lines[:max_lines]) - 1) * 4
        for index, line in enumerate(lines[:max_lines]):
            draw_centered_label(canvas, line, x_center, start_y - index * 9, self.globals.fonts["body_bold"], font_size)
