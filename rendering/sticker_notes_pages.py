from __future__ import annotations

from dataclasses import dataclass

from reportlab.pdfgen.canvas import Canvas

from layout.geometry import rect_from_xywh
from models.specs import PageSpec, Rect, RenderManifest
from rendering.global_components import GlobalComponents
from rendering.text_utils import draw_centered_label, draw_label, draw_right_label


@dataclass(frozen=True, slots=True)
class StickerCategory:
    title: str
    folder: str
    count: str
    body: str
    icon: str


@dataclass(frozen=True, slots=True)
class NoteRow:
    left: str
    middle: str
    right: str
    note: str


STICKER_CATEGORIES: tuple[StickerCategory, ...] = (
    StickerCategory("Flags", "/flags/", "48+", "Country markers for group tables, team hubs and match logs.", "icons_flag_generic_001.png"),
    StickerCategory("Jerseys", "/jerseys/", "96+", "Home and away style markers for fan picks and rivalry notes.", "icons_jersey_001.png"),
    StickerCategory("Events", "/events/", "140+", "Goals, VAR, cards, saves, injuries, subs and late drama.", "icons_goal_001.png"),
    StickerCategory("Tactics", "/tactics/", "80+", "Arrows, pitch zones, pressure labels and formation notes.", "icons_tactics_001.png"),
    StickerCategory("Bingo", "/bingo/", "90+", "Dots, checks, prizes, party badges and bingo callouts.", "icons_bingo_dot_001.png"),
    StickerCategory("Planner", "/icons/", "46+", "Navigation, notes, print, replay, trophy and support icons.", "icons_sticker_001.png"),
)


REPLAY_ROWS: tuple[NoteRow, ...] = (
    NoteRow("Opening match", "MEX vs RSA", "Replay", "Watch crowd energy and first-goal momentum."),
    NoteRow("Host watch", "USA group match", "Live", "Track group chat reactions and home pressure."),
    NoteRow("Upset candidate", "Dark horse fixture", "Replay", "Mark tactical swing and confidence miss."),
    NoteRow("Knockout classic", "R32 / R16", "Save", "Add to favorite moments log after full-time."),
    NoteRow("Final weekend", "Third place / Final", "Live", "Capture final mood and MVP case."),
)


MOMENT_ROWS: tuple[NoteRow, ...] = (
    NoteRow("Best goal", "Player + team", "Minute", "Why it belongs in the tournament memory page."),
    NoteRow("Best save", "Keeper", "Minute", "Shot quality, pressure and rebound control."),
    NoteRow("Best quote", "Group chat", "Mood", "Keep the funniest no-context line."),
    NoteRow("Worst miss", "Player", "Minute", "Was it nerves, angle or keeper pressure?"),
    NoteRow("Favorite crowd", "Stadium", "Match", "Flag wall, anthem, roar or full-time scenes."),
)


LEGAL_POINTS: tuple[str, ...] = (
    "This is an unofficial fan-made digital planner for personal entertainment and organization.",
    "This product is not affiliated with, endorsed by, sponsored by or connected to FIFA, World Cup, national teams, leagues, clubs, players or broadcasters.",
    "No official logos, crests, mascots, trademarks, protected marks or proprietary team artwork are included.",
    "Country names, match labels and generic fan-planning terms are used descriptively for tournament organization.",
    "Digital stickers are original generic flat icons designed for planner annotation and watch-party tracking.",
)


class StickerNotesPageRenderer:
    """Production renderer for Phase 1.13 pages.

    Covers:
    - pages 59-65: sticker workflow/catalog
    - pages 66-70: notes, replay, support and legal pages
    - pages 175-184: dark notes pages
    """

    def __init__(self, globals_: GlobalComponents) -> None:
        self.globals = globals_

    def can_render(self, page: PageSpec) -> bool:
        return 59 <= page.page_number <= 70 or 175 <= page.page_number <= 184

    def render(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        active_nav = "stickers" if 59 <= page.page_number <= 65 else "notes"
        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id=active_nav)

        if page.page_number == 59:
            self.render_sticker_index(canvas, page)
        elif page.page_number == 60:
            self.render_jersey_flag_catalog(canvas, page)
        elif page.page_number == 61:
            self.render_event_catalog(canvas, page)
        elif page.page_number == 62:
            self.render_tactics_catalog(canvas, page)
        elif page.page_number == 63:
            self.render_bingo_dot_sheet(canvas, page)
        elif page.page_number == 64:
            self.render_planner_icons_catalog(canvas, page)
        elif page.page_number == 65:
            self.render_sticker_placement_examples(canvas, page)
        elif page.page_number == 66:
            self.render_replay_watchlist(canvas, page)
        elif page.page_number == 67:
            self.render_favorite_moments_log(canvas, page)
        elif page.page_number == 68:
            self.render_final_recap(canvas, page)
        elif page.page_number == 69:
            self.render_support_cta(canvas, page)
        elif page.page_number == 70:
            self.render_legal_disclaimer(canvas, page)
        elif 175 <= page.page_number <= 184:
            self.render_dark_notes(canvas, page)
        else:
            raise ValueError(f"StickerNotesPageRenderer cannot render page {page.page_number}")

    def _draw_title(self, canvas: Canvas, page: PageSpec, kicker: str) -> None:
        canvas.saveState()
        canvas.setFillColor("#A7FF00")
        draw_label(canvas, kicker.upper(), 48, 518, self.globals.fonts["body_bold"], 8)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, page.title, 48, 490, self.globals.fonts["display"], 30)
        canvas.setFillColor("#AAB3C2")
        draw_label(canvas, page.subtitle, 50, 468, self.globals.fonts["body"], 9.5)
        canvas.restoreState()

    def _draw_wrapped(self, canvas: Canvas, text: str, x: float, y: float, width: float, max_lines: int = 3, font_size: float = 7.4) -> None:
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

    def _draw_table(self, canvas: Canvas, rect: Rect, headers: tuple[str, ...], rows: tuple[tuple[str, ...], ...], col_widths: tuple[float, ...]) -> None:
        x_positions = [rect.x + 16]
        for width in col_widths[:-1]:
            x_positions.append(x_positions[-1] + width)
        canvas.setFillColor("#AAB3C2")
        for index, header in enumerate(headers):
            draw_label(canvas, header.upper(), x_positions[index], rect.y + rect.height - 30, self.globals.fonts["body_bold"], 6.7)
        start_y = rect.y + rect.height - 60
        row_h = 34
        for row_index, row in enumerate(rows):
            y = start_y - row_index * row_h
            row_rect = rect_from_xywh(rect.x + 12, y - 9, rect.width - 24, 26)
            self.globals.draw_write_plate(canvas, row_rect, radius=8, opacity=0.90)
            for col_index, value in enumerate(row):
                canvas.setFillColor("#F4F7FB" if col_index == 0 else "#AAB3C2")
                font = self.globals.fonts["body_bold"] if col_index == 0 else self.globals.fonts["body"]
                draw_label(canvas, value, x_positions[col_index], y, font, 7.2)

    def render_sticker_index(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Premium sticker system")
        for index, category in enumerate(STICKER_CATEGORIES):
            col = index % 3
            row = index // 3
            x = 48 + col * 238
            y = 294 - row * 142
            card = rect_from_xywh(x, y, 214, 118)
            self.globals.draw_card_panel(canvas, card)
            self.globals.icons.draw_icon(canvas, category.icon, x + 174, y + 78, size=24, allow_missing=True)
            self.globals.draw_section_chip(canvas, category.count, x + 16, y + 76, 54, color="#FFD166")
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, category.title, x + 16, y + 56, self.globals.fonts["body_bold"], 11)
            canvas.setFillColor("#A7FF00")
            draw_label(canvas, category.folder, x + 16, y + 40, self.globals.fonts["mono"], 7)
            canvas.setFillColor("#AAB3C2")
            self._draw_wrapped(canvas, category.body, x + 16, y + 26, 172, 2)
        note = rect_from_xywh(48, 92, 688, 42)
        self.globals.draw_write_plate(canvas, note)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "Premium target: 500 transparent PNG/SVG stickers at 300 DPI, organized by category folders.", 64, 116, self.globals.fonts["body_bold"], 8.5)

    def render_jersey_flag_catalog(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Flags + jerseys")
        panel = rect_from_xywh(48, 110, 688, 328)
        self.globals.draw_card_panel(canvas, panel)
        samples = (("Flag marker", "Group table + match log", "icons_flag_generic_001.png"), ("Home jersey", "Favorite team hub", "icons_jersey_001.png"), ("Away jersey", "Rival watch", "icons_jersey_001.png"), ("Winner badge", "Bracket + recap", "icons_trophy_generic_001.png"), ("Captain star", "Squad card", "icons_star_001.png"), ("Host note", "Watch party", "icons_party_001.png"))
        self._draw_catalog_grid(canvas, panel, samples)

    def render_event_catalog(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Live event stickers")
        panel = rect_from_xywh(48, 110, 688, 328)
        self.globals.draw_card_panel(canvas, panel)
        samples = (("Goal", "Timeline + recap", "icons_goal_001.png"), ("VAR", "Controversy log", "icons_var_001.png"), ("Yellow / red", "Discipline notes", "icons_card_001.png"), ("Save", "Keeper watch", "icons_save_001.png"), ("Sub", "Tactical shift", "icons_player_001.png"), ("Late drama", "90+ moment", "icons_clock_001.png"))
        self._draw_catalog_grid(canvas, panel, samples)

    def render_tactics_catalog(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Tactics stickers")
        panel = rect_from_xywh(48, 110, 688, 328)
        self.globals.draw_card_panel(canvas, panel)
        samples = (("Press", "Momentum arrow", "icons_tactics_001.png"), ("Low block", "Shape note", "icons_tactics_001.png"), ("Counter", "Fast break", "icons_path_001.png"), ("Set piece", "Corner/free kick", "icons_target_001.png"), ("Formation", "Pitch overlay", "icons_table_001.png"), ("Swing", "Tactical recap", "icons_review_001.png"))
        self._draw_catalog_grid(canvas, panel, samples)

    def render_bingo_dot_sheet(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Bingo markers")
        panel = rect_from_xywh(48, 110, 688, 328)
        self.globals.draw_card_panel(canvas, panel)
        labels = ("GOAL", "VAR", "SAVE", "CARD", "POST", "FANS", "SUB", "FREE", "UPSET", "90+", "PEN", "MVP")
        for index, label in enumerate(labels):
            col = index % 6
            row = index // 6
            x = 86 + col * 102
            y = 324 - row * 112
            dot = rect_from_xywh(x, y, 54, 54)
            fill = "#A7FF00" if label == "FREE" else "#1A2230"
            self.globals.draw_card_panel(canvas, dot, radius=18, fill=fill)
            canvas.setFillColor("#070A0F" if label == "FREE" else "#F4F7FB")
            draw_centered_label(canvas, label, x + 27, y + 22, self.globals.fonts["body_bold"], 7)
            canvas.setFillColor("#AAB3C2")
            draw_centered_label(canvas, "bingo dot", x + 27, y - 14, self.globals.fonts["body"], 6.5)

    def render_planner_icons_catalog(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Planner icon catalog")
        panel = rect_from_xywh(48, 110, 688, 328)
        self.globals.draw_card_panel(canvas, panel)
        samples = (("PDF", "Import guide", "icons_pdf_001.png"), ("Print", "Compatibility", "icons_print_001.png"), ("Link", "Navigation", "icons_link_001.png"), ("Notes", "Memory pages", "icons_notes_001.png"), ("Pen", "Writing zones", "icons_pen_001.png"), ("Support", "Help CTA", "icons_info_001.png"))
        self._draw_catalog_grid(canvas, panel, samples)

    def render_sticker_placement_examples(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Placement examples")
        left = rect_from_xywh(48, 112, 328, 326)
        right = rect_from_xywh(408, 112, 328, 326)
        self.globals.draw_card_panel(canvas, left)
        self.globals.draw_card_panel(canvas, right)
        steps = (("1", "Drop jersey markers into score boxes before kickoff."), ("2", "Add goal, VAR and card icons to the 0-90+ timeline."), ("3", "Use tactics arrows on the pitch panel after halftime."), ("4", "Mark bingo cells live during watch parties."))
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "GOODNOTES WORKFLOW", left.x + 18, left.y + left.height - 30, self.globals.fonts["body_bold"], 9)
        for index, (number, body) in enumerate(steps):
            y = left.y + left.height - 70 - index * 58
            self.globals.draw_section_chip(canvas, number, left.x + 18, y - 4, 32, color="#FFD166")
            canvas.setFillColor("#AAB3C2")
            self._draw_wrapped(canvas, body, left.x + 62, y + 2, 230, 2)
        self._draw_mock_timeline(canvas, right)

    def _draw_catalog_grid(self, canvas: Canvas, panel: Rect, samples: tuple[tuple[str, str, str], ...]) -> None:
        for index, (title, body, icon) in enumerate(samples):
            col = index % 3
            row = index // 3
            x = panel.x + 24 + col * 214
            y = panel.y + panel.height - 118 - row * 126
            card = rect_from_xywh(x, y, 180, 92)
            self.globals.draw_write_plate(canvas, card, radius=10)
            self.globals.icons.draw_icon(canvas, icon, x + 16, y + 48, size=24, allow_missing=True)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, title, x + 52, y + 62, self.globals.fonts["body_bold"], 8.5)
            canvas.setFillColor("#AAB3C2")
            self._draw_wrapped(canvas, body, x + 52, y + 44, 106, 2, font_size=7)
            canvas.setFillColor("#A7FF00")
            draw_label(canvas, "300 DPI PNG/SVG", x + 16, y + 16, self.globals.fonts["mono"], 6)

    def _draw_mock_timeline(self, canvas: Canvas, rect: Rect) -> None:
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "MATCH LOG DROP ZONE", rect.x + 18, rect.y + rect.height - 30, self.globals.fonts["body_bold"], 9)
        timeline = rect_from_xywh(rect.x + 28, rect.y + 84, rect.width - 56, 86)
        self.globals.draw_write_plate(canvas, timeline)
        canvas.setStrokeColor("#394457")
        canvas.line(timeline.x + 22, timeline.y + 42, timeline.x + timeline.width - 22, timeline.y + 42)
        icons = (("icons_goal_001.png", "15"), ("icons_var_001.png", "45"), ("icons_card_001.png", "60"), ("icons_star_001.png", "90+"))
        for index, (icon, minute) in enumerate(icons):
            x = timeline.x + 34 + index * 70
            self.globals.icons.draw_icon(canvas, icon, x, timeline.y + 48, size=22, allow_missing=True)
            canvas.setFillColor("#A7FF00")
            draw_centered_label(canvas, minute, x + 11, timeline.y + 22, self.globals.fonts["mono"], 7)
        canvas.setFillColor("#AAB3C2")
        self._draw_wrapped(canvas, "Use transparent stickers over dark write plates so ink and icons stay readable in dark mode.", rect.x + 28, rect.y + 54, rect.width - 56, 3)

    def render_replay_watchlist(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Replay queue")
        panel = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, panel)
        rows = tuple((row.left, row.middle, row.right, row.note) for row in REPLAY_ROWS)
        self._draw_table(canvas, panel, ("Slot", "Match", "Mode", "Reason"), rows, (138, 176, 78, 260))

    def render_favorite_moments_log(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Memory log")
        panel = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, panel)
        rows = tuple((row.left, row.middle, row.right, row.note) for row in MOMENT_ROWS)
        self._draw_table(canvas, panel, ("Moment", "Who", "When", "Why it mattered"), rows, (138, 176, 78, 260))

    def render_final_recap(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Tournament recap")
        cards = (("Champion pick", "Who lifted the trophy and did your bracket survive?"), ("Best match", "The replay you would recommend first."), ("MVP case", "Player who owned the tournament narrative."), ("Biggest shock", "Upset, VAR call or group-stage collapse."), ("Favorite memory", "Watch party, group chat or full-time scene."), ("Next tournament note", "What to track better next time."))
        for index, (title, body) in enumerate(cards):
            col = index % 3
            row = index // 3
            x = 48 + col * 238
            y = 288 - row * 132
            card = rect_from_xywh(x, y, 214, 104)
            self.globals.draw_write_plate(canvas, card)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, title, x + 16, y + 66, self.globals.fonts["body_bold"], 9)
            canvas.setFillColor("#AAB3C2")
            self._draw_wrapped(canvas, body, x + 16, y + 46, 176, 3)

    def render_support_cta(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "Buyer support")
        left = rect_from_xywh(48, 112, 328, 326)
        right = rect_from_xywh(408, 112, 328, 326)
        self.globals.draw_card_panel(canvas, left)
        self.globals.draw_card_panel(canvas, right)
        support_steps = (("Import", "Use the hyperlinked GoodNotes PDF first."), ("Fallback", "Use the flattened PDF if your app shows layer issues."), ("Stickers", "Import PNG files as elements or image stickers."), ("Printing", "Print selected party sheets rather than the full dark planner."))
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "COMMON FIXES", left.x + 18, left.y + left.height - 30, self.globals.fonts["body_bold"], 9)
        for index, (title, body) in enumerate(support_steps):
            y = left.y + left.height - 70 - index * 58
            plate = rect_from_xywh(left.x + 18, y - 10, left.width - 36, 38)
            self.globals.draw_write_plate(canvas, plate)
            canvas.setFillColor("#A7FF00")
            draw_label(canvas, title.upper(), plate.x + 10, y + 8, self.globals.fonts["body_bold"], 6.5)
            canvas.setFillColor("#AAB3C2")
            self._draw_wrapped(canvas, body, plate.x + 96, y + 8, 190, 2)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "REVIEW PROMPT", right.x + 18, right.y + right.height - 30, self.globals.fonts["body_bold"], 9)
        self.globals.draw_write_plate(canvas, rect_from_xywh(right.x + 24, right.y + 150, right.width - 48, 110))
        canvas.setFillColor("#AAB3C2")
        self._draw_wrapped(canvas, "If this planner helped your matchday workflow, leave a quick review mentioning navigation, stickers, match logs or watch-party tools.", right.x + 42, right.y + 226, right.width - 84, 5, 8)
        self.globals.draw_section_chip(canvas, "THANK YOU", right.x + 42, right.y + 178, 112, color="#FFD166")

    def render_legal_disclaimer(self, canvas: Canvas, page: PageSpec) -> None:
        self._draw_title(canvas, page, "IP disclaimer")
        panel = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, panel)
        canvas.setFillColor("#FFD166")
        draw_label(canvas, "UNOFFICIAL FAN-MADE PRODUCT", panel.x + 20, panel.y + panel.height - 34, self.globals.fonts["body_bold"], 9)
        for index, point in enumerate(LEGAL_POINTS):
            y = panel.y + panel.height - 72 - index * 48
            row = rect_from_xywh(panel.x + 18, y - 12, panel.width - 36, 36)
            self.globals.draw_write_plate(canvas, row)
            canvas.setFillColor("#A7FF00")
            draw_label(canvas, f"{index + 1:02d}", row.x + 10, y + 2, self.globals.fonts["mono"], 7)
            canvas.setFillColor("#F4F7FB")
            self._draw_wrapped(canvas, point, row.x + 44, y + 4, row.width - 62, 2, 7.2)

    def render_dark_notes(self, canvas: Canvas, page: PageSpec) -> None:
        note_number = page.page_number - 174
        self._draw_title(canvas, page, f"Dark notes {note_number:02d}")
        big_plate = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_write_plate(canvas, big_plate, radius=14, opacity=0.90)
        canvas.setStrokeColor("#394457")
        canvas.setLineWidth(0.6)
        for index in range(1, 11):
            y = big_plate.y + 28 + index * 26
            canvas.line(big_plate.x + 22, y, big_plate.x + big_plate.width - 22, y)
        canvas.setFillColor("#AAB3C2")
        draw_label(canvas, "Use white, volt, gold, cyan or red digital ink for maximum dark-mode contrast.", big_plate.x + 24, big_plate.y + 18, self.globals.fonts["body"], 8)
