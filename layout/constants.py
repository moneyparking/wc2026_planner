from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PageGeometry:
    width: float
    height: float
    margin_outer: float
    margin_inner: float
    margin_top: float
    margin_bottom: float
    grid: float
    min_touch_target: float
    nav_height: float
    nav_y: float
    content_top: float
    content_bottom: float
    content_left: float
    content_right: float

LETTER_LANDSCAPE = PageGeometry(792.0, 612.0, 24.0, 24.0, 24.0, 24.0, 8.0, 25.0, 48.0, 18.0, 560.0, 82.0, 24.0, 768.0)
COLOR_GEOMETRY_TAGS = {
    "background": "#070A0F",
    "surface": "#101722",
    "surface_alt": "#1A2230",
    "line": "#394457",
    "write_plate": "#181A20",
    "ink": "#F4F7FB",
    "muted_ink": "#AAB3C2",
    "primary": "#A7FF00",
    "secondary": "#FFD166",
    "accent": "#35D6E8",
    "danger": "#FF4D6D",
}
