from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os


@dataclass
class SheetRuntimeState:
    enabled: bool
    connected: bool
    spreadsheet_id: str
    last_pull_utc: str
    warnings: list[str]
    manual_results: list[dict]
    friends_picks: list[dict]
    admin_notes: list[dict]


EXPECTED_TABS = ["Results_Override", "Friends_Picks", "League_Settings", "Admin_Notes"]


def _disabled_state(spreadsheet_id: str = "", warning: str | None = None) -> SheetRuntimeState:
    return SheetRuntimeState(
        enabled=False,
        connected=False,
        spreadsheet_id=spreadsheet_id,
        last_pull_utc="",
        warnings=[warning or "Google Sheet disabled: GOOGLE_SHEET_ENABLED=false or credentials missing."],
        manual_results=[],
        friends_picks=[],
        admin_notes=[],
    )


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _values_to_dicts(values: list[list[object]]) -> list[dict]:
    if not values:
        return []
    headers = [str(value).strip() for value in values[0]]
    rows = []
    for raw in values[1:]:
        row = {header: raw[idx] if idx < len(raw) else "" for idx, header in enumerate(headers) if header}
        if any(str(value).strip() for value in row.values()):
            rows.append(row)
    return rows


def pull_sheet_runtime_state() -> SheetRuntimeState:
    enabled = os.getenv("GOOGLE_SHEET_ENABLED", "false").strip().lower() == "true"
    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID", "").strip()
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()

    if not enabled or not spreadsheet_id or not service_account_json:
        return _disabled_state(spreadsheet_id)

    try:
        info = json.loads(service_account_json)
    except json.JSONDecodeError:
        return _disabled_state(spreadsheet_id, "Google Sheet disabled: GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON.")

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        return SheetRuntimeState(
            enabled=True,
            connected=False,
            spreadsheet_id=spreadsheet_id,
            last_pull_utc="",
            warnings=["Google Sheet enabled but Google API client libraries are not installed."],
            manual_results=[],
            friends_picks=[],
            admin_notes=[],
        )

    try:
        credentials = service_account.Credentials.from_service_account_info(
            info,
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
        )
        service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
        sheet = service.spreadsheets()

        def read_tab(tab: str) -> list[dict]:
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=f"{tab}!A:Z").execute()
            return _values_to_dicts(result.get("values", []))

        manual_results = read_tab("Results_Override")
        friends_picks = read_tab("Friends_Picks")
        admin_notes = read_tab("Admin_Notes")
        warnings = []
        sheet.values().get(spreadsheetId=spreadsheet_id, range="League_Settings!A:Z").execute()
        return SheetRuntimeState(
            enabled=True,
            connected=True,
            spreadsheet_id=spreadsheet_id,
            last_pull_utc=_utc_now_iso(),
            warnings=warnings,
            manual_results=manual_results,
            friends_picks=friends_picks,
            admin_notes=admin_notes,
        )
    except Exception as exc:
        return SheetRuntimeState(
            enabled=True,
            connected=False,
            spreadsheet_id=spreadsheet_id,
            last_pull_utc="",
            warnings=[f"Google Sheet enabled but pull failed: {type(exc).__name__}."],
            manual_results=[],
            friends_picks=[],
            admin_notes=[],
        )
