from __future__ import annotations
from models.specs import Rect
from layout.constants import LETTER_LANDSCAPE
from layout.geometry import Box, rect_from_xywh, split_horizontal


def global_boxes() -> dict[str, Box]:
    g = LETTER_LANDSCAPE
    return {
        "page.content": Box("page.content", Rect(g.content_left, g.content_bottom, g.content_right - g.content_left, g.content_top - g.content_bottom), "content_area"),
        "page.header": Box("page.header", rect_from_xywh(24, 552, 744, 36), "top_context_bar"),
        "page.nav": Box("page.nav", rect_from_xywh(24, g.nav_y, 744, g.nav_height), "sticky_navigation"),
        "cta.primary": Box("cta.primary", rect_from_xywh(296, 116, 200, 44), "primary_cta", True),
    }


def nav_boxes() -> dict[str, Box]:
    nav_rect = global_boxes()["page.nav"].rect
    cells = split_horizontal(nav_rect, count=9, gap=6.0)
    nav_ids = ("home", "teams", "groups", "match", "bracket", "stats", "party", "stickers", "notes")
    return {f"nav.{nav_id}": Box(f"nav.{nav_id}", cell, "sticky_nav_button", True) for nav_id, cell in zip(nav_ids, cells)}


def all_component_boxes() -> dict[str, Box]:
    boxes: dict[str, Box] = {}
    boxes.update(global_boxes())
    boxes.update(nav_boxes())
    boxes.update({
        "bundle.card.quick_start": Box("bundle.card.quick_start", rect_from_xywh(48, 390, 220, 96), "bundle_card", True),
        "bundle.card.stickers": Box("bundle.card.stickers", rect_from_xywh(286, 390, 220, 96), "bundle_card", True),
        "bundle.card.bingo": Box("bundle.card.bingo", rect_from_xywh(524, 390, 220, 96), "bundle_card", True),
        "dashboard.card.groups": Box("dashboard.card.groups", rect_from_xywh(48, 350, 160, 88), "dashboard_card", True),
        "dashboard.card.match_logs": Box("dashboard.card.match_logs", rect_from_xywh(224, 350, 160, 88), "dashboard_card", True),
        "dashboard.card.bracket": Box("dashboard.card.bracket", rect_from_xywh(400, 350, 160, 88), "dashboard_card", True),
        "dashboard.card.party": Box("dashboard.card.party", rect_from_xywh(576, 350, 160, 88), "dashboard_card", True),
        "match_log.back_to_index": Box("match_log.back_to_index", rect_from_xywh(588, 524, 148, 30), "back_link", True),
    })
    for row in range(1, 7):
        boxes[f"group.fixture.row.{row:02d}"] = Box(f"group.fixture.row.{row:02d}", rect_from_xywh(508, 362 - (row - 1) * 38, 228, 32), "group_fixture_link", True)
    for row in range(1, 37):
        boxes[f"match_index.row_slot.{row:02d}"] = Box(f"match_index.row_slot.{row:02d}", rect_from_xywh(56, 92 + (36 - row) * 12.8, 680, 25.5), "match_index_full_row_link", True)
    return boxes


def match_log_boxes() -> dict[str, Box]:
    boxes = all_component_boxes()
    boxes.update({
        "match_log.score_box": Box("match_log.score_box", rect_from_xywh(48, 382, 260, 76), "score_box"),
        "match_log.prediction": Box("match_log.prediction", rect_from_xywh(48, 264, 260, 94), "prediction"),
        "match_log.pitch": Box("match_log.pitch", rect_from_xywh(332, 264, 244, 194), "pitch"),
        "match_log.timeline": Box("match_log.timeline", rect_from_xywh(48, 156, 688, 78), "timeline"),
        "match_log.recap": Box("match_log.recap", rect_from_xywh(48, 92, 688, 42), "recap"),
    })
    return {key: boxes[key] for key in boxes if key.startswith("match_log.")}
