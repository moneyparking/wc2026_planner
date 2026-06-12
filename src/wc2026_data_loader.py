from __future__ import annotations

from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"

GROUP_COLUMNS = ["group", "seed", "team", "team_code", "confederation", "flag_emoji", "source_status"]
FIXTURE_COLUMNS = [
    "match_no",
    "stage",
    "group",
    "date",
    "kickoff_local",
    "kickoff_uk",
    "kickoff_utc",
    "home",
    "away",
    "home_code",
    "away_code",
    "city",
    "country",
    "stadium",
    "team_data_status",
    "source_status",
    "bracket_slot_note",
]
SQUAD_COLUMNS = [
    "team",
    "team_code",
    "shirt_no",
    "position",
    "player_name",
    "first_names",
    "last_names",
    "name_on_shirt",
    "dob",
    "club",
    "height_cm",
    "caps",
    "goals",
    "source_status",
    "parser_confidence",
]
METADATA_COLUMNS = ["team", "team_code", "group", "seed", "coach", "ranking_note", "style_note", "key_players_note", "source_status"]


def _load_csv(filename: str, required_columns: list[str]) -> pd.DataFrame:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing WC2026 data file: {path}")
    frame = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    missing = [column for column in required_columns if column not in frame.columns]
    if missing:
        raise ValueError(f"{filename} missing required columns: {', '.join(missing)}")
    return frame.loc[:, required_columns].copy()


def load_groups() -> pd.DataFrame:
    return _load_csv("wc2026_groups.csv", GROUP_COLUMNS)


def load_fixtures() -> pd.DataFrame:
    fixtures = _load_csv("wc2026_fixtures.csv", FIXTURE_COLUMNS)
    fixtures["match_no"] = pd.to_numeric(fixtures["match_no"], errors="coerce").astype("Int64")
    return fixtures


def load_squads() -> pd.DataFrame:
    return _load_csv("wc2026_squads.csv", SQUAD_COLUMNS)


def load_team_metadata() -> pd.DataFrame:
    return _load_csv("wc2026_team_metadata.csv", METADATA_COLUMNS)


def fixtures_as_match_planner() -> pd.DataFrame:
    fixtures = load_fixtures()
    planner = pd.DataFrame(
        {
            "Match ID": fixtures["match_no"].apply(lambda value: f"M{int(value):03d}" if pd.notna(value) else ""),
            "Phase": fixtures["stage"],
            "Side A": fixtures["home"],
            "Side B": fixtures["away"],
            "Prediction": "",
            "AI Signal": fixtures.apply(
                lambda row: "Rule-based squad-aware scout signal ready"
                if row.get("team_data_status") == "known_teams"
                else "Result-dependent bracket slot",
                axis=1,
            ),
            "Confidence %": "",
            "Watch Priority": fixtures["group"].apply(lambda value: f"Group {value}" if str(value).strip() else "Knockout"),
            "Notes": fixtures.apply(
                lambda row: " | ".join(
                    part
                    for part in [
                        str(row.get("date", "")).strip(),
                        str(row.get("kickoff_local", "")).strip(),
                        str(row.get("city", "")).strip(),
                        str(row.get("stadium", "")).strip(),
                    ]
                    if part
                ),
                axis=1,
            ),
            "Result": "",
            "Points": "",
        }
    )
    return planner.astype(object)


def validate_wc2026_dataset() -> dict:
    result = {
        "groups_count": 0,
        "teams_count": 0,
        "fixtures_count": 0,
        "group_stage_count": 0,
        "knockout_count": 0,
        "squad_rows_count": 0,
        "errors": [],
        "warnings": [],
    }
    try:
        groups = load_groups()
        fixtures = load_fixtures()
        squads = load_squads()
        load_team_metadata()
    except Exception as exc:
        result["errors"].append(str(exc))
        return result

    result["groups_count"] = int(groups["group"].nunique())
    result["teams_count"] = int(groups["team"].nunique())
    result["fixtures_count"] = int(len(fixtures))
    result["group_stage_count"] = int((fixtures["match_no"] <= 72).sum())
    result["knockout_count"] = int((fixtures["match_no"] >= 73).sum())
    result["squad_rows_count"] = int(len(squads))

    if result["groups_count"] != 12:
        result["errors"].append(f"Expected 12 groups, found {result['groups_count']}.")
    if result["teams_count"] != 48:
        result["errors"].append(f"Expected 48 teams, found {result['teams_count']}.")
    if sorted(fixtures["match_no"].dropna().astype(int).tolist()) != list(range(1, 105)):
        result["errors"].append("Fixture match_no values must be exactly 1-104.")
    if result["fixtures_count"] != 104:
        result["errors"].append(f"Expected 104 fixtures, found {result['fixtures_count']}.")
    if result["group_stage_count"] != 72:
        result["errors"].append(f"Expected 72 group-stage fixtures, found {result['group_stage_count']}.")
    if result["knockout_count"] != 32:
        result["errors"].append(f"Expected 32 knockout fixtures, found {result['knockout_count']}.")
    if result["squad_rows_count"] != 1248:
        result["warnings"].append(f"Squad parser warning: {result['squad_rows_count']} / 1248 player rows parsed.")
    if groups.groupby("group")["team"].count().ne(4).any():
        result["errors"].append("Every group must contain exactly four teams.")
    if fixtures[["date", "home", "away"]].eq("").any().any():
        result["errors"].append("Fixtures must not contain blank date, home, or away values.")
    return result
