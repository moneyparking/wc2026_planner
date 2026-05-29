from __future__ import annotations
from models.enums import LinkType, SKU
from models.specs import LinkSpec, PageSpec
from registries.nav_registry import CANONICAL_NAV


def build_sticky_nav_links_for_page(page_number: int, sku: SKU) -> tuple[LinkSpec, ...]:
    return tuple(LinkSpec(f"page_{page_number:03d}.nav.{nav_item.nav_id}", nav_item.label, LinkType.INTERNAL_PAGE, page_number, nav_item.target_for(sku), None, f"nav.{nav_item.nav_id}", True) for nav_item in CANONICAL_NAV)


def collect_declared_page_links(pages: tuple[PageSpec, ...]) -> tuple[LinkSpec, ...]:
    links: list[LinkSpec] = []
    for page in pages:
        links.extend(page.links)
    return tuple(links)


def build_hyperlink_registry(pages: tuple[PageSpec, ...], sku: SKU) -> tuple[LinkSpec, ...]:
    links = list(collect_declared_page_links(pages))
    for page in pages:
        links.extend(build_sticky_nav_links_for_page(page.page_number, sku))
    unique: dict[str, LinkSpec] = {}
    for link in links:
        if link.link_id in unique:
            raise ValueError(f"Duplicate link_id: {link.link_id}")
        unique[link.link_id] = link
    return tuple(unique.values())


def validate_hyperlink_registry(links: tuple[LinkSpec, ...], page_count: int) -> None:
    for link in links:
        link.validate(page_count)
