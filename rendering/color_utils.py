from __future__ import annotations
from reportlab.lib.colors import Color, HexColor


def hex_color(value: str) -> Color:
    if not value.startswith("#") or len(value) != 7:
        raise ValueError(f"Invalid hex color: {value}")
    return HexColor(value)


def alpha_color(hex_value: str, alpha: float) -> Color:
    if alpha < 0 or alpha > 1:
        raise ValueError(f"Invalid alpha value: {alpha}")
    base = HexColor(hex_value)
    return Color(base.red, base.green, base.blue, alpha=alpha)
