from __future__ import annotations

import pandas as pd


GROUP_IDS = tuple("ABCDEFGHIJKL")
ROUND_ROBIN_PAIRINGS = (
    (1, 2),
    (3, 4),
    (1, 3),
    (2, 4),
    (1, 4),
    (2, 3),
)
RESULT_CYCLE = (
    "2-1",
    "1-1",
    "3-0",
    "0-2",
    "2-2",
    "1-0",
)
PREDICTION_CYCLE = (
    "2-1",
    "1-0",
    "2-0",
    "0-1",
    "1-1",
    "1-0",
)


def _group_match_plan() -> dict[str, dict[str, str]]:
    plan: dict[str, dict[str, str]] = {}
    match_number = 1
    for group in GROUP_IDS:
        teams = {idx: f"Group {group} Team {idx}" for idx in range(1, 5)}
        for pairing_index, (side_a, side_b) in enumerate(ROUND_ROBIN_PAIRINGS):
            match_id = f"M{match_number:03d}"
            plan[match_id] = {
                "Phase": f"Group {group}",
                "Side A": teams[side_a],
                "Side B": teams[side_b],
                "Prediction": PREDICTION_CYCLE[(pairing_index + GROUP_IDS.index(group)) % len(PREDICTION_CYCLE)],
                "AI Signal": f"Demo signal {group}{pairing_index + 1}",
                "Confidence %": 62 + ((match_number * 7) % 31),
                "Watch Priority": ("Normal", "Watch", "High", "Must Watch")[pairing_index % 4],
                "Notes": "Demo scenario seed. Editable generic teams only.",
                "Result": RESULT_CYCLE[(pairing_index + GROUP_IDS.index(group)) % len(RESULT_CYCLE)],
            }
            match_number += 1
    return plan


def apply_demo_scenario(matches_df: pd.DataFrame) -> pd.DataFrame:
    demo = matches_df.copy(deep=True)
    plan = _group_match_plan()

    for column in ("Phase", "Side A", "Side B", "Prediction", "AI Signal", "Confidence %", "Watch Priority", "Notes", "Result"):
        if column not in demo.columns:
            demo[column] = ""

    for row_index, row in demo.iterrows():
        match_id = str(row.get("Match ID", "")).strip().upper()
        if match_id not in plan:
            continue
        for column, value in plan[match_id].items():
            demo.at[row_index, column] = value

    return demo
