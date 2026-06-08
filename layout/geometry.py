from __future__ import annotations
from dataclasses import dataclass
from models.specs import Rect

@dataclass(frozen=True, slots=True)
class Box:
    key: str
    rect: Rect
    role: str
    min_touch_required: bool = False
    def validate(self, min_touch_target: float = 25.0) -> None:
        if self.rect.width <= 0 or self.rect.height <= 0:
            raise ValueError(f"Invalid box size for {self.key}: {self.rect}")
        if self.min_touch_required:
            self.rect.validate_min_touch_target(min_touch_target)

def rect_from_xywh(x: float, y: float, width: float, height: float) -> Rect:
    return Rect(x=x, y=y, width=width, height=height)

def rect_to_reportlab_tuple(rect: Rect) -> tuple[float, float, float, float]:
    return (rect.x, rect.y, rect.x + rect.width, rect.y + rect.height)

def split_horizontal(rect: Rect, count: int, gap: float) -> tuple[Rect, ...]:
    if count <= 0:
        raise ValueError("count must be positive")
    cell_width = (rect.width - gap * (count - 1)) / count
    return tuple(Rect(rect.x + index * (cell_width + gap), rect.y, cell_width, rect.height) for index in range(count))
