from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import csv
import json
import os
from pathlib import Path
from typing import Any, Optional

import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
LOCAL_JSON_PATH = DATA_DIR / "live_results_override.json"
VERIFIED_CACHE_PATH = DATA_DIR / "worldcup_results_verified.json"
PROVIDER_MAP_PATH = DATA_DIR / "provider_match_id_map.csv"
SUPPORTED_PROVIDERS = {
    "none",
    "verified_cache",
    "local_json",
    "live_score_api",
    "football_data",
    "sportmonks",
    "api_football",
}
COMPLETED_STATUSES = {"FT", "AET", "PEN", "COMPLETED", "FINISHED", "FINISHED_PEN"}
LIVE_STATUSES = {"LIVE", "IN_PLAY", "PAUSED", "1H", "2H", "HT", "ET"}


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
    raw_id: str
    source_note: str


@dataclass
class LiveScoreRuntimeStatus:
    enabled: bool
    provider: str
    last_sync_utc: str
    warnings: list[str]
    status_label: str


_LAST_STATUS = LiveScoreRuntimeStatus(
    enabled=False,
    provider="none",
    last_sync_utc="",
    warnings=["Live scores disabled: LIVE_SCORE_PROVIDER=none."],
    status_label="OFF",
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _coerce_int(value: object) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return None


def _norm_status(value: object) -> str:
    status = str(value or "Scheduled").strip()
    upper = status.upper()
    if upper in {"FINISHED", "COMPLETED", "FINISHED_PEN"}:
        return "FT"
    if upper in {"IN_PLAY", "LIVE"}:
        return "LIVE"
    return upper if upper else "Scheduled"


def _set_status(enabled: bool, provider: str, label: str, warnings: list[str] | None = None, last_sync: str = "") -> None:
    global _LAST_STATUS
    _LAST_STATUS = LiveScoreRuntimeStatus(
        enabled=enabled,
        provider=provider,
        last_sync_utc=last_sync,
        warnings=warnings or [],
        status_label=label,
    )


def get_live_score_status() -> LiveScoreRuntimeStatus:
    return _LAST_STATUS


def _read_json_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(str(path.relative_to(REPO_ROOT)))
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, list) else []


def _verified_cache_results(note_prefix: str = "verified public results cache") -> list[LiveMatchResult]:
    rows = _read_json_rows(VERIFIED_CACHE_PATH)
    results: list[LiveMatchResult] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        match_no = _coerce_int(row.get("match_no"))
        home_score = _coerce_int(row.get("home_score"))
        away_score = _coerce_int(row.get("away_score"))
        if match_no is None or home_score is None or away_score is None:
            continue
        results.append(
            LiveMatchResult(
                match_no=match_no,
                home_score=home_score,
                away_score=away_score,
                status=_norm_status(row.get("status") or "FT"),
                minute=None,
                source="verified public results cache",
                synced_at_utc=str(row.get("verified_at_utc") or _utc_now_iso()),
                confidence=str(row.get("confidence") or "verified"),
                raw_id=str(row.get("raw_id") or ""),
                source_note=f"{note_prefix}: {row.get('notes') or row.get('primary_source') or ''}".strip(),
            )
        )
    return results


def _local_json_results() -> list[LiveMatchResult]:
    results: list[LiveMatchResult] = []
    for row in _read_json_rows(LOCAL_JSON_PATH):
        if not isinstance(row, dict):
            continue
        match_no = _coerce_int(row.get("match_no"))
        if match_no is None:
            continue
        results.append(
            LiveMatchResult(
                match_no=match_no,
                home_score=_coerce_int(row.get("home_score")),
                away_score=_coerce_int(row.get("away_score")),
                status=_norm_status(row.get("status")),
                minute=_coerce_int(row.get("minute")),
                source=str(row.get("source") or "local override/cache"),
                synced_at_utc=str(row.get("synced_at_utc") or _utc_now_iso()),
                confidence=str(row.get("confidence") or "manual_override"),
                raw_id=str(row.get("raw_id") or ""),
                source_note=str(row.get("source_note") or "local_json override/cache; not a live provider"),
            )
        )
    return results


def _provider_map(provider: str) -> dict[str, int]:
    mapping: dict[str, int] = {}
    if not PROVIDER_MAP_PATH.exists():
        return mapping
    with PROVIDER_MAP_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if str(row.get("provider", "")).strip().lower() != provider:
                continue
            provider_id = str(row.get("provider_match_id", "")).strip()
            match_no = _coerce_int(row.get("match_no"))
            if provider_id and match_no is not None:
                mapping[provider_id] = match_no
    return mapping


def _fixtures_lookup(fixtures_df: Any) -> dict[tuple[str, str, str], int]:
    if fixtures_df is None or not hasattr(fixtures_df, "iterrows"):
        return {}
    lookup: dict[tuple[str, str, str], int] = {}
    for _, row in fixtures_df.iterrows():
        match_no = _coerce_int(row.get("match_no"))
        if match_no is None:
            continue
        key = (
            str(row.get("home", "")).strip().lower(),
            str(row.get("away", "")).strip().lower(),
            str(row.get("date", "")).strip()[:10],
        )
        lookup[key] = match_no
    return lookup


def _map_match_no(provider: str, raw_id: object, item: dict[str, Any], fixtures_df: Any) -> Optional[int]:
    raw_text = str(raw_id or "").strip()
    mapped = _provider_map(provider).get(raw_text)
    if mapped:
        return mapped
    direct = _coerce_int(item.get("match_no") or item.get("matchNumber") or item.get("match_number"))
    if direct:
        return direct
    home = str(item.get("home") or item.get("home_team") or item.get("homeTeam", {}).get("name", "")).strip().lower()
    away = str(item.get("away") or item.get("away_team") or item.get("awayTeam", {}).get("name", "")).strip().lower()
    date = str(item.get("date") or item.get("utcDate") or item.get("starting_at") or item.get("fixture", {}).get("date", ""))[:10]
    return _fixtures_lookup(fixtures_df).get((home, away, date))


def _request_json(url: str, headers: dict[str, str] | None = None, params: dict[str, Any] | None = None) -> Any:
    response = requests.get(url, headers=headers or {}, params=params or {}, timeout=10)
    response.raise_for_status()
    return response.json()


def _items(payload: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _result(provider: str, match_no: Optional[int], raw_id: object, home_score: object, away_score: object, status: object, minute: object, note: str) -> Optional[LiveMatchResult]:
    if match_no is None:
        return None
    status_norm = _norm_status(status)
    score_a = _coerce_int(home_score)
    score_b = _coerce_int(away_score)
    if score_a is None or score_b is None:
        if status_norm not in LIVE_STATUSES:
            return None
    return LiveMatchResult(
        match_no=match_no,
        home_score=score_a,
        away_score=score_b,
        status=status_norm,
        minute=_coerce_int(minute),
        source=f"live provider: {provider}",
        synced_at_utc=_utc_now_iso(),
        confidence="provider",
        raw_id=str(raw_id or ""),
        source_note=note,
    )


def _fetch_live_score_api(fixtures_df: Any) -> list[LiveMatchResult]:
    key = os.getenv("LIVE_SCORE_API_KEY", "").strip()
    secret = os.getenv("LIVE_SCORE_API_SECRET", "").strip()
    competition = os.getenv("LIVE_SCORE_COMPETITION_ID", "").strip()
    if not key or not secret or not competition:
        raise RuntimeError("live_score_api credentials missing: LIVE_SCORE_API_KEY, LIVE_SCORE_API_SECRET, LIVE_SCORE_COMPETITION_ID required.")
    base = os.getenv("LIVE_SCORE_BASE_URL", "").strip() or "https://livescore-api.com/api-client/scores/live.json"
    payload = _request_json(base, params={"key": key, "secret": secret, "competition_id": competition})
    results = []
    for item in _items(payload, "data", "matches"):
        raw_id = item.get("id") or item.get("fixture_id")
        match_no = _map_match_no("live_score_api", raw_id, item, fixtures_df)
        scores = item.get("scores") if isinstance(item.get("scores"), dict) else {}
        results.append(_result("live_score_api", match_no, raw_id, scores.get("home_score", item.get("home_score")), scores.get("away_score", item.get("away_score")), item.get("status"), item.get("time"), "Live-Score API response"))
    return [item for item in results if item is not None]


def _fetch_football_data(fixtures_df: Any) -> list[LiveMatchResult]:
    key = os.getenv("FOOTBALL_DATA_API_KEY", "").strip()
    if not key:
        raise RuntimeError("football_data credentials missing: FOOTBALL_DATA_API_KEY required.")
    competition = os.getenv("LIVE_SCORE_COMPETITION_ID", "WC").strip() or "WC"
    base = os.getenv("LIVE_SCORE_BASE_URL", "").strip() or f"https://api.football-data.org/v4/competitions/{competition}/matches"
    payload = _request_json(base, headers={"X-Auth-Token": key})
    results = []
    for item in _items(payload, "matches"):
        raw_id = item.get("id")
        match_no = _map_match_no("football_data", raw_id, item, fixtures_df)
        score = item.get("score") if isinstance(item.get("score"), dict) else {}
        full = score.get("fullTime") if isinstance(score.get("fullTime"), dict) else {}
        results.append(_result("football_data", match_no, raw_id, full.get("home"), full.get("away"), item.get("status"), item.get("minute"), "football-data.org matches response"))
    return [item for item in results if item is not None]


def _fetch_sportmonks(fixtures_df: Any) -> list[LiveMatchResult]:
    key = os.getenv("SPORTMONKS_API_KEY", "").strip()
    if not key:
        raise RuntimeError("sportmonks credentials missing: SPORTMONKS_API_KEY required.")
    base = os.getenv("LIVE_SCORE_BASE_URL", "").strip() or "https://api.sportmonks.com/v3/football/fixtures"
    payload = _request_json(base, params={"api_token": key, "include": "scores;state;participants"})
    results = []
    for item in _items(payload, "data"):
        raw_id = item.get("id")
        match_no = _map_match_no("sportmonks", raw_id, item, fixtures_df)
        scores = item.get("scores") if isinstance(item.get("scores"), list) else []
        home_score = away_score = None
        for score in scores:
            desc = str(score.get("description", "")).upper()
            participant = str(score.get("score", {}).get("participant", "")).lower()
            goals = score.get("score", {}).get("goals")
            if "CURRENT" not in desc and "FT" not in desc:
                continue
            if participant == "home":
                home_score = goals
            elif participant == "away":
                away_score = goals
        state = item.get("state") if isinstance(item.get("state"), dict) else {}
        results.append(_result("sportmonks", match_no, raw_id, home_score, away_score, state.get("short_name") or item.get("status"), item.get("minute"), "Sportmonks fixtures response"))
    return [item for item in results if item is not None]


def _fetch_api_football(fixtures_df: Any) -> list[LiveMatchResult]:
    key = os.getenv("API_FOOTBALL_KEY", "").strip()
    if not key:
        raise RuntimeError("api_football credentials missing: API_FOOTBALL_KEY required.")
    host = os.getenv("API_FOOTBALL_HOST", "v3.football.api-sports.io").strip() or "v3.football.api-sports.io"
    base = os.getenv("LIVE_SCORE_BASE_URL", "").strip() or f"https://{host}/fixtures"
    params = {}
    if os.getenv("LIVE_SCORE_COMPETITION_ID", "").strip():
        params["league"] = os.getenv("LIVE_SCORE_COMPETITION_ID", "").strip()
    payload = _request_json(base, headers={"x-apisports-key": key, "x-rapidapi-host": host}, params=params)
    results = []
    for item in _items(payload, "response"):
        fixture = item.get("fixture") if isinstance(item.get("fixture"), dict) else {}
        goals = item.get("goals") if isinstance(item.get("goals"), dict) else {}
        status = fixture.get("status") if isinstance(fixture.get("status"), dict) else {}
        raw_id = fixture.get("id")
        match_no = _map_match_no("api_football", raw_id, item, fixtures_df)
        results.append(_result("api_football", match_no, raw_id, goals.get("home"), goals.get("away"), status.get("short"), status.get("elapsed"), "API-Football fixtures response"))
    return [item for item in results if item is not None]


API_FETCHERS = {
    "live_score_api": _fetch_live_score_api,
    "football_data": _fetch_football_data,
    "sportmonks": _fetch_sportmonks,
    "api_football": _fetch_api_football,
}


def fetch_live_results(fixtures_df: Any = None) -> list[LiveMatchResult]:
    provider = os.getenv("LIVE_SCORE_PROVIDER", "verified_cache").strip().lower() or "verified_cache"
    if provider not in SUPPORTED_PROVIDERS:
        _set_status(False, provider, "OFF", [f"Unsupported live score provider '{provider}'."])
        provider = "verified_cache"

    if provider == "none":
        _set_status(False, "none", "OFF", ["Live scores disabled: LIVE_SCORE_PROVIDER=none."])
        return []

    if provider == "verified_cache":
        try:
            results = _verified_cache_results()
            last_sync = results[0].synced_at_utc if results else _utc_now_iso()
            _set_status(False, "verified_cache", "OFF — using verified public results cache", [], last_sync)
            return results
        except Exception as exc:
            _set_status(False, "verified_cache", "OFF", [f"Verified public results cache unavailable: {type(exc).__name__}."])
            return []

    if provider == "local_json":
        try:
            results = _local_json_results()
            _set_status(False, "local_json", "OFF — using local override/cache", [], results[0].synced_at_utc if results else _utc_now_iso())
            return results
        except Exception as exc:
            _set_status(False, "local_json", "OFF — using local override/cache", [f"local_json override/cache unavailable: {type(exc).__name__}."])
            return []

    warnings: list[str] = []
    try:
        results = API_FETCHERS[provider](fixtures_df)
        _set_status(True, provider, "ON — provider connected", [], results[0].synced_at_utc if results else _utc_now_iso())
        return results
    except Exception as exc:
        warnings.append(f"{provider} unavailable: {type(exc).__name__}. Falling back to verified public results cache.")
        try:
            results = _verified_cache_results("fallback after live provider failure")
            _set_status(False, provider, "OFF — using verified public results cache", warnings, results[0].synced_at_utc if results else _utc_now_iso())
            return results
        except Exception as cache_exc:
            warnings.append(f"Verified public results cache unavailable: {type(cache_exc).__name__}.")
            _set_status(False, provider, "OFF", warnings)
            return []

# PHASE_1_42_VERIFIED_RESULTS_CACHE_OVERRIDE
# Deterministic verified public completed-results cache.
# Contract: fetch_live_results(...) -> list[LiveMatchResult]
try:
    _PHASE_142_PREVIOUS_FETCH_LIVE_RESULTS = fetch_live_results  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    _PHASE_142_PREVIOUS_FETCH_LIVE_RESULTS = None


_PHASE_142_VERIFIED_COMPLETED_RESULTS = [
    LiveMatchResult(1, 2, 0, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Mexico 2-0 South Africa"),
    LiveMatchResult(2, 2, 1, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Korea Republic 2-1 Czechia"),
    LiveMatchResult(3, 1, 1, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Canada 1-1 Bosnia & Herzegovina"),
    LiveMatchResult(4, 4, 1, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: United States 4-1 Paraguay"),
    LiveMatchResult(5, 1, 1, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Qatar 1-1 Switzerland"),
    LiveMatchResult(6, 1, 1, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Brazil 1-1 Morocco"),
    LiveMatchResult(7, 0, 1, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Haiti 0-1 Scotland"),
    LiveMatchResult(8, 2, 0, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Australia 2-0 Turkey"),
    LiveMatchResult(9, 7, 1, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Germany 7-1 Curacao"),
    LiveMatchResult(10, 2, 2, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Netherlands 2-2 Japan"),
    LiveMatchResult(11, 1, 0, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Ivory Coast 1-0 Ecuador"),
    LiveMatchResult(12, 5, 1, "FT", None, "verified public results cache", "2026-06-15T07:55:01Z", "verified", "", "verified public results cache: Sweden 5-1 Tunisia"),
]


def fetch_live_results(fixtures_df: Any = None) -> list[LiveMatchResult]:  # type: ignore[no-redef]
    """Return previous live results plus Phase 1.42 verified completed cache.

    This keeps the original adapter contract and avoids dict/DataFrame payloads.
    Existing provider rows are preserved, but verified public cache wins by match_no.
    """
    base: list[LiveMatchResult] = []

    if _PHASE_142_PREVIOUS_FETCH_LIVE_RESULTS is not None:
        try:
            previous = _PHASE_142_PREVIOUS_FETCH_LIVE_RESULTS(fixtures_df)
            if previous:
                base = list(previous)
        except Exception:
            base = []

    merged: dict[int, LiveMatchResult] = {}
    for result in base:
        try:
            merged[int(result.match_no)] = result
        except Exception:
            continue

    for result in _PHASE_142_VERIFIED_COMPLETED_RESULTS:
        merged[int(result.match_no)] = result

    return [merged[k] for k in sorted(merged)]
