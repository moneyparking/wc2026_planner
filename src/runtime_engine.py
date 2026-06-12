from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

import pandas as pd


COMPLETED_STATUSES = {"FT", "AET", "PEN", "COMPLETED", "FINISHED"}
LIVE_STATUSES = {"LIVE", "1H", "2H", "HT", "ET"}


def _match_no(value: object) -> int | None:
    if value is None:
        return None
    text = str(value).strip().upper()
    if text.startswith("M"):
        text = text[1:]
    try:
        return int(text)
    except ValueError:
        return None


def _score(value: object) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_dict(item: Any) -> dict:
    if is_dataclass(item):
        return asdict(item)
    return dict(item or {})


def _first_present(row: dict, *keys: str) -> object:
    for key in keys:
        if key in row and row.get(key) not in (None, ""):
            return row.get(key)
    return None


def _manual_rows(sheet_state: Any, local_edits: Any = None) -> list[dict]:
    rows: list[dict] = []
    if sheet_state is not None:
        rows.extend(getattr(sheet_state, "manual_results", []) or [])
    if local_edits is None:
        return rows
    if isinstance(local_edits, pd.DataFrame):
        rows.extend(local_edits.to_dict("records"))
    elif isinstance(local_edits, list):
        rows.extend(local_edits)
    return rows


def _normalize_manual(row: dict) -> dict | None:
    match_no = _match_no(
        _first_present(row, "match_no", "Match No", "Match_No", "Match ID", "match_id")
    )
    if match_no is None:
        return None
    result = str(row.get("Result") or row.get("result") or "").strip()
    home_score = _score(_first_present(row, "home_score", "Home Score", "Score_A"))
    away_score = _score(_first_present(row, "away_score", "Away Score", "Score_B"))
    if result and "-" in result and (home_score is None or away_score is None):
        left, right = result.split("-", 1)
        home_score = _score(left.strip())
        away_score = _score(right.strip())
    if home_score is None or away_score is None:
        return None
    return {
        "match_no": match_no,
        "home_score": home_score,
        "away_score": away_score,
        "status": str(row.get("status") or row.get("Status") or "FT"),
        "minute": _score(_first_present(row, "minute", "Minute")),
        "source": str(row.get("source") or row.get("Source") or "manual override"),
        "synced_at_utc": str(row.get("synced_at_utc") or row.get("Synced At UTC") or ""),
    }


def _normalize_live(live_result: Any) -> dict | None:
    row = _as_dict(live_result)
    match_no = _match_no(row.get("match_no"))
    home_score = _score(row.get("home_score"))
    away_score = _score(row.get("away_score"))
    if match_no is None or home_score is None or away_score is None:
        return None
    return {
        "match_no": match_no,
        "home_score": home_score,
        "away_score": away_score,
        "status": str(row.get("status") or "Scheduled"),
        "minute": _score(row.get("minute")),
        "source": str(row.get("source") or "live provider"),
        "synced_at_utc": str(row.get("synced_at_utc") or ""),
    }


def build_runtime_match_state(
    fixtures_df,
    live_results,
    sheet_state,
    local_edits=None,
) -> pd.DataFrame:
    fixtures = fixtures_df.copy().sort_values("match_no").reset_index(drop=True)
    fixtures["match_no"] = pd.to_numeric(fixtures["match_no"], errors="coerce").astype(int)

    live_by_match = {
        row["match_no"]: row
        for row in (_normalize_live(item) for item in (live_results or []))
        if row is not None
    }
    manual_by_match = {
        row["match_no"]: row
        for row in (_normalize_manual(item) for item in _manual_rows(sheet_state, local_edits))
        if row is not None
    }

    rows = []
    for _, fixture in fixtures.iterrows():
        match_no = int(fixture["match_no"])
        source_row = None
        result_source = "static_fixture"
        is_manual = False
        if match_no in manual_by_match:
            source_row = manual_by_match[match_no]
            result_source = source_row["source"] or "manual override"
            is_manual = True
        elif match_no in live_by_match:
            source_row = live_by_match[match_no]
            result_source = source_row["source"] or "live provider"

        home_score = source_row["home_score"] if source_row else None
        away_score = source_row["away_score"] if source_row else None
        status = source_row["status"] if source_row else "Scheduled"
        minute = source_row["minute"] if source_row else None
        synced_at = source_row["synced_at_utc"] if source_row else ""
        status_upper = str(status).upper()
        rows.append(
            {
                "match_no": match_no,
                "stage": fixture.get("stage", ""),
                "group": fixture.get("group", ""),
                "date": fixture.get("date", ""),
                "home": fixture.get("home", ""),
                "away": fixture.get("away", ""),
                "home_score": home_score,
                "away_score": away_score,
                "status": status,
                "minute": minute,
                "result_source": result_source,
                "synced_at_utc": synced_at,
                "is_completed": status_upper in COMPLETED_STATUSES or (home_score is not None and away_score is not None and status_upper == "FT"),
                "is_live": status_upper in LIVE_STATUSES,
                "is_manual_override": is_manual,
                "city": fixture.get("city", ""),
                "country": fixture.get("country", ""),
                "stadium": fixture.get("stadium", ""),
            }
        )
    return pd.DataFrame(rows)


def runtime_to_match_planner(runtime_df: pd.DataFrame) -> pd.DataFrame:
    runtime = runtime_df.copy()
    result = runtime.apply(
        lambda row: f"{int(row['home_score'])}-{int(row['away_score'])}"
        if pd.notna(row.get("home_score")) and pd.notna(row.get("away_score"))
        else "",
        axis=1,
    )
    return pd.DataFrame(
        {
            "Match ID": runtime["match_no"].astype(int).apply(lambda value: f"M{value:03d}"),
            "Phase": runtime.apply(
                lambda row: f"Group {row['group']}" if str(row.get("group", "")).strip() else row["stage"],
                axis=1,
            ),
            "Side A": runtime["home"],
            "Side B": runtime["away"],
            "Prediction": "",
            "AI Signal": runtime["result_source"].apply(lambda value: f"Runtime source: {value}"),
            "Confidence %": "",
            "Watch Priority": runtime["group"].apply(lambda value: f"Group {value}" if str(value).strip() else "Knockout"),
            "Notes": runtime.apply(lambda row: f"{row['date']} · {row['city']} · {row['stadium']}", axis=1),
            "Result": result,
            "Points": "",
        }
    ).astype(object)
