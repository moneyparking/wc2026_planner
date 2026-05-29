from __future__ import annotations
from layout.component_boxes import nav_boxes
from layout.constants import LETTER_LANDSCAPE
from rendering.font_registry import FontRegistry


def assert_nav_geometry_valid() -> None:
    boxes = nav_boxes()
    if len(boxes) != 9:
        raise AssertionError("Expected 9 nav boxes")
    for box in boxes.values():
        box.validate(LETTER_LANDSCAPE.min_touch_target)


def assert_font_registry_resolves() -> None:
    font_map = FontRegistry().register_all()
    required = {"display", "body", "body_bold", "mono"}
    if set(font_map) != required:
        raise AssertionError("Font map keys mismatch")


def run_global_component_checks() -> None:
    assert_nav_geometry_valid()
    assert_font_registry_resolves()
