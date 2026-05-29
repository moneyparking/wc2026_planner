from __future__ import annotations
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from layout.constants import LETTER_LANDSCAPE
from models.specs import RenderManifest
from rendering.hyperlink_renderer import ReportLabHyperlinkRenderer
from rendering.renderer_registry import RendererRegistry

class PlannerPDFSmokeRenderer:
    def __init__(self) -> None:
        self.page_renderers = RendererRegistry()
        self.link_renderer = ReportLabHyperlinkRenderer()
    def render_smoke_pdf(self, manifest: RenderManifest, output_path: str | Path, smoke_page_numbers: tuple[int, ...] = (1, 3, 22)) -> None:
        selected_pages = [page for page in manifest.pages if page.page_number in set(smoke_page_numbers)]
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        canvas = Canvas(str(output), pagesize=(LETTER_LANDSCAPE.width, LETTER_LANDSCAPE.height))
        for page in selected_pages:
            self.link_renderer.register_page_bookmark(canvas, page)
            self.page_renderers.get(page.template_id).render(canvas, page, manifest)
            smoke_set = set(smoke_page_numbers)
            smoke_links = tuple(link for link in manifest.links if link.target_page in smoke_set)
            self.link_renderer.register_links_for_page(canvas, page.page_number, smoke_links)
            canvas.showPage()
        canvas.save()
