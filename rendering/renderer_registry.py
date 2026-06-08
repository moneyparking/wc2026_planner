from __future__ import annotations

from registries.component_registry import TEMPLATE_TO_RENDERER
from rendering.core_pages import CorePageRenderer
from rendering.font_registry import FontRegistry
from rendering.global_components import GlobalComponents
from rendering.icon_loader import IconLoader
from rendering.match_log_pages import MatchLogPageRenderer
from rendering.party_bingo_pages import PartyBingoPageRenderer
from rendering.simple_templates import SimpleTemplateRenderer
from rendering.sticker_notes_pages import StickerNotesPageRenderer
from rendering.team_stats_pages import TeamStatsPageRenderer
from rendering.tournament_pages import TournamentPageRenderer


class CompositePageRenderer:
    def __init__(self, template_id: str, globals_: GlobalComponents) -> None:
        self.template_id = template_id
        self.core_pages = CorePageRenderer(globals_)
        self.tournament_pages = TournamentPageRenderer(globals_)
        self.team_stats_pages = TeamStatsPageRenderer(globals_)
        self.party_bingo_pages = PartyBingoPageRenderer(globals_)
        self.match_log_pages = MatchLogPageRenderer(globals_)
        self.sticker_notes_pages = StickerNotesPageRenderer(globals_)
        self.fallback = SimpleTemplateRenderer(globals_)

    def render(self, canvas, page, manifest) -> None:
        for renderer in (
            self.core_pages,
            self.tournament_pages,
            self.team_stats_pages,
            self.party_bingo_pages,
            self.match_log_pages,
            self.sticker_notes_pages,
        ):
            if renderer.can_render(page):
                renderer.render(canvas, page, manifest)
                return

        self.fallback.render(canvas, page, manifest)


class RendererRegistry:
    def __init__(self) -> None:
        globals_ = GlobalComponents(FontRegistry().register_all(), IconLoader())
        self._renderers = {
            template_id: CompositePageRenderer(template_id, globals_)
            for template_id in TEMPLATE_TO_RENDERER
        }

    def get(self, template_id: str) -> CompositePageRenderer:
        if template_id not in self._renderers:
            raise KeyError(f"No renderer registered for {template_id}")
        return self._renderers[template_id]
