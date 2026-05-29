from __future__ import annotations
from dataclasses import dataclass
from reportlab.pdfgen.canvas import Canvas
from layout.component_boxes import nav_boxes
from layout.constants import LETTER_LANDSCAPE
from models.specs import PageSpec, Rect, RenderManifest
from registries.nav_registry import CANONICAL_NAV
from rendering.color_utils import alpha_color, hex_color
from rendering.icon_loader import IconLoader
from rendering.text_utils import draw_centered_label, draw_label, draw_right_label

@dataclass(frozen=True, slots=True)
class ComponentTheme:
    background: str = "#070A0F"
    surface: str = "#101722"
    surface_alt: str = "#1A2230"
    line: str = "#394457"
    write_plate: str = "#181A20"
    ink: str = "#F4F7FB"
    muted_ink: str = "#AAB3C2"
    primary: str = "#A7FF00"
    secondary: str = "#FFD166"
    accent: str = "#35D6E8"
    danger: str = "#FF4D6D"

class GlobalComponents:
    def __init__(self, font_map: dict[str, str], icon_loader: IconLoader | None = None) -> None:
        self.fonts = font_map
        self.icons = icon_loader or IconLoader()
        self.theme = ComponentTheme()
    def draw_page_background(self, canvas: Canvas) -> None:
        canvas.setFillColor(hex_color(self.theme.background))
        canvas.rect(0, 0, LETTER_LANDSCAPE.width, LETTER_LANDSCAPE.height, fill=1, stroke=0)
    def draw_top_context_bar(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest) -> None:
        if page.page_number == 1:
            return
        canvas.setFillColor(hex_color(self.theme.surface))
        canvas.roundRect(24, 552, 744, 36, 8, fill=1, stroke=0)
        if page.primary_icon:
            self.icons.draw_icon(canvas, page.primary_icon, 36, 558, 22, True)
        canvas.setFillColor(hex_color(self.theme.primary))
        draw_label(canvas, page.section_id.value.replace("_", " ").upper(), 66, 572, self.fonts["body_bold"], 7)
        canvas.setFillColor(hex_color(self.theme.ink))
        draw_label(canvas, page.title, 66, 558, self.fonts["body_bold"], 11)
        canvas.setFillColor(hex_color(self.theme.muted_ink))
        draw_right_label(canvas, f"{page.page_number}/{manifest.total_pages}", 748, 562, self.fonts["mono"], 8)
    def draw_sticky_nav(self, canvas: Canvas, active_nav_id: str | None = None) -> None:
        boxes = nav_boxes()
        for nav in CANONICAL_NAV:
            box = boxes[f"nav.{nav.nav_id}"].rect
            active = nav.nav_id == active_nav_id
            canvas.setFillColor(hex_color(self.theme.primary if active else self.theme.surface_alt))
            canvas.roundRect(box.x, box.y, box.width, box.height, 7, fill=1, stroke=0)
            canvas.setFillColor(hex_color(self.theme.background if active else self.theme.ink))
            draw_centered_label(canvas, nav.label, box.x + box.width / 2, box.y + 18, self.fonts["body_bold"], 6.7)
    def draw_card_panel(self, canvas: Canvas, rect: Rect, radius: float = 12, fill: str | None = None, stroke: str | None = None) -> None:
        canvas.setFillColor(hex_color(fill or self.theme.surface))
        canvas.setStrokeColor(hex_color(stroke or self.theme.line))
        canvas.roundRect(rect.x, rect.y, rect.width, rect.height, radius, fill=1, stroke=1)
    def draw_write_plate(self, canvas: Canvas, rect: Rect, radius: float = 10, opacity: float = 0.90) -> None:
        canvas.setFillColor(alpha_color(self.theme.write_plate, opacity))
        canvas.roundRect(rect.x, rect.y, rect.width, rect.height, radius, fill=1, stroke=0)
    def draw_section_chip(self, canvas: Canvas, text: str, x: float, y: float, width: float, color: str | None = None) -> None:
        canvas.setFillColor(hex_color(color or self.theme.primary))
        canvas.roundRect(x, y, width, 22, 11, fill=1, stroke=0)
        canvas.setFillColor(hex_color(self.theme.background))
        draw_centered_label(canvas, text.upper(), x + width / 2, y + 7, self.fonts["body_bold"], 7)
    def draw_page_shell(self, canvas: Canvas, page: PageSpec, manifest: RenderManifest, active_nav_id: str | None = None) -> None:
        self.draw_page_background(canvas)
        self.draw_top_context_bar(canvas, page, manifest)
        self.draw_sticky_nav(canvas, active_nav_id)
