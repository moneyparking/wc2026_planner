from __future__ import annotations

from dataclasses import dataclass
from reportlab.pdfgen.canvas import Canvas

from layout.geometry import rect_from_xywh
from models.specs import PageSpec, RenderManifest
from rendering.global_components import GlobalComponents
from rendering.text_utils import draw_centered_label, draw_label


@dataclass(frozen=True, slots=True)
class BundleItem:
    number: str
    title: str
    body: str
    icon: str


@dataclass(frozen=True, slots=True)
class DashboardCard:
    title: str
    body: str
    metric: str
    icon: str


@dataclass(frozen=True, slots=True)
class InstructionStep:
    number: str
    title: str
    body: str
    icon: str


@dataclass(frozen=True, slots=True)
class TournamentStat:
    value: str
    label: str
    body: str


BUNDLE_ITEMS: tuple[BundleItem, ...] = (
    BundleItem("01", "GoodNotes PDF", "184-page hyperlinked fan command center with 104 dedicated match logs.", "icons_pdf_001.png"),
    BundleItem("02", "Flattened PDF", "Compatibility fallback for print workflows and annotation apps.", "icons_print_001.png"),
    BundleItem("03", "Bingo Bonus", "Eight watch-party bingo cards for friends, group chats and office pools.", "icons_bingo_001.png"),
    BundleItem("04", "Sticker ZIP", "500 transparent PNG/SVG flags, jerseys, events, tactics and bingo icons.", "icons_sticker_001.png"),
    BundleItem("05", "Quick Guide", "Import notes, link mode, sticker workflow, print tips and support rules.", "icons_info_001.png"),
)

DASHBOARD_CARDS: tuple[DashboardCard, ...] = (
    DashboardCard("Groups", "Update 12 live tables with P/W/D/L/GD/PTS columns.", "12", "icons_table_001.png"),
    DashboardCard("Match Logs", "Jump to any fixture and track score, timeline, tactics and recap.", "104", "icons_match_001.png"),
    DashboardCard("Bracket", "Predict the route from Round of 32 to Champion pick.", "R32", "icons_bracket_001.png"),
    DashboardCard("Party", "Run bingo, snacks, group chat prompts and office pool scoring.", "8", "icons_party_001.png"),
)

QUICK_START_STEPS: tuple[InstructionStep, ...] = (
    InstructionStep("1", "Import the GoodNotes PDF", "Open the hyperlinked PDF first. Use the flattened PDF only if your app renders layers oddly.", "icons_pdf_001.png"),
    InstructionStep("2", "Use viewing mode", "Tap tabs and index rows in viewing mode. In pen mode, long-press links if needed.", "icons_hand_tap_001.png"),
    InstructionStep("3", "Mark every match live", "Use white, volt, gold, cyan or red ink over dark write plates.", "icons_pen_001.png"),
    InstructionStep("4", "Drop stickers into timelines", "Add goals, VAR, cards, jerseys and bingo dots from the PNG sticker pack.", "icons_sticker_001.png"),
)

LINK_MODE_STEPS: tuple[InstructionStep, ...] = (
    InstructionStep("A", "Read-only mode", "Best for navigation. Tap HOME, GROUPS, MATCH, BRACKET and page cards directly.", "icons_eye_001.png"),
    InstructionStep("B", "Pen mode", "Best for writing. Long-press or use your app link tool when a tap draws ink.", "icons_pen_001.png"),
    InstructionStep("C", "Index rows", "Match index rows are full-width links, sized for finger taps and Apple Pencil workflow.", "icons_list_001.png"),
    InstructionStep("D", "Back links", "Each dedicated match log returns to index block 001–036, 037–072 or 073–104.", "icons_link_001.png"),
)

STICKER_WORKFLOW_STEPS: tuple[InstructionStep, ...] = (
    InstructionStep("1", "Team markers", "Use jersey and flag-style markers on team hubs, group tables and match logs.", "icons_jersey_001.png"),
    InstructionStep("2", "Live events", "Drop goal, VAR, card, save and upset icons onto the 0–90+ timeline.", "icons_goal_001.png"),
    InstructionStep("3", "Tactics", "Use pitch, arrows, pressure and formation stickers to map match momentum.", "icons_tactics_001.png"),
    InstructionStep("4", "Party games", "Use bingo dots, check marks and winner badges during watch parties.", "icons_bingo_dot_001.png"),
)

PRINT_GUIDE_STEPS: tuple[InstructionStep, ...] = (
    InstructionStep("1", "Use flattened PDF", "The flattened version removes hyperlinks and keeps page visuals stable.", "icons_print_001.png"),
    InstructionStep("2", "Choose Letter or A4", "Use Letter for US buyers and A4 for UK/EU print workflows.", "icons_pdf_001.png"),
    InstructionStep("3", "Print bingo separately", "Bingo cards are designed for digital dots or printed watch-party tokens.", "icons_bingo_card_001.png"),
    InstructionStep("4", "Expect dark pages", "This is a dark-mode digital planner. Print key party sheets rather than the full planner.", "icons_info_001.png"),
)

TOURNAMENT_STATS: tuple[TournamentStat, ...] = (
    TournamentStat("48", "Teams", "Expanded tournament field."),
    TournamentStat("12", "Groups", "Twelve groups of four."),
    TournamentStat("104", "Matches", "Dedicated log for every fixture."),
    TournamentStat("32", "Knockout", "Round-of-32 support."),
)


class CorePageRenderer:
    def __init__(self, globals_: GlobalComponents) -> None:
        self.globals = globals_

    def can_render(self, page: PageSpec) -> bool:
        return page.template_id in {
            "cover_hero",
            "bundle_map",
            "dashboard",
            "instruction_cards",
            "support_guide",
            "sticker_preview",
            "print_guide",
            "upsell_sample",
            "tournament_overview",
        } and page.page_number <= 9

    def render(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        if page.template_id == "cover_hero":
            self.render_cover(canvas)
        elif page.template_id == "bundle_map":
            self.render_bundle_map(canvas, page, manifest)
        elif page.template_id == "dashboard":
            self.render_dashboard(canvas, page, manifest)
        elif page.template_id == "instruction_cards":
            self.render_step_page(canvas, page, manifest, "Setup", QUICK_START_STEPS, "home")
        elif page.template_id == "support_guide":
            self.render_step_page(canvas, page, manifest, "Navigation", LINK_MODE_STEPS, "home")
        elif page.template_id == "sticker_preview":
            self.render_step_page(canvas, page, manifest, "Sticker system", STICKER_WORKFLOW_STEPS, "stickers")
        elif page.template_id == "print_guide":
            self.render_step_page(canvas, page, manifest, "Compatibility", PRINT_GUIDE_STEPS, "home")
        elif page.template_id == "upsell_sample":
            self.render_sticker_sample(canvas, page, manifest)
        elif page.template_id == "tournament_overview":
            self.render_tournament_overview(canvas, page, manifest)
        else:
            raise ValueError(f"CorePageRenderer cannot render template {page.template_id}")

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
        max_lines: int = 3,
        font_size: float = 7.5,
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

    def _draw_step_grid(self, canvas: Canvas, steps: tuple[InstructionStep, ...]) -> None:
        for index, step in enumerate(steps):
            col = index % 2
            row = index // 2
            x = 48 + col * 360
            y = 338 - row * 116
            card = rect_from_xywh(x, y, 336, 96)
            self.globals.draw_card_panel(canvas, card)
            self.globals.draw_section_chip(canvas, step.number, x + 16, y + 58, 34, color="#FFD166")
            self.globals.icons.draw_icon(canvas, step.icon, x + 294, y + 56, size=24, allow_missing=True)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, step.title, x + 64, y + 64, self.globals.fonts["body_bold"], 11)
            canvas.setFillColor("#AAB3C2")
            self._draw_wrapped(canvas, step.body, x + 64, y + 44, 244, 2)

    def render_cover(self, canvas: Canvas) -> None:
        self.globals.draw_page_background(canvas)
        canvas.setFillColor("#A7FF00")
        draw_centered_label(canvas, "WORLD CUP 2026", 396, 504, self.globals.fonts["body_bold"], 11)

        canvas.setFillColor("#F4F7FB")
        canvas.setFont(self.globals.fonts["display"], 64)
        canvas.drawCentredString(396, 420, "MATCHDAY")
        canvas.drawCentredString(396, 352, "NO CHAOS")

        canvas.setFillColor("#AAB3C2")
        draw_centered_label(
            canvas,
            "Premium GoodNotes fan command center with 104 match logs, office pool, bingo and 500 stickers.",
            396,
            318,
            self.globals.fonts["body"],
            10,
        )

        for index, (value, label) in enumerate((("184", "pages"), ("104", "match logs"), ("12", "groups"), ("500", "stickers"))):
            card = rect_from_xywh(144 + index * 132, 218, 112, 68)
            self.globals.draw_card_panel(canvas, card)
            canvas.setFillColor("#A7FF00")
            draw_centered_label(canvas, value, card.x + card.width / 2, card.y + 36, self.globals.fonts["body_bold"], 18)
            canvas.setFillColor("#AAB3C2")
            draw_centered_label(canvas, label.upper(), card.x + card.width / 2, card.y + 18, self.globals.fonts["body_bold"], 7)

        cta = rect_from_xywh(296, 116, 200, 44)
        canvas.setFillColor("#A7FF00")
        canvas.roundRect(cta.x, cta.y, cta.width, cta.height, 12, fill=1, stroke=0)
        canvas.setFillColor("#070A0F")
        draw_centered_label(canvas, "TAP TO START", 396, 132, self.globals.fonts["body_bold"], 10)
        self.globals.draw_sticky_nav(canvas, "home")

    def render_bundle_map(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id="home")
        self._draw_title_block(canvas, page, "Instant download")

        for index, item in enumerate(BUNDLE_ITEMS):
            col = index % 3
            row = index // 3
            x = 48 + col * 238
            y = 314 - row * 132
            card = rect_from_xywh(x, y, 214, 104)
            self.globals.draw_card_panel(canvas, card)
            self.globals.draw_section_chip(canvas, item.number, x + 14, y + 66, 42)
            self.globals.icons.draw_icon(canvas, item.icon, x + 174, y + 66, size=24, allow_missing=True)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, item.title, x + 16, y + 50, self.globals.fonts["body_bold"], 11)
            canvas.setFillColor("#AAB3C2")
            self._draw_wrapped(canvas, item.body, x + 16, y + 32, 180, 2)

        note = rect_from_xywh(48, 104, 688, 44)
        self.globals.draw_write_plate(canvas, note)
        canvas.setFillColor("#FFD166")
        draw_label(canvas, "POSITIONING:", 64, 128, self.globals.fonts["body_bold"], 8)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "Not just a bracket. Track every World Cup 2026 matchday in one fan command center.", 132, 128, self.globals.fonts["body"], 9)

    def render_dashboard(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id="home")
        self._draw_title_block(canvas, page, "Fan command center")

        for index, card_data in enumerate(DASHBOARD_CARDS):
            x = 48 + index * 176
            y = 352
            card = rect_from_xywh(x, y, 156, 92)
            self.globals.draw_card_panel(canvas, card)
            self.globals.icons.draw_icon(canvas, card_data.icon, x + 116, y + 54, size=24, allow_missing=True)
            canvas.setFillColor("#A7FF00")
            draw_label(canvas, card_data.metric, x + 16, y + 58, self.globals.fonts["body_bold"], 18)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, card_data.title, x + 16, y + 38, self.globals.fonts["body_bold"], 10)
            canvas.setFillColor("#AAB3C2")
            self._draw_wrapped(canvas, card_data.body, x + 16, y + 24, 124, 2, 7.2)

        for panel, title, rows in (
            (
                rect_from_xywh(48, 142, 316, 170),
                "TODAY MATCHDAY ROUTINE",
                ("Check group table", "Open match log", "Pick winner + confidence", "Drop goal / VAR sticker", "Update stats + recap"),
            ),
            (
                rect_from_xywh(388, 142, 348, 170),
                "NEXT WATCH BLOCK",
                ("Opening match: MEX vs RSA", "Host watch: USA vs PAR", "Statement game: BRA vs MAR"),
            ),
        ):
            self.globals.draw_card_panel(canvas, panel)
            canvas.setFillColor("#F4F7FB")
            draw_label(canvas, title, panel.x + 20, panel.y + panel.height - 32, self.globals.fonts["body_bold"], 10)
            canvas.setFillColor("#AAB3C2")
            for index, line in enumerate(rows):
                draw_label(canvas, f"• {line}", panel.x + 24, panel.y + panel.height - 56 - index * 22, self.globals.fonts["body"], 9)

    def render_step_page(
        self,
        canvas: Canvas,
        page: PageSpec,
        manifest: RenderManifest,
        kicker: str,
        steps: tuple[InstructionStep, ...],
        active_nav: str,
    ) -> None:
        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id=active_nav)
        self._draw_title_block(canvas, page, kicker)
        self._draw_step_grid(canvas, steps)

    def render_sticker_sample(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id="stickers")
        self._draw_title_block(canvas, page, "Bundle value")

        panel = rect_from_xywh(48, 128, 688, 310)
        self.globals.draw_card_panel(canvas, panel)
        sample_icons = (
            "icons_goal_001.png",
            "icons_var_001.png",
            "icons_card_001.png",
            "icons_save_001.png",
            "icons_jersey_001.png",
            "icons_flag_generic_001.png",
            "icons_bingo_dot_001.png",
            "icons_tactics_001.png",
            "icons_trophy_generic_001.png",
            "icons_star_001.png",
            "icons_chat_001.png",
            "icons_print_001.png",
        )

        for index, icon in enumerate(sample_icons):
            col = index % 6
            row = index // 6
            x = 96 + col * 96
            y = 324 - row * 96
            self.globals.draw_write_plate(canvas, rect_from_xywh(x - 18, y - 18, 60, 60), radius=12)
            self.globals.icons.draw_icon(canvas, icon, x, y, size=24, allow_missing=True)

        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "Included in Premium: 500 transparent PNG/SVG files", 96, 164, self.globals.fonts["body_bold"], 13)
        canvas.setFillColor("#AAB3C2")
        draw_label(canvas, "Use them on match timelines, group tables, team hubs, bingo cards and party pages.", 96, 144, self.globals.fonts["body"], 9)

    def render_tournament_overview(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        self.globals.draw_page_shell(canvas, page, manifest, active_nav_id="groups")
        self._draw_title_block(canvas, page, "Tournament hub")

        for index, stat in enumerate(TOURNAMENT_STATS):
            x = 48 + index * 176
            y = 336
            card = rect_from_xywh(x, y, 156, 102)
            self.globals.draw_card_panel(canvas, card)
            canvas.setFillColor("#A7FF00")
            draw_centered_label(canvas, stat.value, x + 78, y + 58, self.globals.fonts["body_bold"], 22)
            canvas.setFillColor("#F4F7FB")
            draw_centered_label(canvas, stat.label.upper(), x + 78, y + 38, self.globals.fonts["body_bold"], 8)
            canvas.setFillColor("#AAB3C2")
            draw_centered_label(canvas, stat.body, x + 78, y + 20, self.globals.fonts["body"], 7)

        map_panel = rect_from_xywh(48, 128, 688, 156)
        self.globals.draw_card_panel(canvas, map_panel)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "PREMIUM FLOW", 72, 248, self.globals.fonts["body_bold"], 10)
        canvas.setFillColor("#AAB3C2")
        draw_label(canvas, "Groups → Match Index → Dedicated Match Log → Stats → Bracket → Final Recap", 72, 224, self.globals.fonts["body"], 11)
        canvas.setFillColor("#FFD166")
        draw_label(canvas, "DESIGN RULE:", 72, 184, self.globals.fonts["body_bold"], 8)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, "Every core action has a large tap target and a visible dark write plate.", 142, 184, self.globals.fonts["body"], 9)
