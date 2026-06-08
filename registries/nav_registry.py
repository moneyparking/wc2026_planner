from __future__ import annotations
from dataclasses import dataclass
from models.enums import SKU

@dataclass(frozen=True, slots=True)
class NavTarget:
    nav_id: str
    label: str
    premium_target: int
    standard_target: int
    minimal_target: int
    required_all_sku: bool = True
    def target_for(self, sku: SKU) -> int:
        if sku == SKU.PREMIUM:
            return self.premium_target
        if sku == SKU.STANDARD:
            return self.standard_target
        if sku == SKU.MINIMAL:
            return self.minimal_target
        raise ValueError(f"Unsupported SKU: {sku}")

CANONICAL_NAV: tuple[NavTarget, ...] = (
    NavTarget("home", "HOME", 3, 3, 4),
    NavTarget("teams", "TEAMS", 27, 24, 21),
    NavTarget("groups", "GROUPS", 10, 7, 5),
    NavTarget("match", "MATCH", 22, 19, 17),
    NavTarget("bracket", "BRACKET", 25, 22, 19),
    NavTarget("stats", "STATS", 35, 27, 22),
    NavTarget("party", "PARTY", 45, 32, 24),
    NavTarget("stickers", "STICKERS", 59, 34, 8),
    NavTarget("notes", "NOTES", 66, 37, 77),
)

def get_nav_targets(sku: SKU) -> dict[str, int]:
    return {item.nav_id: item.target_for(sku) for item in CANONICAL_NAV}

def get_nav_labels() -> tuple[str, ...]:
    return tuple(item.label for item in CANONICAL_NAV)

def validate_nav() -> None:
    if len(CANONICAL_NAV) != 9:
        raise ValueError("Canonical nav must contain exactly 9 buttons")
    ids = [item.nav_id for item in CANONICAL_NAV]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate nav_id in canonical nav")
