from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
from models.enums import HotspotKind, LinkType, Scope, SectionId

@dataclass(frozen=True, slots=True)
class Rect:
    x: float
    y: float
    width: float
    height: float
    def validate_min_touch_target(self, min_size: float = 25.0) -> None:
        if self.width < min_size or self.height < min_size:
            raise ValueError("Touch target too small")

@dataclass(frozen=True, slots=True)
class SectionSpec:
    section_id: SectionId
    title: str
    start_page: int
    end_page: int
    count: int
    scope: Scope
    def validate(self) -> None:
        if self.end_page - self.start_page + 1 != self.count:
            raise ValueError("Section count mismatch")

@dataclass(frozen=True, slots=True)
class IconSpec:
    icon_id: str
    filename: str
    category: str
    scope: Scope
    dpi: int = 300
    transparent: bool = True
    display_width: float = 24.0
    display_height: float = 24.0
    def validate(self) -> None:
        if not self.filename.endswith(".png"):
            raise ValueError("Icon must be PNG")
        if self.dpi < 300:
            raise ValueError("Icon DPI too low")

@dataclass(frozen=True, slots=True)
class LinkSpec:
    link_id: str
    label: str
    link_type: LinkType
    source_page: int
    target_page: Optional[int]
    target_anchor: Optional[str]
    hotspot_key: str
    required: bool = True
    hotspot_kind: HotspotKind = HotspotKind.SEMANTIC
    rect: Optional[Rect] = None
    def validate(self, page_count: int) -> None:
        if not 1 <= self.source_page <= page_count:
            raise ValueError("Invalid source page")
        if self.link_type in {LinkType.INTERNAL_PAGE, LinkType.INTERNAL_ANCHOR}:
            if self.target_page is None or not 1 <= self.target_page <= page_count:
                raise ValueError("Invalid target page")
        if self.hotspot_kind == HotspotKind.ABSOLUTE_RECT:
            if self.rect is None:
                raise ValueError("Absolute hotspot missing rect")
            self.rect.validate_min_touch_target()

@dataclass(frozen=True, slots=True)
class PageSpec:
    page_number: int
    page_id: str
    title: str
    subtitle: str
    section_id: SectionId
    template_id: str
    scope: Scope
    primary_icon: Optional[str]
    secondary_icons: tuple[str, ...] = field(default_factory=tuple)
    links: tuple[LinkSpec, ...] = field(default_factory=tuple)
    data_ref: Optional[str] = None
    qa_tags: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    def validate(self, page_count: int) -> None:
        if not 1 <= self.page_number <= page_count:
            raise ValueError("Invalid page number")
        if not self.page_id or not self.title or not self.template_id:
            raise ValueError("Invalid page spec")
        for link in self.links:
            link.validate(page_count)

@dataclass(frozen=True, slots=True)
class RenderManifest:
    sku: str
    display_name: str
    total_pages: int
    price_usd: float
    sections: tuple[SectionSpec, ...]
    pages: tuple[PageSpec, ...]
    links: tuple[LinkSpec, ...]
    icons: tuple[IconSpec, ...]
    export_files: dict[str, str]
    qa_targets: dict[str, Any]
    def validate(self) -> None:
        if len(self.pages) != self.total_pages:
            raise ValueError("Manifest page count mismatch")
        if [p.page_number for p in self.pages] != list(range(1, self.total_pages + 1)):
            raise ValueError("Manifest pages are not contiguous or sorted")
        for section in self.sections:
            section.validate()
        for page in self.pages:
            page.validate(self.total_pages)
        for link in self.links:
            link.validate(self.total_pages)
        for icon in self.icons:
            icon.validate()
