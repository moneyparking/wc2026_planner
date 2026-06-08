from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
from typing import Dict, Literal, Tuple

SkuName = Literal["premium", "standard", "minimal"]
MatchLogType = Literal["dedicated", "condensed"]
PageSizeName = Literal["letter_landscape", "a4_landscape"]

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

@dataclass(frozen=True)
class DesignSystem:
    product_name: str; canvas_size: PageSizeName; background: str; surface: str; surface_alt: str; ink: str; muted_ink: str; primary: str; secondary: str; accent: str; danger: str; line: str; write_plate: str; write_plate_opacity: float; display_font: str; body_font: str; mono_font: str; grid_px: int; page_padding_px: int; min_touch_target_px: int; icon_style: str; icon_size_px: int; icon_stroke_px: int

@dataclass(frozen=True)
class FeatureFlags:
    dedicated_match_logs: bool; condensed_match_logs: bool; group_trackers_12_pages: bool; match_index_3_pages: bool; bracket_prediction: bool; live_knockout_tracker: bool; bingo_cards_count: int; dark_notes_count: int

@dataclass(frozen=True)
class StickerConfig:
    total_target_files: int; png_target_count: int; svg_target_count: int; dpi: int; transparent_background: bool; folders: Tuple[str, ...]; naming_examples: Tuple[str, ...]

@dataclass(frozen=True)
class ExportConfig:
    price_usd: float; sku_label: str; pdf_filename: str; flattened_pdf_filename: str; buyer_zip_filename: str; sticker_zip_filename: str; quick_start_filename: str; include_a4_printable: bool; include_letter_printable: bool; include_bingo_bonus_pdf: bool; include_office_pool_printable: bool; etsy_mockup_count: int

@dataclass(frozen=True)
class PageSection:
    section_id: SectionId; title: str; start_page: int; end_page: int; count: int; enabled: bool = True; notes: str = ""

@dataclass(frozen=True)
class QAConfig:
    expected_pages: int; max_pdf_mb: float; min_touch_target_px: int; require_sticky_nav_all_pages: bool; require_no_blank_pages: bool; require_hyperlinks: bool; require_fonts_embedded: bool; require_dark_write_plates: bool; require_match_index_targets: bool; expected_match_logs: int; expected_group_trackers: int; expected_bingo_cards: int; expected_sticker_files: int

@dataclass(frozen=True)
class SKUConfig:
    name: SkuName; display_name: str; description: str; active: bool; total_pages: int; match_log_type: MatchLogType; match_log_count: int; group_count: int; team_count: int; fixture_count: int; design: DesignSystem; features: FeatureFlags; stickers: StickerConfig; export: ExportConfig; sections: Tuple[PageSection, ...]; qa: QAConfig

DESIGN_SYSTEM = DesignSystem("WC2026 Matchday No Chaos", "letter_landscape", "#070A0F", "#101722", "#1A2230", "#F4F7FB", "#AAB3C2", "#A7FF00", "#FFD166", "#35D6E8", "#FF4D6D", "#394457", "#181A20", 0.90, "Bebas Neue", "Inter", "IBM Plex Mono", 8, 24, 25, "flat_line", 24, 2)
PREMIUM_SECTIONS=(PageSection(SectionId.ONBOARDING,"Onboarding + Bundle Value",1,8,8),PageSection(SectionId.TOURNAMENT_HUB,"Tournament Hub",9,26,18),PageSection(SectionId.TEAM_FAN_IDENTITY,"Team + Fan Identity",27,34,8),PageSection(SectionId.STATS_PREDICTIONS,"Stats + Predictions",35,44,10),PageSection(SectionId.WATCH_PARTY_OFFICE_POOL,"Watch Party + Office Pool",45,58,14),PageSection(SectionId.STICKER_WORKFLOW,"Sticker Workflow + Catalog",59,65,7),PageSection(SectionId.NOTES_MEMORY,"Notes + Memory",66,70,5),PageSection(SectionId.MATCH_LOGS,"Dedicated Match Logs 001-104",71,174,104),PageSection(SectionId.DARK_NOTES,"Dark Notes Pages",175,184,10))
STANDARD_SECTIONS=(PageSection(SectionId.ONBOARDING,"Onboarding + Bundle Value",1,6,6),PageSection(SectionId.TOURNAMENT_HUB,"Tournament Hub",7,23,17),PageSection(SectionId.TEAM_FAN_IDENTITY,"Team + Fan Identity",24,26,3),PageSection(SectionId.STATS_PREDICTIONS,"Stats + Predictions",27,31,5),PageSection(SectionId.WATCH_PARTY_OFFICE_POOL,"Watch Party + Bingo",32,33,2),PageSection(SectionId.STICKER_WORKFLOW,"Sticker Workflow + Catalog",34,36,3),PageSection(SectionId.NOTES_MEMORY,"Notes + Memory",37,38,2),PageSection(SectionId.MATCH_LOGS,"Dedicated Match Logs 001-104",39,142,104),PageSection(SectionId.NOTES_MEMORY,"Extra Notes",143,144,2))
MINIMAL_SECTIONS=(PageSection(SectionId.ONBOARDING,"Onboarding + Core Value",1,4,4),PageSection(SectionId.TOURNAMENT_HUB,"Tournament Hub",5,20,16),PageSection(SectionId.TEAM_FAN_IDENTITY,"Favorite Team Hub",21,21,1),PageSection(SectionId.STATS_PREDICTIONS,"Basic Stats + Predictions",22,23,2),PageSection(SectionId.NOTES_MEMORY,"Final Recap",24,24,1),PageSection(SectionId.MATCH_LOGS,"Condensed Match Logs 001-104",25,76,52),PageSection(SectionId.NOTES_MEMORY,"Notes + Support",77,84,8))

def _stickers(total:int,png:int,svg:int,folders:Tuple[str,...])->StickerConfig:
    return StickerConfig(total,png,svg,300,True,folders,("flags_mexico_001.png","jerseys_usa_001.png","events_goal_001.png","events_var_001.png"))

SKU_CONFIGS: Dict[SkuName, SKUConfig] = {
"premium": SKUConfig("premium","WC2026 Matchday No Chaos Ultimate Fan Command Center","184-page premium GoodNotes fan command center with 104 dedicated match logs, office pool kit, bingo, expanded stats and 500-file sticker bundle.",True,184,"dedicated",104,12,48,104,DESIGN_SYSTEM,FeatureFlags(True,False,True,True,True,True,8,10),_stickers(500,250,250,("flags","jerseys","icons","events","bingo","tactics")),ExportConfig(27.99,"Premium","01_WC2026_Matchday_No_Chaos_Premium_GoodNotes_Hyperlinked.pdf","02_WC2026_Matchday_No_Chaos_Premium_Flattened_Compatibility.pdf","WC2026_Matchday_No_Chaos_Premium_Buyer_Pack.zip","04_WC2026_Matchday_No_Chaos_Premium_Sticker_Pack_300DPI_PNG_SVG.zip","05_WC2026_Matchday_No_Chaos_Premium_Quick_Start_Guide.pdf",True,True,True,True,12),PREMIUM_SECTIONS,QAConfig(184,20.0,25,True,True,True,True,True,True,104,12,8,500)),
"standard": SKUConfig("standard","WC2026 Matchday No Chaos Standard Planner","144-page standard GoodNotes planner with 104 dedicated match logs, group trackers, basic stats, 4 bingo cards and 180-file sticker bundle.",False,144,"dedicated",104,12,48,104,DESIGN_SYSTEM,FeatureFlags(True,False,True,True,True,True,4,2),_stickers(180,90,90,("flags","jerseys","icons","events","bingo")),ExportConfig(17.99,"Standard","01_WC2026_Matchday_No_Chaos_Standard_GoodNotes_Hyperlinked.pdf","02_WC2026_Matchday_No_Chaos_Standard_Flattened_Compatibility.pdf","WC2026_Matchday_No_Chaos_Standard_Buyer_Pack.zip","04_WC2026_Matchday_No_Chaos_Standard_Sticker_Pack_300DPI_PNG_SVG.zip","05_WC2026_Matchday_No_Chaos_Standard_Quick_Start_Guide.pdf",False,True,True,False,10),STANDARD_SECTIONS,QAConfig(144,20.0,25,True,True,True,True,True,True,104,12,4,180)),
"minimal": SKUConfig("minimal","WC2026 Matchday No Chaos Minimal Tracker","84-page entry GoodNotes tracker with group tables, bracket, condensed two-match logs, basic predictions and sample sticker set.",False,84,"condensed",52,12,48,104,DESIGN_SYSTEM,FeatureFlags(False,True,True,False,True,True,0,6),_stickers(24,24,0,("sample",)),ExportConfig(9.99,"Minimal","01_WC2026_Matchday_No_Chaos_Minimal_GoodNotes_Hyperlinked.pdf","02_WC2026_Matchday_No_Chaos_Minimal_Flattened_Compatibility.pdf","WC2026_Matchday_No_Chaos_Minimal_Buyer_Pack.zip","04_WC2026_Matchday_No_Chaos_Minimal_Sample_Sticker_Pack_300DPI_PNG.zip","05_WC2026_Matchday_No_Chaos_Minimal_Quick_Start_Guide.pdf",False,True,False,False,8),MINIMAL_SECTIONS,QAConfig(84,20.0,25,True,True,True,True,True,True,52,12,0,24)),
}

REPO_ROOT = Path(__file__).resolve().parent

APP_TITLE = "AI Bracket War Room 2026 - Build Small Hackathon"

SPREADSHEET_CANDIDATE_PATHS = (
    REPO_ROOT / "releases" / "final" / "artifacts" / "03_AI_Bracket_War_Room_2026_Spreadsheet_Engine.xlsx",
    REPO_ROOT / "FIX6C_STATIC_ANNEXC_HACKATHON_READY.xlsx",
    REPO_ROOT / "assets" / "AI_Bracket_War_Room_2026_Planner_FIX7.xlsx",
)

SHEET_START_HERE = "START_HERE"
SHEET_BRACKET_WAR_ROOM = "BRACKET_WAR_ROOM"
SHEET_MATCH_PLANNER = "MATCH_PLANNER"
SHEET_FRIENDS_LEAGUE = "FRIENDS_LEAGUE"
SHEET_ANNEX_C = "AnnexC_495_STATIC"
SHEET_QA_STATIC_CHECK = "QA_STATIC_CHECK"

CANONICAL_SHEETS = (
    SHEET_START_HERE,
    SHEET_BRACKET_WAR_ROOM,
    SHEET_MATCH_PLANNER,
    SHEET_FRIENDS_LEAGUE,
    SHEET_ANNEX_C,
    SHEET_QA_STATIC_CHECK,
)

REQUIRED_SHEETS = (
    SHEET_MATCH_PLANNER,
    SHEET_FRIENDS_LEAGUE,
    SHEET_ANNEX_C,
)

OPTIONAL_SHEETS = (
    SHEET_START_HERE,
    SHEET_BRACKET_WAR_ROOM,
    SHEET_QA_STATIC_CHECK,
)

MATCH_COLUMNS = (
    "Match ID",
    "Phase",
    "Side A",
    "Side B",
    "Prediction",
    "AI Signal",
    "Confidence %",
    "Watch Priority",
    "Notes",
    "Result",
    "Points",
)

FRIENDS_COLUMNS = (
    "Player",
    "Role",
    "Correct Scores",
    "Correct Winners",
    "Upsets Hit",
    "Total Points",
    "Status",
)

SCORING_EXACT_SCORE_POINTS = 5
SCORING_CORRECT_OUTCOME_POINTS = 2
SCORING_MISS_POINTS = 0
SCORING_EMPTY_RESULT_POINTS = 0

EXPECTED_MATCH_COUNT = 104
EXPECTED_GROUP_COUNT = 12
EXPECTED_ANNEX_C_RECORD_COUNT = 495

def get_sku_config(sku: SkuName) -> SKUConfig:
    if sku not in SKU_CONFIGS: raise KeyError(f"Unknown SKU: {sku}")
    return SKU_CONFIGS[sku]

def validate_section_page_counts(config: SKUConfig)->None:
    covered=[]
    for section in config.sections:
        if section.end_page-section.start_page+1 != section.count: raise ValueError(f"{config.name}: section count mismatch for {section.title}")
        covered.extend(range(section.start_page,section.end_page+1))
    if sorted(set(covered)) != list(range(1,config.total_pages+1)): raise ValueError(f"{config.name}: page coverage mismatch")

def validate_sku_config(config: SKUConfig)->None:
    validate_section_page_counts(config)
    if config.total_pages != config.qa.expected_pages: raise ValueError(f"{config.name}: total_pages mismatch")
    if config.design.min_touch_target_px < 25: raise ValueError(f"{config.name}: touch target too small")

def validate_all_configs()->None:
    for cfg in SKU_CONFIGS.values(): validate_sku_config(cfg)

if __name__ == "__main__":
    validate_all_configs()
    for sku,cfg in SKU_CONFIGS.items(): print(f"{sku}: {cfg.total_pages} pages, {cfg.match_log_type} logs, ${cfg.export.price_usd}")
