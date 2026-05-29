from __future__ import annotations
from registries.component_registry import TEMPLATE_TO_RENDERER
from rendering.font_registry import FontRegistry
from rendering.global_components import GlobalComponents
from rendering.icon_loader import IconLoader
from rendering.simple_templates import SimpleTemplateRenderer

class RendererRegistry:
    def __init__(self) -> None:
        globals_ = GlobalComponents(FontRegistry().register_all(), IconLoader())
        self._renderers = {template_id: SimpleTemplateRenderer(globals_) for template_id in TEMPLATE_TO_RENDERER}
    def get(self, template_id: str) -> SimpleTemplateRenderer:
        if template_id not in self._renderers:
            raise KeyError(f"No renderer registered for {template_id}")
        return self._renderers[template_id]
