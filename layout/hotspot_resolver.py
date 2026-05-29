from __future__ import annotations
from models.specs import LinkSpec, Rect
from layout.component_boxes import all_component_boxes

class HotspotResolver:
    def __init__(self) -> None:
        self._boxes = all_component_boxes()
    def resolve(self, link: LinkSpec) -> Rect:
        key = link.hotspot_key
        if key.startswith("match_index.row."):
            match_id = int(key.split(".")[-1])
            slot = match_id if match_id <= 36 else match_id - 36 if match_id <= 72 else match_id - 72
            return self._boxes[f"match_index.row_slot.{slot:02d}"].rect
        if key.startswith("group.fixture."):
            match_id = int(key.split(".")[-1])
            row = ((match_id - 1) % 6) + 1
            return self._boxes[f"group.fixture.row.{row:02d}"].rect
        if key not in self._boxes:
            raise KeyError(f"No hotspot geometry for key: {key}")
        return self._boxes[key].rect
