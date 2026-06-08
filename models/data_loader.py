from __future__ import annotations

from pathlib import Path
from typing import Iterable
import warnings

import pandas as pd

from product_config import (
    EXPECTED_ANNEX_C_RECORD_COUNT,
    EXPECTED_MATCH_COUNT,
    FRIENDS_COLUMNS,
    MATCH_COLUMNS,
    OPTIONAL_SHEETS,
    REQUIRED_SHEETS,
    SHEET_ANNEX_C,
    SHEET_FRIENDS_LEAGUE,
    SHEET_MATCH_PLANNER,
    SPREADSHEET_CANDIDATE_PATHS,
)


def phase_for_match_id(match_id: object) -> str:
    text = str(match_id).strip().upper()
    if not text.startswith("M"):
        return ""
    try:
        number = int(text[1:])
    except ValueError:
        return ""
    if 1 <= number <= 72:
        return "Group Stage"
    if 73 <= number <= 88:
        return "Round of 32"
    if 89 <= number <= 96:
        return "Round of 16"
    if 97 <= number <= 100:
        return "Quarterfinal"
    if 101 <= number <= 102:
        return "Semifinal"
    if number == 103:
        return "Third Place"
    if number == 104:
        return "Final"
    return ""


def resolve_spreadsheet_path(candidates: Iterable[Path] = SPREADSHEET_CANDIDATE_PATHS) -> Path:
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return path.resolve()
    joined = "\n".join(str(Path(candidate)) for candidate in candidates)
    raise FileNotFoundError(f"No spreadsheet source found. Checked:\n{joined}")


def _clean_label(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def _find_header_row(raw: pd.DataFrame, required_columns: Iterable[str]) -> int:
    required = set(required_columns)
    for idx, row in raw.iterrows():
        labels = {_clean_label(value) for value in row.tolist()}
        if required.issubset(labels):
            return int(idx)
    raise ValueError(f"Could not find header row with columns: {', '.join(required_columns)}")


def _read_table(path: Path, sheet_name: str, required_columns: Iterable[str] | None = None) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=sheet_name, header=None, dtype=object)
    if required_columns is None:
        required_columns = []
    header_row = _find_header_row(raw, required_columns) if required_columns else 0
    headers = [_clean_label(value) or f"Column {idx + 1}" for idx, value in enumerate(raw.iloc[header_row].tolist())]
    table = raw.iloc[header_row + 1 :].copy()
    table.columns = headers
    table = table.dropna(how="all").reset_index(drop=True)
    return table


def normalize_match_columns(matches: pd.DataFrame) -> pd.DataFrame:
    normalized = matches.copy()
    rename_map = {column: column.strip() for column in normalized.columns if isinstance(column, str)}
    normalized = normalized.rename(columns=rename_map)
    for column in MATCH_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = ""
    normalized = normalized.loc[:, list(MATCH_COLUMNS)]
    normalized["Match ID"] = normalized["Match ID"].astype(str).str.strip()
    normalized = normalized[normalized["Match ID"].ne("") & normalized["Match ID"].ne("nan")].reset_index(drop=True)
    normalized = normalized[normalized["Match ID"].str.match(r"^M(0[0-9][1-9]|0[1-9][0-9]|10[0-4])$", na=False)]
    normalized = normalized.head(EXPECTED_MATCH_COUNT).reset_index(drop=True)
    normalized["Phase"] = normalized["Match ID"].apply(phase_for_match_id)
    return normalized


def _normalize_friends_columns(friends: pd.DataFrame) -> pd.DataFrame:
    normalized = friends.copy()
    rename_map = {column: column.strip() for column in normalized.columns if isinstance(column, str)}
    normalized = normalized.rename(columns=rename_map)
    for column in FRIENDS_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = ""
    normalized = normalized.loc[:, list(FRIENDS_COLUMNS)]
    normalized["Player"] = normalized["Player"].astype(str).str.strip()
    normalized = normalized[normalized["Player"].ne("") & normalized["Player"].ne("nan")].reset_index(drop=True)
    return normalized


def load_workbook_state(path: str | Path | None = None) -> dict:
    spreadsheet_path = Path(path).resolve() if path else resolve_spreadsheet_path()
    excel = pd.ExcelFile(spreadsheet_path)
    sheet_names = list(excel.sheet_names)
    load_warnings: list[str] = []

    missing_required = [sheet for sheet in REQUIRED_SHEETS if sheet not in sheet_names]
    if missing_required:
        raise ValueError(f"Missing required sheet(s): {', '.join(missing_required)}")

    missing_optional = [sheet for sheet in OPTIONAL_SHEETS if sheet not in sheet_names]
    if missing_optional:
        load_warnings.append(f"Optional sheet(s) missing: {', '.join(missing_optional)}")

    matches = normalize_match_columns(_read_table(spreadsheet_path, SHEET_MATCH_PLANNER, MATCH_COLUMNS))
    friends = _normalize_friends_columns(_read_table(spreadsheet_path, SHEET_FRIENDS_LEAGUE, FRIENDS_COLUMNS))
    annex_c = _read_table(
        spreadsheet_path,
        SHEET_ANNEX_C,
        ("annex_id", "module", "record_type", "code", "label"),
    )

    state = {
        "spreadsheet_path": str(spreadsheet_path),
        "sheet_names": sheet_names,
        "matches": matches,
        "friends": friends,
        "annex_c": annex_c,
        "warnings": load_warnings,
    }
    validate_state(state)
    return state


def validate_state(state: dict) -> None:
    matches = state.get("matches")
    annex_c = state.get("annex_c")
    if matches is None:
        raise ValueError("MATCH_PLANNER could not be loaded.")
    if len(matches) < EXPECTED_MATCH_COUNT:
        raise ValueError(f"MATCH_PLANNER has {len(matches)} rows; expected at least {EXPECTED_MATCH_COUNT}.")
    if len(matches) > EXPECTED_MATCH_COUNT:
        warnings.warn(
            f"MATCH_PLANNER has {len(matches)} rows; Build Small uses the first {EXPECTED_MATCH_COUNT}.",
            stacklevel=2,
        )
    if annex_c is None or len(annex_c) < EXPECTED_ANNEX_C_RECORD_COUNT:
        warnings.warn(
            f"Annex C has {0 if annex_c is None else len(annex_c)} rows; expected {EXPECTED_ANNEX_C_RECORD_COUNT}.",
            stacklevel=2,
        )
