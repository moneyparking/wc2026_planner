from __future__ import annotations

from models.enums import Scope, SectionId, SKU
from models.specs import IconSpec, RenderManifest, SectionSpec
from product_config import get_sku_config
from registries.component_registry import validate_templates
from registries.hyperlink_registry import build_hyperlink_registry, validate_hyperlink_registry
from registries.page_registry import build_page_registry


def build_section_specs(config) -> tuple[SectionSpec, ...]:
    return tuple(
        SectionSpec(
            SectionId(section.section_id.value),
            section.title,
            section.start_page,
            section.end_page,
            section.count,
            Scope.SHARED_ALL,
        )
        for section in config.sections
    )


def build_icon_specs_from_pages(pages) -> tuple[IconSpec, ...]:
    filenames: set[str] = set()
    for page in pages:
        if page.primary_icon:
            filenames.add(page.primary_icon)
        filenames.update(page.secondary_icons)
    return tuple(
        IconSpec(filename.replace(".png", ""), filename, filename.split("_")[0], Scope.SHARED_ALL, 300, True)
        for filename in sorted(filenames)
    )


def build_render_manifest(active_sku: SKU = SKU.PREMIUM) -> RenderManifest:
    config = get_sku_config(active_sku.value)
    pages = build_page_registry(active_sku)
    sections = build_section_specs(config)
    links = build_hyperlink_registry(pages, active_sku)
    icons = build_icon_specs_from_pages(pages)

    validate_templates({page.template_id for page in pages})
    validate_hyperlink_registry(links, config.total_pages)

    manifest = RenderManifest(
        sku=config.name,
        display_name=config.display_name,
        total_pages=config.total_pages,
        price_usd=config.export.price_usd,
        sections=sections,
        pages=pages,
        links=links,
        icons=icons,
        export_files={
            "hyperlinked_pdf": config.export.pdf_filename,
            "flattened_pdf": config.export.flattened_pdf_filename,
            "buyer_zip": config.export.buyer_zip_filename,
            "sticker_zip": config.export.sticker_zip_filename,
            "quick_start": config.export.quick_start_filename,
        },
        qa_targets={
            "expected_pages": config.qa.expected_pages,
            "max_pdf_mb": config.qa.max_pdf_mb,
            "min_touch_target_px": config.qa.min_touch_target_px,
            "expected_match_logs": config.qa.expected_match_logs,
            "expected_group_trackers": config.qa.expected_group_trackers,
            "expected_bingo_cards": config.qa.expected_bingo_cards,
            "expected_sticker_files": config.qa.expected_sticker_files,
        },
    )
    manifest.validate()
    return manifest


def build_all_manifests() -> dict[SKU, RenderManifest]:
    return {
        SKU.PREMIUM: build_render_manifest(SKU.PREMIUM),
        SKU.STANDARD: build_render_manifest(SKU.STANDARD),
        SKU.MINIMAL: build_render_manifest(SKU.MINIMAL),
    }


if __name__ == "__main__":
    for sku, manifest in build_all_manifests().items():
        print(f"SKU: {manifest.sku}")
        print(f"Pages: {manifest.total_pages}")
        print(f"Page specs: {len(manifest.pages)}")
        print(f"Links: {len(manifest.links)}")
        print(f"Icons: {len(manifest.icons)}")
        print("---")
