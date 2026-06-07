from __future__ import annotations

import pandas as pd

from models.scoring import parse_score


GROUP_TABLE_COLUMNS = [
    "Group_ID",
    "Team",
    "Played",
    "Won",
    "Drawn",
    "Lost",
    "GF",
    "GA",
    "GD",
    "Pts",
    "Rank",
]

THIRD_PLACE_COLUMNS = [
    "Group_ID",
    "Team",
    "Played",
    "GF",
    "GA",
    "GD",
    "Pts",
    "Group_Rank",
    "Third_Place_Rank",
    "Qualified",
]


def empty_group_table() -> pd.DataFrame:
    return pd.DataFrame(columns=GROUP_TABLE_COLUMNS)


def empty_third_place_table() -> pd.DataFrame:
    return pd.DataFrame(columns=THIRD_PLACE_COLUMNS)


def derive_completed_matches(matches: pd.DataFrame) -> pd.DataFrame:
    completed = matches.copy()
    completed["_score"] = completed["Result"].apply(parse_score)
    completed = completed[completed["_score"].notna()].copy()
    if completed.empty:
        return completed.drop(columns=["_score"])
    completed[["Goals A", "Goals B"]] = pd.DataFrame(completed["_score"].tolist(), index=completed.index)
    return completed.drop(columns=["_score"])


def _phase_group_label(phase: object) -> str:
    text = "" if pd.isna(phase) else str(phase).strip()
    return text or "Group Stage"


def build_group_table(matches: pd.DataFrame) -> pd.DataFrame:
    if matches is None or matches.empty:
        return empty_group_table()
    if "Result" not in matches.columns:
        return empty_group_table()

    has_result = matches["Result"].fillna("").astype(str).str.strip().ne("")
    if not has_result.any():
        return empty_group_table()

    completed = derive_completed_matches(matches)
    rows: dict[tuple[str, str], dict] = {}

    for _, match in completed.iterrows():
        group = _phase_group_label(match.get("Phase"))
        teams = [
            (str(match.get("Side A", "")).strip() or "Side A", int(match["Goals A"]), int(match["Goals B"])),
            (str(match.get("Side B", "")).strip() or "Side B", int(match["Goals B"]), int(match["Goals A"])),
        ]
        for team, gf, ga in teams:
            key = (group, team)
            row = rows.setdefault(
                key,
                {
                    "Group_ID": group,
                    "Team": team,
                    "Played": 0,
                    "Won": 0,
                    "Drawn": 0,
                    "Lost": 0,
                    "GF": 0,
                    "GA": 0,
                    "GD": 0,
                    "Pts": 0,
                },
            )
            row["Played"] += 1
            row["GF"] += gf
            row["GA"] += ga
            row["GD"] = row["GF"] - row["GA"]
            if gf > ga:
                row["Won"] += 1
                row["Pts"] += 3
            elif gf == ga:
                row["Drawn"] += 1
                row["Pts"] += 1
            else:
                row["Lost"] += 1

    if not rows:
        return empty_group_table()

    table = pd.DataFrame(rows.values())
    table = table.sort_values(["Group_ID", "Pts", "GD", "GF", "Team"], ascending=[True, False, False, False, True])
    table["Rank"] = table.groupby("Group_ID").cumcount() + 1
    return table[GROUP_TABLE_COLUMNS].reset_index(drop=True)


def build_third_place_table(group_table: pd.DataFrame) -> pd.DataFrame:
    if group_table.empty or "Rank" not in group_table.columns:
        return empty_third_place_table()
    thirds = group_table[group_table["Rank"] == 3].copy()
    if thirds.empty:
        return empty_third_place_table()
    thirds = thirds.sort_values(["Pts", "GD", "GF", "Team"], ascending=[False, False, False, True])
    thirds["Group_Rank"] = thirds["Rank"]
    thirds["Third_Place_Rank"] = range(1, len(thirds) + 1)
    thirds["Qualified"] = thirds["Third_Place_Rank"] <= 8
    return thirds[
        ["Group_ID", "Team", "Played", "GF", "GA", "GD", "Pts", "Group_Rank", "Third_Place_Rank", "Qualified"]
    ].reset_index(drop=True)


# TODO Phase 2: implement the full official tournament tie-breaker sequence.


compute_group_table = build_group_table
third_place_ranking = build_third_place_table
