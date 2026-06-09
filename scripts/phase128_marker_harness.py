from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
README = ROOT / "README.md"
RELEASES = ROOT / "releases" / "final"
OUT = RELEASES / "PHASE_1_28_MARKER_EXTRACT.json"

TEXT_FILES = [APP, README]
TEXT_FILES += sorted((ROOT / "releases" / "final").glob("*.md"))
TEXT_FILES += [p for p in sorted((ROOT / "scripts").glob("*.py")) if p.name != "phase128_marker_harness.py"]

REQUIRED_MARKERS = {
    "product_name": r"AI Bracket War Room 2026",
    "unofficial": r"Unofficial|unofficial|fan-made",
    "teams_48": r"\b48\b",
    "groups_12": r"\b12\b",
    "matches_104": r"\b104\b",
    "combos_495": r"\b495\b",
    "friends_league": r"Friends League",
    "ai_scout": r"AI Scout",
    "tactical_slip": r"Tactical Slip|tactical slip",
    "json_contract": r"JSON Contract|Judge JSON|json contract",
    "phase128": r"PHASE 1\.28|Phase 1\.28|phase128",
    "contrast_header_semantic": r"\.gradio-dataframe th|\.gradio-container th\.header-cell|\.gradio-container \.ag-header-cell",
    "contrast_nested_semantic": r"\.gradio-dataframe th \*|\.gradio-container th\.header-cell \*|\.gradio-container \.header-cell \*|\.gradio-container \.ag-header-cell-text",
    "contrast_svelte_semantic": r"header-cell\.svelte-1d6xqpb|\.svelte-1d6xqpb\.header-cell",
    "contrast_dark_text_fill": r"-webkit-text-fill-color: #111827|-webkit-text-fill-color: #09090b",
}

FORBIDDEN_MARKERS = {
    "official_affiliation_claim": r"officially affiliated|official partner|endorsed by FIFA|FIFA-approved",
    "unsafe_money_staking_language": r"(?<!no )(?<!No )\bbetting\b|\bodds\b|\bsportsbook\b|\bwager\b|\bwagering\b|\bparlay\b",
}

def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")

combined = "\n\n".join(
    f"\n--- {p.relative_to(ROOT)} ---\n{read(p)}"
    for p in TEXT_FILES
    if p.exists()
)

required = {}
for name, pattern in REQUIRED_MARKERS.items():
    matches = re.findall(pattern, combined, flags=re.IGNORECASE)
    required[name] = {"pass": bool(matches), "count": len(matches), "pattern": pattern}

forbidden = {}
for name, pattern in FORBIDDEN_MARKERS.items():
    matches = re.findall(pattern, combined, flags=re.IGNORECASE)
    forbidden[name] = {"pass": not bool(matches), "count": len(matches), "pattern": pattern}

result = {
    "phase": "PHASE_1_28_PRODUCTIZED_ONBOARDING_DEMO_PATH_CLARITY",
    "required": required,
    "forbidden": forbidden,
    "files_scanned": [str(p.relative_to(ROOT)) for p in TEXT_FILES if p.exists()],
}

RELEASES.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

missing = [k for k, v in required.items() if not v["pass"]]
violations = [k for k, v in forbidden.items() if not v["pass"]]

if missing or violations:
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(f"PHASE_1_28_MARKER_HARNESS_FAIL missing={missing} violations={violations}")

print("PHASE_1_28_MARKER_HARNESS_PASS")
print(f"Report: {OUT.relative_to(ROOT)}")
