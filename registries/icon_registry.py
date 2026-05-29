from __future__ import annotations

KNOWN_ICON_PREFIXES = ("icons_",)

def validate_icon_filename(filename: str) -> None:
    if not filename.endswith(".png"):
        raise ValueError(f"Icon must be PNG: {filename}")
    if not filename.startswith(KNOWN_ICON_PREFIXES):
        raise ValueError(f"Unexpected icon name: {filename}")
