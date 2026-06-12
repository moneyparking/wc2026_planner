from __future__ import annotations

import json
import re
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.wc2026_data_loader import load_fixtures, load_groups, load_squads, validate_wc2026_dataset


DATA_FILES = [
    "data/wc2026_groups.csv",
    "data/wc2026_fixtures.csv",
    "data/wc2026_squads.csv",
    "data/wc2026_team_metadata.csv",
    "data/wc2026_data_manifest.json",
]
FORBIDDEN_TERMS = ["odds", "betting", "wager", "sportsbook", "parlay", "payout"]
SCAN_FILES = ["app.py", "README.md", "releases/final/HACKATHON_SUBMISSION_PHASE_1_29.md"]
SPECIAL_NAMES = ["Côte d'Ivoire", "Türkiye", "Curaçao", "IR Iran", "Korea Republic", "Bosnia & Herzegovina", "DR Congo"]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    for relative in DATA_FILES:
        path = REPO_ROOT / relative
        if not path.exists():
            fail(f"Missing required file: {relative}")
        if path.stat().st_size < 100:
            fail(f"File size too small for real data: {relative}")

    manifest = json.loads((REPO_ROOT / "data/wc2026_data_manifest.json").read_text(encoding="utf-8"))
    for key in ["official_fixtures", "official_teams", "official_squads", "fixture_crosscheck"]:
        if not str(manifest.get("sources", {}).get(key, "")).startswith("http"):
            fail(f"Manifest source URL missing: {key}")

    validation = validate_wc2026_dataset()
    if validation["errors"]:
        fail(" | ".join(validation["errors"]))
    if validation["groups_count"] != 12:
        fail("Groups count must be 12.")
    if validation["teams_count"] != 48:
        fail("Team count must be 48.")
    if validation["fixtures_count"] != 104:
        fail("Fixtures count must be 104.")
    if validation["group_stage_count"] != 72:
        fail("Group-stage count must be 72.")
    if validation["knockout_count"] != 32:
        fail("Knockout count must be 32.")

    groups = load_groups()
    fixtures = load_fixtures()
    squads = load_squads()
    if groups.groupby("group")["team"].count().ne(4).any():
        fail("Each group must have exactly four teams.")
    if sorted(fixtures["match_no"].astype(int).tolist()) != list(range(1, 105)):
        fail("Match numbers must be exactly 1-104.")
    if not fixtures[fixtures["match_no"].astype(int).le(72)]["team_data_status"].eq("known_teams").all():
        fail("Group-stage matches must use known teams.")
    if fixtures[["home", "away", "date"]].eq("").any().any():
        fail("Fixtures must not contain blank home, away, or date fields.")
    if len(squads) != 1248:
        fail(f"Squad parser warning: {len(squads)} / 1248 player rows parsed.")

    combined_data = "\n".join(path.read_text(encoding="utf-8-sig") for path in (REPO_ROOT / "data").glob("wc2026_*.csv"))
    for name in SPECIAL_NAMES:
        if name not in combined_data:
            fail(f"Special-character team name not preserved: {name}")

    for relative in SCAN_FILES:
        path = REPO_ROOT / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for term in FORBIDDEN_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", text):
                fail(f"Forbidden term '{term}' found in {relative}")

    print("PHASE_1_29_REAL_DATA_QA_PASS")
    print(f"groups={validation['groups_count']}")
    print(f"teams={validation['teams_count']}")
    print(f"fixtures={validation['fixtures_count']}")
    print(f"squad_rows={validation['squad_rows_count']}")


if __name__ == "__main__":
    main()
