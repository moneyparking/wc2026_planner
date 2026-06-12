from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_JSON_PATH = REPO_ROOT / "data" / "live_results_override.json"
SUPPORTED_STUB_PROVIDERS = {"api_football", "sportmonks", "football_data"}


@dataclass
class LiveMatchResult:
    match_no: int
    home_score: Optional[int]
    away_score: Optional[int]
    status: str
    minute: Optional[int]
    source: str
    synced_at_utc: str
    confidence: str
    raw_id: str = ""


@dataclass
class LiveScoreRuntimeStatus:
    enabled: bool
    provider: str
    last_sync_utc: str
    warnings: list[str]


_LAST_STATUS = LiveScoreRuntimeStatus(
    enabled=False,
    provider="none",
    last_sync_utc="",
    warnings=["Live scores disabled: no provider configured."],
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _coerce_int(value: object) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _status_for_off(provider: str, warning: str) -> LiveScoreRuntimeStatus:
    return LiveScoreRuntimeStatus(enabled=False, provider=provider, last_sync_utc="", warnings=[warning])


def get_live_score_status() -> LiveScoreRuntimeStatus:
    return _LAST_STATUS


def fetch_live_results() -> list[LiveMatchResult]:
    global _LAST_STATUS

    provider = os.getenv("LIVE_SCORE_PROVIDER", "none").strip().lower() or "none"
    api_key = os.getenv("LIVE_SCORE_API_KEY", "").strip()

    if provider == "none":
        _LAST_STATUS = _status_for_off(provider, "Live scores disabled: LIVE_SCORE_PROVIDER=none.")
        return []

    if provider == "local_json":
        if not LOCAL_JSON_PATH.exists():
            _LAST_STATUS = _status_for_off(provider, f"local_json provider missing {LOCAL_JSON_PATH.relative_to(REPO_ROOT)}.")
            return []
        try:
            payload = json.loads(LOCAL_JSON_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            _LAST_STATUS = _status_for_off(provider, f"local_json provider could not parse JSON: {exc}.")
            return []

        results: list[LiveMatchResult] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            match_no = _coerce_int(item.get("match_no"))
            if match_no is None:
                continue
            synced = str(item.get("synced_at_utc") or _utc_now_iso())
            results.append(
                LiveMatchResult(
                    match_no=match_no,
                    home_score=_coerce_int(item.get("home_score")),
                    away_score=_coerce_int(item.get("away_score")),
                    status=str(item.get("status") or "Scheduled"),
                    minute=_coerce_int(item.get("minute")),
                    source=str(item.get("source") or "local_json"),
                    synced_at_utc=synced,
                    confidence=str(item.get("confidence") or "manual_demo"),
                    raw_id=str(item.get("raw_id") or ""),
                )
            )
        last_sync = results[0].synced_at_utc if results else _utc_now_iso()
        _LAST_STATUS = LiveScoreRuntimeStatus(
            enabled=True,
            provider="local_json",
            last_sync_utc=last_sync,
            warnings=[],
        )
        return results

    if provider in SUPPORTED_STUB_PROVIDERS:
        if not api_key:
            _LAST_STATUS = _status_for_off(provider, f"Live scores disabled: {provider} configured but LIVE_SCORE_API_KEY missing.")
            return []
        _LAST_STATUS = _status_for_off(
            provider,
            f"Provider configured but adapter credentials/mapping incomplete: {provider}.",
        )
        return []

    _LAST_STATUS = _status_for_off(provider, f"Live scores disabled: unsupported provider '{provider}'.")
    return []
