from __future__ import annotations
from reportlab.pdfgen.canvas import Canvas
from layout.geometry import rect_to_reportlab_tuple
from layout.hotspot_resolver import HotspotResolver
from models.specs import LinkSpec, PageSpec

class ReportLabHyperlinkRenderer:
    def __init__(self) -> None:
        self.resolver = HotspotResolver()
    @staticmethod
    def page_destination_name(page_number: int) -> str:
        return f"page_{page_number:03d}"
    def register_page_bookmark(self, canvas: Canvas, page: PageSpec) -> None:
        canvas.bookmarkPage(self.page_destination_name(page.page_number), fit="Fit")
    def register_link(self, canvas: Canvas, link: LinkSpec) -> None:
        if link.target_page is None:
            raise ValueError(f"Internal link missing target_page: {link.link_id}")
        rect = self.resolver.resolve(link)
        rect.validate_min_touch_target()
        canvas.linkAbsolute(contents=link.label, destinationname=self.page_destination_name(link.target_page), Rect=rect_to_reportlab_tuple(rect), Border="[0 0 0]")
    def register_links_for_page(self, canvas: Canvas, page_number: int, links: tuple[LinkSpec, ...]) -> None:
        for link in links:
            if link.source_page == page_number:
                self.register_link(canvas, link)
