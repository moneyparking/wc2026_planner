from __future__ import annotations
from registries.component_registry import TEMPLATE_TO_RENDERER
from rendering.font_registry import FontRegistry
from rendering.global_components import GlobalComponents
from rendering.icon_loader import IconLoader
from rendering.simple_templates import SimpleTemplateRenderer
from rendering.sticker_notes_pages import StickerNotesPageRenderer

class CompositePageRenderer:
    def __init__(self, template_id: str, globals_: GlobalComponents) -> None:
        self.template_id = template_id
        self.sticker_notes_pages = StickerNotesPageRenderer(globals_)
        self.fallback = SimpleTemplateRenderer(globals_)
    def render(self, canvas, page, manifest) -> None:
        if self.sticker_notes_pages.can_render(page):
            self.sticker_notes_pages.render(canvas, page, manifest)
            return
        self.fallback.render(canvas, page, manifest)

class RendererRegistry:
    def __init__(self) -> None:
        globals_ = GlobalComponents(FontRegistry().register_all(), IconLoader())
        self._renderers = {template_id: CompositePageRenderer(template_id, globals_) for template_id in TEMPLATE_TO_RENDERER}
    def get(self, template_id: str) -> CompositePageRenderer:
        if template_id not in self._renderers:
            raise KeyError(f"No renderer registered for {template_id}")
        return self._renderers[template_id]
