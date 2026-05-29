from __future__ import annotations

from models.enums import Scope, SectionId
from models.specs import PageSpec
from registries.page_registry import build_premium_page_registry


def _clone_page(
    source: PageSpec,
    page_number: int,
    page_id: str | None = None,
    title: str | None = None,
    subtitle: str | None = None,
    template_id: str | None = None,
    section_id: SectionId | None = None,
    scope: Scope | None = None,
    primary_icon: str | None = None,
    secondary_icons: tuple[str, ...] | None = None,
    data_ref: str | None = None,
    qa_tags: tuple[str, ...] | None = None,
) -> PageSpec:
    return PageSpec(
        page_number=page_number,
        page_id=page_id or source.page_id,
        title=title or source.title,
        subtitle=subtitle or source.subtitle,
        section_id=section_id or source.section_id,
        template_id=template_id or source.template_id,
        scope=scope or source.scope,
        primary_icon=primary_icon if primary_icon is not None else source.primary_icon,
        secondary_icons=secondary_icons if secondary_icons is not None else source.secondary_icons,
        links=tuple(),
        data_ref=data_ref if data_ref is not None else source.data_ref,
        qa_tags=qa_tags if qa_tags is not None else source.qa_tags,
        metadata=dict(source.metadata),
    )


def _premium_by_number() -> dict[int, PageSpec]:
    return {page.page_number: page for page in build_premium_page_registry()}


def _match_log_page(
    page_number: int,
    match_id: int,
    condensed_pair: tuple[int, int] | None = None,
) -> PageSpec:
    if condensed_pair:
        first, second = condensed_pair
        return PageSpec(
            page_number=page_number,
            page_id=f"condensed_match_log_{first:03d}_{second:03d}",
            title=f"Matches {first:03d}–{second:03d}",
            subtitle="Two-match condensed score, pick and recap tracker",
            section_id=SectionId.MATCH_LOGS,
            template_id="dedicated_match_log",
            scope=Scope.DERIVED_CONDENSED,
            primary_icon="icons_match_001.png",
            secondary_icons=("icons_goal_001.png", "icons_var_001.png", "icons_card_001.png"),
            links=tuple(),
            data_ref=f"fixtures.match_{first:03d}_{second:03d}",
            qa_tags=("match_log", "condensed_match_log", "sticky_nav", "dark_write_plate"),
        )

    return PageSpec(
        page_number=page_number,
        page_id=f"match_log_{match_id:03d}",
        title=f"Match {match_id:03d}",
        subtitle="Score, prediction, tactics, event timeline and recap",
        section_id=SectionId.MATCH_LOGS,
        template_id="dedicated_match_log",
        scope=Scope.SHARED_PREMIUM_STANDARD,
        primary_icon="icons_match_001.png",
        secondary_icons=("icons_goal_001.png", "icons_var_001.png", "icons_card_001.png", "icons_save_001.png"),
        links=tuple(),
        data_ref=f"fixtures.match_{match_id:03d}",
        qa_tags=("match_log", "dedicated_match_log", "sticky_nav", "dark_write_plate"),
    )


def _standard_static_pages() -> list[PageSpec]:
    premium = _premium_by_number()
    pages: list[PageSpec] = []

    mappings = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 9),
    )
    for target, source in mappings:
        pages.append(_clone_page(premium[source], target))

    for group_index, source_page in enumerate(range(10, 22), start=8):
        pages.append(_clone_page(premium[source_page], group_index))

    pages.extend(
        (
            _clone_page(premium[22], 20),
            _clone_page(premium[23], 21),
            _clone_page(premium[25], 22),
            _clone_page(premium[26], 23),
            _clone_page(premium[27], 24),
            _clone_page(premium[28], 25),
            _clone_page(premium[29], 26),
            _clone_page(premium[35], 27),
            _clone_page(premium[36], 28),
            _clone_page(premium[37], 29),
            _clone_page(premium[38], 30),
            _clone_page(premium[39], 31),
            _clone_page(premium[45], 32),
            _clone_page(premium[51], 33, page_id="standard_bingo_card_01", title="Bingo Card 1"),
            _clone_page(premium[59], 34),
            _clone_page(premium[60], 35),
            _clone_page(premium[61], 36),
            _clone_page(premium[68], 37),
            _clone_page(premium[70], 38),
        )
    )
    return pages


def _minimal_static_pages() -> list[PageSpec]:
    premium = _premium_by_number()
    pages: list[PageSpec] = []

    mappings = (
        (1, 1),
        (2, 4),
        (3, 5),
        (4, 3),
    )
    for target, source in mappings:
        pages.append(_clone_page(premium[source], target))

    for group_index, source_page in enumerate(range(10, 22), start=5):
        pages.append(_clone_page(premium[source_page], group_index))

    pages.extend(
        (
            _clone_page(premium[22], 17),
            _clone_page(premium[23], 18),
            _clone_page(premium[25], 19),
            _clone_page(premium[26], 20),
            _clone_page(premium[27], 21),
            _clone_page(premium[35], 22),
            _clone_page(premium[38], 23),
            _clone_page(premium[68], 24),
        )
    )
    return pages


def build_standard_page_registry() -> tuple[PageSpec, ...]:
    pages = _standard_static_pages()

    for match_id in range(1, 105):
        pages.append(_match_log_page(page_number=38 + match_id, match_id=match_id))

    pages.extend(
        (
            PageSpec(
                143,
                "standard_notes_01",
                "Standard Notes 1",
                "Extra tournament notes and watch reminders",
                SectionId.NOTES_MEMORY,
                "dark_notes",
                Scope.STANDARD_ONLY,
                "icons_notes_001.png",
                ("icons_pen_001.png",),
                tuple(),
                None,
                ("notes", "sticky_nav", "dark_write_plate"),
            ),
            PageSpec(
                144,
                "standard_notes_02",
                "Standard Notes 2",
                "Extra bracket, team and party notes",
                SectionId.NOTES_MEMORY,
                "dark_notes",
                Scope.STANDARD_ONLY,
                "icons_notes_001.png",
                ("icons_pen_001.png",),
                tuple(),
                None,
                ("notes", "sticky_nav", "dark_write_plate"),
            ),
        )
    )

    return tuple(sorted(pages, key=lambda page: page.page_number))


def build_minimal_page_registry() -> tuple[PageSpec, ...]:
    pages = _minimal_static_pages()
    page_number = 25

    for first_match in range(1, 105, 2):
        second_match = first_match + 1
        pages.append(_match_log_page(page_number=page_number, match_id=first_match, condensed_pair=(first_match, second_match)))
        page_number += 1

    for note_number in range(77, 85):
        pages.append(
            PageSpec(
                page_number=note_number,
                page_id=f"minimal_notes_{note_number - 76:02d}",
                title=f"Minimal Notes {note_number - 76}",
                subtitle="Compact tournament writing page",
                section_id=SectionId.NOTES_MEMORY,
                template_id="dark_notes",
                scope=Scope.MINIMAL_ONLY,
                primary_icon="icons_notes_001.png",
                secondary_icons=("icons_pen_001.png",),
                links=tuple(),
                data_ref=None,
                qa_tags=("notes", "sticky_nav", "dark_write_plate"),
            )
        )

    return tuple(sorted(pages, key=lambda page: page.page_number))


def validate_derived_page_registry(pages: tuple[PageSpec, ...], expected_pages: int) -> None:
    numbers = [page.page_number for page in pages]
    if numbers != list(range(1, expected_pages + 1)):
        raise AssertionError(f"Derived page registry is not contiguous: expected={expected_pages}, actual={len(numbers)}")

    page_ids = [page.page_id for page in pages]
    if len(set(page_ids)) != expected_pages:
        duplicates = sorted({page_id for page_id in page_ids if page_ids.count(page_id) > 1})
        raise AssertionError(f"Derived registry contains duplicate page_id values: {duplicates}")
