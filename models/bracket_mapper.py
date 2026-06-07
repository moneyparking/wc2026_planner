from __future__ import annotations

import pandas as pd


def build_later_round_dependencies() -> dict:
    return {
        "R16_M089": {"depends_on": ["R32_M073", "R32_M074"]},
        "R16_M090": {"depends_on": ["R32_M075", "R32_M076"]},
        "R16_M091": {"depends_on": ["R32_M077", "R32_M078"]},
        "R16_M092": {"depends_on": ["R32_M079", "R32_M080"]},
        "R16_M093": {"depends_on": ["R32_M081", "R32_M082"]},
        "R16_M094": {"depends_on": ["R32_M083", "R32_M084"]},
        "R16_M095": {"depends_on": ["R32_M085", "R32_M086"]},
        "R16_M096": {"depends_on": ["R32_M087", "R32_M088"]},
        "QF_M097": {"depends_on": ["R16_M089", "R16_M090"]},
        "QF_M098": {"depends_on": ["R16_M091", "R16_M092"]},
        "QF_M099": {"depends_on": ["R16_M093", "R16_M094"]},
        "QF_M100": {"depends_on": ["R16_M095", "R16_M096"]},
        "SF_M101": {"depends_on": ["QF_M097", "QF_M098"]},
        "SF_M102": {"depends_on": ["QF_M099", "QF_M100"]},
        "THIRD_PLACE_M103": {"depends_on": ["SF_M101", "SF_M102"]},
        "FINAL_M104": {"depends_on": ["SF_M101", "SF_M102"]},
    }


def extract_top_third_place_groups(third_places_df: pd.DataFrame) -> list[str]:
    if third_places_df is None or third_places_df.empty:
        return []
    thirds = third_places_df.copy()
    sort_columns = [column for column in ["Pts", "GD", "GF", "Team"] if column in thirds.columns]
    ascending = [False, False, False, True][: len(sort_columns)]
    if sort_columns:
        thirds = thirds.sort_values(sort_columns, ascending=ascending)
    group_column = "Group_ID" if "Group_ID" in thirds.columns else "Group"
    groups = [str(value) for value in thirds[group_column].head(8).tolist()]
    return [group[-1] if len(group) > 1 and group.lower().startswith("group ") else group for group in groups]


def make_third_place_key(top_8_third_places: list[str]) -> str:
    return "".join(sorted(str(group) for group in top_8_third_places))


def build_bracket_mapping(groups_df: pd.DataFrame, third_places_df: pd.DataFrame, annex_c_df: pd.DataFrame) -> dict:
    if third_places_df is None or third_places_df.empty:
        return {
            "status": "waiting_for_completed_results",
            "source": "AnnexC_495_STATIC",
            "third_place_key": "",
            "qualified_third_groups": [],
            "round_of_32": {},
            "later_rounds": build_later_round_dependencies(),
            "message": (
                "Enter completed match results in MATCH_PLANNER to generate the third-place key "
                "and Round of 32 mapping."
            ),
        }

    qualified_third_groups = extract_top_third_place_groups(third_places_df)
    key = make_third_place_key(qualified_third_groups)

    if annex_c_df is None or annex_c_df.empty:
        return {
            "status": "annex_c_missing",
            "qualified_third_groups": qualified_third_groups,
            "third_place_key": key,
            "round_of_32": {},
            "later_rounds": build_later_round_dependencies(),
        }

    return {
        "status": "annex_c_loaded_but_mapping_pending",
        "source": "AnnexC_495_STATIC",
        "qualified_third_groups": qualified_third_groups,
        "third_place_key": key,
        "round_of_32": {},
        "later_rounds": build_later_round_dependencies(),
    }


extract_third_place_groups = extract_top_third_place_groups
