from __future__ import annotations
from enum import Enum

class SKU(str, Enum):
    PREMIUM = "premium"
    STANDARD = "standard"
    MINIMAL = "minimal"

class Scope(str, Enum):
    SHARED_ALL = "shared_all"
    SHARED_PREMIUM_STANDARD = "shared_premium_standard"
    PREMIUM_ONLY = "premium_only"
    STANDARD_ONLY = "standard_only"
    MINIMAL_ONLY = "minimal_only"
    DERIVED_CONDENSED = "derived_condensed"

class SectionId(str, Enum):
    ONBOARDING = "onboarding"
    TOURNAMENT_HUB = "tournament_hub"
    TEAM_FAN_IDENTITY = "team_fan_identity"
    STATS_PREDICTIONS = "stats_predictions"
    WATCH_PARTY_OFFICE_POOL = "watch_party_office_pool"
    STICKER_WORKFLOW = "sticker_workflow"
    NOTES_MEMORY = "notes_memory"
    MATCH_LOGS = "match_logs"
    DARK_NOTES = "dark_notes"

class LinkType(str, Enum):
    INTERNAL_PAGE = "internal_page"
    INTERNAL_ANCHOR = "internal_anchor"
    EXTERNAL_URL = "external_url"

class HotspotKind(str, Enum):
    SEMANTIC = "semantic"
    ABSOLUTE_RECT = "absolute_rect"
