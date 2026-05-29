from __future__ import annotations
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from layout.constants import LETTER_LANDSCAPE
from layout.layout_validation import validate_manifest_geometry
from models.specs import RenderManifest
from rendering.hyperlink_renderer import ReportLabHyperlinkRenderer
from rendering.renderer_registry import RendererRegistry

class FullSkeletonPDFRenderer:
    def __init__(self) -> None:
        self.page_renderers = RendererRegistry()
        self.link_renderer = ReportLabHyperlinkRenderer()
    def render_skeleton_pdf(self, manifest: RenderManifest, output_path: str | Path) -> None:
        validate_manifest_geometry(manifest)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        canvas = Canvas(str(output), pagesize=(LETTER_LANDSCAPE.width, LETTER_LANDSCAPE.height))
        for page in manifest.pages:
            self.link_renderer.register_page_bookmark(canvas, page)
            self.page_renderers.get(page.template_id).render(canvas, page, manifest)
            self.link_renderer.register_links_for_page(canvas, page.page_number, manifest.links)
            canvas.showPage()
        canvas.save()
