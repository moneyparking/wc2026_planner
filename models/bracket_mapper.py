from __future__ import annotations

import pandas as pd


def extract_top_third_place_groups(third_places_df: pd.DataFrame) -> list[str]:
    if third_places_df.empty:
        return []
    thirds = third_places_df.copy()
    sort_columns = [column for column in ["Pts", "GD", "GF", "Team"] if column in thirds.columns]
    ascending = [False, False, False, True][: len(sort_columns)]
    if sort_columns:
        thirds = thirds.sort_values(sort_columns, ascending=ascending)
    groups = [str(value) for value in thirds["Group"].head(8).tolist()]
    return [group[-1] if len(group) > 1 and group.lower().startswith("group ") else group for group in groups]


def make_third_place_key(top_8_third_places: list[str]) -> str:
    return "".join(sorted(str(group) for group in top_8_third_places))


def build_bracket_mapping(groups_df: pd.DataFrame, third_places_df: pd.DataFrame, annex_c_df: pd.DataFrame) -> dict:
    qualified_third_groups = extract_top_third_place_groups(third_places_df)
    key = make_third_place_key(qualified_third_groups)

    if annex_c_df is None or annex_c_df.empty:
        return {
            "status": "annex_c_missing",
            "qualified_third_groups": qualified_third_groups,
            "third_place_key": key,
        }

    return {
        "status": "annex_c_loaded_but_mapping_pending",
        "source": "AnnexC_495_STATIC",
        "qualified_third_groups": qualified_third_groups,
        "third_place_key": key,
        "round_of_32": {},
    }


extract_third_place_groups = extract_top_third_place_groups
