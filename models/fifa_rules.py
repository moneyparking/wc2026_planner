from __future__ import annotations

import pandas as pd

from models.scoring import parse_score


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
                {"Group": group, "Team": team, "P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0},
            )
            row["P"] += 1
            row["GF"] += gf
            row["GA"] += ga
            row["GD"] = row["GF"] - row["GA"]
            if gf > ga:
                row["W"] += 1
                row["Pts"] += 3
            elif gf == ga:
                row["D"] += 1
                row["Pts"] += 1
            else:
                row["L"] += 1

    if not rows:
        return pd.DataFrame(columns=["Group", "Rank", "Team", "P", "W", "D", "L", "GF", "GA", "GD", "Pts"])

    table = pd.DataFrame(rows.values())
    table = table.sort_values(["Group", "Pts", "GD", "GF", "Team"], ascending=[True, False, False, False, True])
    table["Rank"] = table.groupby("Group").cumcount() + 1
    return table[["Group", "Rank", "Team", "P", "W", "D", "L", "GF", "GA", "GD", "Pts"]].reset_index(drop=True)


def build_third_place_table(group_table: pd.DataFrame) -> pd.DataFrame:
    if group_table.empty or "Rank" not in group_table.columns:
        return pd.DataFrame(columns=group_table.columns)
    thirds = group_table[group_table["Rank"] == 3].copy()
    if thirds.empty:
        return thirds
    thirds = thirds.sort_values(["Pts", "GD", "GF", "Team"], ascending=[False, False, False, True])
    thirds["Third Rank"] = range(1, len(thirds) + 1)
    return thirds.reset_index(drop=True)


# TODO Phase 2: implement the full official tournament tie-breaker sequence.


compute_group_table = build_group_table
third_place_ranking = build_third_place_table
