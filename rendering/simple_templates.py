from __future__ import annotations
from reportlab.pdfgen.canvas import Canvas
from layout.geometry import rect_from_xywh
from models.specs import PageSpec, RenderManifest
from rendering.global_components import GlobalComponents
from rendering.text_utils import draw_centered_label, draw_label

class SimpleTemplateRenderer:
    def __init__(self, globals_: GlobalComponents) -> None:
        self.globals = globals_
    def active_nav(self, page: PageSpec) -> str | None:
        section = page.section_id.value
        if section == "onboarding": return "home"
        if section == "team_fan_identity": return "teams"
        if section == "tournament_hub":
            if page.template_id == "match_index": return "match"
            if page.template_id in {"bracket_prediction", "knockout_tracker"}: return "bracket"
            return "groups"
        if section == "stats_predictions": return "stats"
        if section == "watch_party_office_pool": return "party"
        if section == "sticker_workflow": return "stickers"
        if section in {"notes_memory", "dark_notes"}: return "notes"
        if section == "match_logs": return "match"
        return None
    def render(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        if page.page_number == 1:
            self.cover(canvas, page)
            return
        self.globals.draw_page_shell(canvas, page, manifest, self.active_nav(page))
        panel = rect_from_xywh(48, 112, 688, 326)
        self.globals.draw_card_panel(canvas, panel)
        canvas.setFillColor("#A7FF00")
        draw_label(canvas, page.section_id.value.replace("_", " ").upper(), 48, 518, self.globals.fonts["body_bold"], 8)
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, page.title, 48, 490, self.globals.fonts["display"], 30)
        canvas.setFillColor("#AAB3C2")
        draw_label(canvas, page.subtitle, 50, 468, self.globals.fonts["body"], 9)
        self.globals.draw_write_plate(canvas, rect_from_xywh(72, 158, 640, 190))
        canvas.setFillColor("#F4F7FB")
        draw_label(canvas, f"template_id: {page.template_id}", 88, 314, self.globals.fonts["mono"], 8)
        draw_label(canvas, f"data_ref: {page.data_ref or 'none'}", 88, 292, self.globals.fonts["mono"], 8)
    def cover(self, canvas: Canvas, page: PageSpec) -> None:
        self.globals.draw_page_background(canvas)
        canvas.setFillColor("#A7FF00")
        draw_centered_label(canvas, "WORLD CUP 2026", 396, 504, self.globals.fonts["body_bold"], 11)
        canvas.setFillColor("#F4F7FB")
        canvas.setFont(self.globals.fonts["display"], 64)
        canvas.drawCentredString(396, 420, "MATCHDAY")
        canvas.drawCentredString(396, 352, "NO CHAOS")
        canvas.setFillColor("#AAB3C2")
        draw_centered_label(canvas, "Premium GoodNotes fan command center with 104 match logs, office pool, bingo and 500 stickers.", 396, 318, self.globals.fonts["body"], 10)
        self.globals.draw_sticky_nav(canvas, "home")
