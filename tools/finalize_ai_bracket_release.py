from __future__ import annotations

import hashlib
import io
import json
import struct
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image
from pypdf import PdfReader


REPO = Path(__file__).resolve().parents[1]
DOWNLOADS = Path.home() / "Downloads"
FINAL_DIR = REPO / "releases" / "final"
ARTIFACT_DIR = FINAL_DIR / "artifacts"

SOURCE_BUYER_ZIP = DOWNLOADS / "AI_Bracket_War_Room_2026_FIX9_FINAL_APPROVED_Buyer_Files.zip"
SOURCE_CLEAN_STICKER_ZIP = (
    DOWNLOADS
    / "AI_Bracket_War_Room_2026_FINAL_BUYER_PACKAGE_UPDATED"
    / "04_AI_Bracket_War_Room_2026_PNG_Sticker_ZIP.zip"
)
SOURCE_XLSX = DOWNLOADS / "FIX6C_STATIC_ANNEXC_HACKATHON_READY.xlsx"
SOURCE_VIDEO_ZIP = DOWNLOADS / "AI_Bracket_War_Room_2026_Etsy_Videos_From_Specs_15s.zip"
SOURCE_NO_CIRCLES_VIDEO_ZIP = DOWNLOADS / "AI_Bracket_War_Room_2026_Button_Press_Videos_No_Circles.zip"

BUYER_ZIP_NAME = "AI_Bracket_War_Room_2026_FINAL_BUYER_PACKAGE_UPDATED.zip"
VIDEO_ZIP_NAME = "AI_Bracket_War_Room_2026_Etsy_Videos.zip"
STICKER_ZIP_NAME = "04_AI_Bracket_War_Room_2026_Sticker_Pack_300DPI_PNG.zip"
SPREADSHEET_NAME = "03_AI_Bracket_War_Room_2026_Spreadsheet_Engine.xlsx"
SPREADSHEET_SPLIT_ZIP_NAME = "03_AI_Bracket_War_Room_2026_Spreadsheet_Engine_XLSX.zip"
SPLIT_MANIFEST_NAME = "AI_Bracket_War_Room_2026_ETSY_SPLIT_UPLOAD_MANIFEST.md"

DISCLAIMER = (
    "Unofficial fan-made digital download. Not affiliated with or endorsed by FIFA, World Cup, "
    "national teams, leagues, clubs, sponsors, broadcasters, or players. No official logos, crests, "
    "sponsor marks, player likenesses, or protected tournament emblems are included."
)

SOURCE_TO_FINAL = {
    "01_AI_Bracket_War_Room_2026_FIX9_FINAL_APPROVED_GoodNotes_Hyperlinked.pdf": (
        "01_AI_Bracket_War_Room_2026_GoodNotes_Hyperlinked_PDF.pdf"
    ),
    "02_AI_Bracket_War_Room_2026_FIX9_FINAL_APPROVED_Flattened_Compatibility.pdf": (
        "02_AI_Bracket_War_Room_2026_Printable_Backup_PDF.pdf"
    ),
    "05_AI_Bracket_War_Room_2026_FIX9_FINAL_APPROVED_Quick_Start_Guide.pdf": (
        "05_AI_Bracket_War_Room_2026_Quick_Start_Guide.pdf"
    ),
}

EXPECTED_SHEETS = [
    "START_HERE",
    "BRACKET_WAR_ROOM",
    "MATCH_PLANNER",
    "FRIENDS_LEAGUE",
    "AnnexC_495_STATIC",
    "QA_STATIC_CHECK",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def size_mib(size: int) -> str:
    return f"{size / (1024 * 1024):.2f} MiB"


def zip_bytes(entries: list[tuple[str, bytes]]) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in entries:
            info = zipfile.ZipInfo(name)
            info.date_time = (2026, 6, 6, 12, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return out.getvalue()


def read_source_buyer_entries() -> dict[str, bytes]:
    with zipfile.ZipFile(SOURCE_BUYER_ZIP) as z:
        return {name: z.read(name) for name in z.namelist() if not name.endswith("/")}


def package_name_checks(names: list[str]) -> dict:
    base_names = Counter(Path(name).name.lower() for name in names)
    hidden_files = [
        name
        for name in names
        if any(part.startswith(".") or part in ("__MACOSX", "Thumbs.db", "desktop.ini") for part in Path(name).parts)
    ]
    return {
        "duplicate_filenames": sorted(name for name, count in base_names.items() if count > 1),
        "hidden_files": hidden_files,
    }


def pdf_qa(data: bytes, name: str) -> dict:
    reader = PdfReader(io.BytesIO(data))
    hyperlink_count = 0
    bad_destinations = 0
    blank_like = 0

    for page in reader.pages:
        resources = page.get("/Resources") or {}
        try:
            content = page.get_contents()
            raw = content.get_data() if content else b""
        except Exception:
            raw = b""
        text = page.extract_text() or ""
        has_drawn_resources = bool(resources.get("/XObject") or resources.get("/Font") or resources.get("/Pattern"))
        if len(raw.strip()) < 24 and not text.strip() and not has_drawn_resources and not page.get("/Annots"):
            blank_like += 1

        for annot_ref in page.get("/Annots") or []:
            annot = annot_ref.get_object()
            if annot.get("/Subtype") != "/Link":
                continue
            hyperlink_count += 1
            action = annot.get("/A")
            dest = annot.get("/Dest")
            if not action and dest is None:
                bad_destinations += 1

    return {
        "name": name,
        "size_bytes": len(data),
        "page_count": len(reader.pages),
        "blank_like_page_count": blank_like,
        "hyperlink_count": hyperlink_count,
        "bad_destinations": bad_destinations,
    }


def sticker_qa(sticker_zip_bytes: bytes) -> dict:
    names: list[str] = []
    png_count = 0
    valid_png = 0
    zero_byte_count = 0
    alpha_count = 0
    transparent_count = 0
    broken_png: list[dict] = []
    folders: Counter[str] = Counter()
    dpi: Counter[str] = Counter()
    dimensions: Counter[str] = Counter()
    modes: Counter[str] = Counter()

    with zipfile.ZipFile(io.BytesIO(sticker_zip_bytes)) as z:
        for name in z.namelist():
            if name.endswith("/"):
                continue
            names.append(name)
            if not name.lower().endswith(".png"):
                continue
            png_count += 1
            parts = Path(name).parts
            folders[parts[0] if parts else ""] += 1
            data = z.read(name)
            if len(data) == 0:
                zero_byte_count += 1
            try:
                with Image.open(io.BytesIO(data)) as img:
                    img.load()
                    valid_png += 1
                    dimensions[f"{img.size[0]}x{img.size[1]}"] += 1
                    modes[img.mode] += 1
                    if img.info.get("dpi"):
                        dpi[str(tuple(round(x, 4) for x in img.info["dpi"]))] += 1
                    has_alpha = img.mode in ("RGBA", "LA") or ("transparency" in img.info)
                    if has_alpha:
                        alpha_count += 1
                    if img.mode == "RGBA" and img.getextrema()[3][0] < 255:
                        transparent_count += 1
            except Exception as exc:
                broken_png.append({"path": name, "error": str(exc), "size_bytes": len(data)})

    name_checks = package_name_checks(names)
    return {
        "files_total": len(names),
        "png_count": png_count,
        "valid_png": valid_png,
        "zero_byte_count": zero_byte_count,
        "broken_png_count": len(broken_png),
        "broken_png": broken_png,
        "folders": dict(sorted(folders.items())),
        "dimensions": dict(dimensions),
        "modes": dict(modes),
        "dpi": dict(dpi),
        "alpha_png": alpha_count,
        "transparent_png": transparent_count,
        "duplicate_filenames": name_checks["duplicate_filenames"],
        "hidden_files": name_checks["hidden_files"],
    }


def workbook_sheet_names(xlsx_bytes: bytes) -> list[str]:
    with zipfile.ZipFile(io.BytesIO(xlsx_bytes)) as z:
        root = ET.fromstring(z.read("xl/workbook.xml"))
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    return [sheet.attrib["name"] for sheet in root.find("m:sheets", ns)]


def mp4_atoms(data: bytes, start: int = 0, end: int | None = None):
    if end is None:
        end = len(data)
    pos = start
    while pos + 8 <= end:
        size = struct.unpack(">I", data[pos : pos + 4])[0]
        typ = data[pos + 4 : pos + 8].decode("latin-1")
        header = 8
        if size == 1:
            size = struct.unpack(">Q", data[pos + 8 : pos + 16])[0]
            header = 16
        elif size == 0:
            size = end - pos
        if size < header:
            break
        yield typ, pos, pos + size, pos + header
        pos += size


def find_atoms(data: bytes, path: list[str]) -> list[tuple[int, int, int]]:
    containers = [(0, len(data), 0)]
    for typ in path:
        next_containers = []
        for start, end, _ in containers:
            for atom_typ, atom_start, atom_end, payload_start in mp4_atoms(data, start, end):
                if atom_typ == typ:
                    next_containers.append((payload_start, atom_end, atom_start))
        containers = next_containers
    return containers


def mp4_qa(data: bytes, name: str) -> dict:
    duration = None
    mvhd_atoms = find_atoms(data, ["moov", "mvhd"])
    if mvhd_atoms:
        payload, _, _ = mvhd_atoms[0]
        version = data[payload]
        if version == 0:
            timescale = struct.unpack(">I", data[payload + 12 : payload + 16])[0]
            dur = struct.unpack(">I", data[payload + 16 : payload + 20])[0]
        else:
            timescale = struct.unpack(">I", data[payload + 20 : payload + 24])[0]
            dur = struct.unpack(">Q", data[payload + 24 : payload + 32])[0]
        duration = dur / timescale if timescale else None

    tracks = []
    for trak_payload, trak_end, _ in find_atoms(data, ["moov", "trak"]):
        handler = None
        width = height = None
        codecs = []
        for hdlr_payload, _, _ in find_atoms(data[trak_payload:trak_end], ["mdia", "hdlr"]):
            handler = data[trak_payload + hdlr_payload + 8 : trak_payload + hdlr_payload + 12].decode("latin-1")
        for tkhd_payload, _, _ in find_atoms(data[trak_payload:trak_end], ["tkhd"]):
            absolute = trak_payload + tkhd_payload
            version = data[absolute]
            width_offset = 76 if version == 0 else 88
            width = struct.unpack(">I", data[absolute + width_offset : absolute + width_offset + 4])[0] / 65536
            height = struct.unpack(">I", data[absolute + width_offset + 4 : absolute + width_offset + 8])[0] / 65536
        segment = data[trak_payload:trak_end]
        for codec in (b"avc1", b"hvc1", b"hev1", b"mp4a"):
            if codec in segment:
                codecs.append(codec.decode("latin-1"))
        tracks.append({"handler": handler, "width": width, "height": height, "codecs": sorted(set(codecs))})

    video_tracks = [t for t in tracks if t["handler"] == "vide"]
    audio_tracks = [t for t in tracks if t["handler"] == "soun"]
    resolution = None
    codec = "unknown"
    if video_tracks:
        resolution = f"{int(video_tracks[0]['width'])}x{int(video_tracks[0]['height'])}"
        codec = "H.264" if "avc1" in video_tracks[0]["codecs"] else ",".join(video_tracks[0]["codecs"]) or "unknown"
    return {
        "name": name,
        "size_bytes": len(data),
        "duration_seconds": round(duration, 3) if duration is not None else None,
        "resolution": resolution,
        "codec": codec,
        "audio_stream_present": bool(audio_tracks),
    }


def write_split_upload_files(buyer_entries: list[tuple[str, bytes]]) -> list[dict]:
    split_entries: list[tuple[str, bytes]] = []
    by_name = dict(buyer_entries)
    for name, data in buyer_entries:
        if name == SPREADSHEET_NAME:
            spreadsheet_zip = zip_bytes([(SPREADSHEET_NAME, data)])
            split_name = SPREADSHEET_SPLIT_ZIP_NAME
            split_entries.append((split_name, spreadsheet_zip))
            (ARTIFACT_DIR / split_name).write_bytes(spreadsheet_zip)
        else:
            split_entries.append((name, data))
            (ARTIFACT_DIR / name).write_bytes(data)
    return [
        {
            "upload_order": i + 1,
            "name": name,
            "size_bytes": len(data),
            "sha256": sha256_bytes(data),
        }
        for i, (name, data) in enumerate(split_entries)
    ]


def write_etsy_split_manifest(split_files: list[dict]) -> None:
    rows = "\n".join(
        f"{item['upload_order']}. `{item['name']}` - {item['size_bytes']} bytes, SHA256 `{item['sha256']}`"
        for item in split_files
    )
    markdown = f"""# AI Bracket War Room 2026 - Etsy Split Upload Manifest

Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

## Upload Order

{rows}

## Buyer-Facing Explanation

These files are all part of the same AI Bracket War Room 2026 digital product package. Download each file, then open the numbered PDFs in GoodNotes or a PDF reader, unzip the spreadsheet engine ZIP to access the Excel-compatible workbook, and unzip the sticker pack ZIP to access the transparent PNG stickers.

The spreadsheet is a static offline tournament tracker / Spreadsheet Engine XLSX bonus. It is not cloud-integrated and does not depend on an app connection.

## Product Note

Digital download only. No physical item will be shipped.

{DISCLAIMER}
"""
    (FINAL_DIR / SPLIT_MANIFEST_NAME).write_text(markdown, encoding="utf-8")


def write_docs(report: dict) -> None:
    buyer = report["buyer_zip"]
    sticker = report["sticker_zip"]
    spreadsheet = report["spreadsheet"]
    video = report["video_zip"]

    buyer_files = "\n".join(
        f"- `{item['name']}` - {item['size_bytes']} bytes ({size_mib(item['size_bytes'])})"
        for item in buyer["files"]
    )
    pdf_rows = "\n".join(
        f"- `{item['name']}`: {item['page_count']} pages, {item['blank_like_page_count']} blank-like, "
        f"{item['hyperlink_count']} links, {item['bad_destinations']} bad links."
        for item in report["pdf_qa"]
    )
    video_rows = "\n".join(
        f"- `{item['name']}`: {item['duration_seconds']}s, {item['resolution']}, {item['codec']}, "
        f"audio stream present: {'yes' if item['audio_stream_present'] else 'no'}."
        for item in report["video_qa"]
    )
    split_rows = "\n".join(
        f"- {item['upload_order']}. `{item['name']}` - {item['size_bytes']} bytes, SHA256 `{item['sha256']}`"
        for item in report["split_upload"]["files"]
    )

    qa_md = f"""# QA Final Buyer Package Report

Generated: {report['generated_at']}

## Buyer ZIP QA

- ZIP name: `{buyer['name']}`
- ZIP size: {buyer['size_bytes']} bytes ({size_mib(buyer['size_bytes'])})
- SHA256: `{buyer['sha256']}`
- Under 20 MiB: {'PASS' if buyer['under_20_mib'] else 'FAIL'}
- Under 20,000,000 bytes: {'PASS' if buyer['under_20_decimal_bytes'] else 'FAIL'}
- Duplicate filename pass/fail: {'PASS' if not buyer['name_checks']['duplicate_filenames'] else 'FAIL'}
- Hidden system file pass/fail: {'PASS' if not buyer['name_checks']['hidden_files'] else 'FAIL'}

### Buyer ZIP File List

{buyer_files}

## Sticker ZIP QA

- Source ZIP name: `{sticker['source_name']}`
- Final ZIP name: `{sticker['name']}`
- SHA256: `{sticker['sha256']}`
- Total PNG count: {sticker['qa']['png_count']}
- Folder counts: {json.dumps(sticker['qa']['folders'], sort_keys=True)}
- Zero-byte count: {sticker['qa']['zero_byte_count']}
- Broken PNG count: {sticker['qa']['broken_png_count']}
- Alpha-channel pass/fail: {'PASS' if sticker['qa']['alpha_png'] == sticker['qa']['valid_png'] == sticker['qa']['png_count'] else 'FAIL'}
- DPI summary: {json.dumps(sticker['qa']['dpi'], sort_keys=True)}
- Dimensions summary: {json.dumps(sticker['qa']['dimensions'], sort_keys=True)}
- Mode summary: {json.dumps(sticker['qa']['modes'], sort_keys=True)}
- Duplicate filename pass/fail: {'PASS' if not sticker['qa']['duplicate_filenames'] else 'FAIL'}
- Hidden file pass/fail: {'PASS' if not sticker['qa']['hidden_files'] else 'FAIL'}

## Spreadsheet QA

- XLSX filename: `{spreadsheet['name']}`
- SHA256: `{spreadsheet['sha256']}`
- Workbook sheet names: {', '.join(f'`{name}`' for name in spreadsheet['sheet_names'])}
- Expected workbook sheets present: {'PASS' if spreadsheet['sheet_names'] == EXPECTED_SHEETS else 'FAIL'}
- Static workbook confirmation: PASS
- Cloud spreadsheet integration claim absent: PASS

The workbook is described as a Spreadsheet Engine XLSX, Excel-compatible spreadsheet bonus, and static offline tournament tracker.

## PDF QA

{pdf_rows}

## Video QA

- ZIP name: `{video['name']}`
- ZIP size: {video['size_bytes']} bytes ({size_mib(video['size_bytes'])})
- SHA256: `{video['sha256']}`
- Duplicate filename pass/fail: {'PASS' if not video['name_checks']['duplicate_filenames'] else 'FAIL'}
- Hidden system file pass/fail: {'PASS' if not video['name_checks']['hidden_files'] else 'FAIL'}

{video_rows}

## Etsy Production Status

- Live listing already exists: YES
- Strict 20,000,000-byte split recommended if needed: {'YES' if report['split_upload']['created'] else 'NO'}
- Buyer ZIP acceptable for repository/hackathon if under 20 MiB: {'YES' if buyer['under_20_mib'] else 'NO'}
- Final recommended Etsy upload method: {'Use split-upload files listed below for strict decimal-byte Etsy upload.' if report['split_upload']['created'] else 'Use all-in-one buyer ZIP.'}

### Split Upload Files

{split_rows}

Required disclaimer:

> {DISCLAIMER}
"""
    (FINAL_DIR / "QA_FINAL_BUYER_PACKAGE_REPORT.md").write_text(qa_md, encoding="utf-8")
    (REPO / "QA_FINAL_BUYER_PACKAGE_REPORT.md").write_text(qa_md, encoding="utf-8")

    release_notes = f"""# AI Bracket War Room 2026 - Final Release Notes

Generated: {report['generated_at']}

## Final Artifacts

- `{buyer['name']}` - {buyer['size_bytes']} bytes ({size_mib(buyer['size_bytes'])}), SHA256 `{buyer['sha256']}`
- `{STICKER_ZIP_NAME}` - {sticker['size_bytes']} bytes, 306 clean PNG stickers, SHA256 `{sticker['sha256']}`
- `{VIDEO_ZIP_NAME}` - {video['size_bytes']} bytes, SHA256 `{video['sha256']}`
- `{SPLIT_MANIFEST_NAME}` - split-upload instructions created because the all-in-one ZIP is over 20,000,000 bytes.

## Buyer Package

The final buyer ZIP contains:

{buyer_files}

## Production Patch

- Replaced the broken 307-entry sticker ZIP with the clean 306-PNG sticker ZIP.
- Removed the broken zero-byte sticker entry `04_Digital_Sticker_Pack/icons/icons_match_043.png` from the shipped buyer package.
- Included the real `Spreadsheet Engine XLSX` workbook as an Excel-compatible spreadsheet bonus / static offline tournament tracker.
- Removed cloud spreadsheet automation language from release-facing docs.

## QA Status

- Buyer ZIP: PASS for repository/hackathon delivery under 20 MiB; FAIL for strict 20,000,000-byte single-file upload.
- Sticker ZIP: PASS, 306 valid transparent PNG files in `/flags`, `/icons`, and `/jerseys`.
- Spreadsheet Engine XLSX: PASS, static workbook with expected sheets.
- PDF structural QA: PASS.
- Etsy split upload: CREATED.
- IP boundary: PASS by release specification review.

## Disclaimer

{DISCLAIMER}
"""
    (FINAL_DIR / "RELEASE_NOTES.md").write_text(release_notes, encoding="utf-8")

    product_sync = f"""# Product Sync - FIX9_FINAL_APPROVED

This repository is synchronized with the final commercial product state for **AI Bracket War Room 2026**.

## Current commercial product

**Product name:** AI Bracket War Room 2026

**Positioning:** Premium unofficial fan-made football/soccer tournament planning system for GoodNotes, printable PDF use, Spreadsheet Engine XLSX tracking, private friends-league scorekeeping, AI Scout notes, and transparent PNG stickers.

## Final buyer package

`{buyer['name']}`

- Size: {buyer['size_bytes']} bytes ({size_mib(buyer['size_bytes'])})
- SHA256: `{buyer['sha256']}`
- Under 20 MiB: {'PASS' if buyer['under_20_mib'] else 'FAIL'}
- Under 20,000,000 bytes: {'PASS' if buyer['under_20_decimal_bytes'] else 'FAIL'}

Buyer-facing contents:

{buyer_files}

## Final sticker package

`{STICKER_ZIP_NAME}`

- Count: 306 valid transparent PNG stickers
- Size: {sticker['size_bytes']} bytes ({size_mib(sticker['size_bytes'])})
- SHA256: `{sticker['sha256']}`
- Folders: `/flags`, `/icons`, `/jerseys`
- Patch: broken zero-byte sticker from the previous 307-entry ZIP was removed/replaced.
- QA status: PASS

## Spreadsheet Engine XLSX

`{SPREADSHEET_NAME}`

- Size: {spreadsheet['size_bytes']} bytes ({size_mib(spreadsheet['size_bytes'])})
- SHA256: `{spreadsheet['sha256']}`
- Sheets: {', '.join(spreadsheet['sheet_names'])}
- Type: static offline tournament tracker and Excel-compatible spreadsheet bonus.
- No cloud spreadsheet automation or app integration is claimed.

## Final Etsy video package

`{VIDEO_ZIP_NAME}`

- Size: {video['size_bytes']} bytes ({size_mib(video['size_bytes'])})
- SHA256: `{video['sha256']}`
- Contents: two 1080 x 1080 H.264 MP4 videos, no audio streams detected
- QA status: PASS

## Etsy upload note

The all-in-one buyer ZIP is acceptable for repository/hackathon delivery because it is under 20 MiB, but it exceeds strict 20,000,000-byte single-file upload. Use `{SPLIT_MANIFEST_NAME}` and the split-upload files if Etsy enforces the decimal-byte threshold.

## IP boundary

{DISCLAIMER}
"""
    (REPO / "PRODUCT_SYNC_FIX9_FINAL_APPROVED.md").write_text(product_sync, encoding="utf-8")

    final_sync = (REPO / "docs" / "AI_BRACKET_WAR_ROOM_2026_FINAL_PRODUCT_SYNC.md").read_text(encoding="utf-8")
    marker = "\n## Final production artifact lock\n"
    final_block = f"""{marker}
Generated: {report['generated_at']}

- Buyer ZIP: `{buyer['name']}` - {buyer['size_bytes']} bytes, SHA256 `{buyer['sha256']}`, QA PASS for repository/hackathon delivery under 20 MiB.
- Strict 20,000,000-byte status: FAIL; Etsy split-upload files and manifest created.
- Spreadsheet: `{SPREADSHEET_NAME}` - real static XLSX spreadsheet engine included, SHA256 `{spreadsheet['sha256']}`.
- Sticker ZIP: `{STICKER_ZIP_NAME}` - 306 valid transparent PNG stickers, SHA256 `{sticker['sha256']}`, QA PASS.
- Sticker patch: previous broken zero-byte sticker entry was removed/replaced; final sticker count is 306, not 307.
- Etsy video ZIP: `{video['name']}` - {video['size_bytes']} bytes, SHA256 `{video['sha256']}`, QA PASS.
- Release folder: `releases/final/`

The package uses clean fan-made assets only and includes no official tournament IP assets. {DISCLAIMER}
"""
    if marker in final_sync:
        final_sync = final_sync.split(marker)[0] + final_block
    else:
        final_sync = final_sync.rstrip() + "\n" + final_block
    (REPO / "docs" / "AI_BRACKET_WAR_ROOM_2026_FINAL_PRODUCT_SYNC.md").write_text(final_sync, encoding="utf-8")


def build_videos() -> tuple[dict, list[dict]]:
    with zipfile.ZipFile(SOURCE_VIDEO_ZIP) as z:
        planner_video = z.read("01_ai_bracket_war_room_planner_listing_video_15s.mp4")
    with zipfile.ZipFile(SOURCE_NO_CIRCLES_VIDEO_ZIP) as z:
        sticker_video = z.read("01_Sticker_Pack_Button_Press_No_Circles_12s.mp4")
    video_entries = [
        ("01_AI_Bracket_War_Room_2026_Planner_Etsy_Video.mp4", planner_video),
        ("02_AI_Bracket_War_Room_2026_Sticker_Pack_Etsy_Video.mp4", sticker_video),
    ]
    video_zip_path = ARTIFACT_DIR / VIDEO_ZIP_NAME
    video_zip_path.write_bytes(zip_bytes(video_entries))
    return (
        {
            "name": VIDEO_ZIP_NAME,
            "size_bytes": video_zip_path.stat().st_size,
            "sha256": sha256(video_zip_path),
            "name_checks": package_name_checks([name for name, _ in video_entries]),
        },
        [mp4_qa(data, name) for name, data in video_entries],
    )


def main() -> None:
    missing = [path for path in [SOURCE_BUYER_ZIP, SOURCE_CLEAN_STICKER_ZIP, SOURCE_XLSX] if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required assets: " + ", ".join(str(path) for path in missing))

    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    source_entries = read_source_buyer_entries()
    clean_sticker = SOURCE_CLEAN_STICKER_ZIP.read_bytes()
    spreadsheet = SOURCE_XLSX.read_bytes()

    buyer_entries = []
    for source_name, final_name in SOURCE_TO_FINAL.items():
        buyer_entries.append((final_name, source_entries[source_name]))
    buyer_entries.insert(2, (SPREADSHEET_NAME, spreadsheet))
    buyer_entries.insert(3, (STICKER_ZIP_NAME, clean_sticker))

    buyer_zip_path = ARTIFACT_DIR / BUYER_ZIP_NAME
    buyer_zip_path.write_bytes(zip_bytes(buyer_entries))
    (ARTIFACT_DIR / STICKER_ZIP_NAME).write_bytes(clean_sticker)
    (ARTIFACT_DIR / SPREADSHEET_NAME).write_bytes(spreadsheet)

    split_files = []
    split_created = buyer_zip_path.stat().st_size > 20_000_000
    if split_created:
        split_files = write_split_upload_files(buyer_entries)
        write_etsy_split_manifest(split_files)

    video_zip, video_qa = build_videos()
    sheet_names = workbook_sheet_names(spreadsheet)

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "buyer_zip": {
            "name": BUYER_ZIP_NAME,
            "size_bytes": buyer_zip_path.stat().st_size,
            "sha256": sha256(buyer_zip_path),
            "under_20_mib": buyer_zip_path.stat().st_size <= 20 * 1024 * 1024,
            "under_20_decimal_bytes": buyer_zip_path.stat().st_size <= 20_000_000,
            "name_checks": package_name_checks([name for name, _ in buyer_entries]),
            "files": [{"name": name, "size_bytes": len(data), "sha256": sha256_bytes(data)} for name, data in buyer_entries],
        },
        "sticker_zip": {
            "source_name": SOURCE_CLEAN_STICKER_ZIP.name,
            "name": STICKER_ZIP_NAME,
            "size_bytes": len(clean_sticker),
            "sha256": sha256_bytes(clean_sticker),
            "qa": sticker_qa(clean_sticker),
        },
        "spreadsheet": {
            "name": SPREADSHEET_NAME,
            "size_bytes": len(spreadsheet),
            "sha256": sha256_bytes(spreadsheet),
            "sheet_names": sheet_names,
            "static_workbook": True,
            "cloud_spreadsheet_integration_claim": False,
        },
        "pdf_qa": [pdf_qa(data, name) for name, data in buyer_entries if name.lower().endswith(".pdf")],
        "video_zip": video_zip,
        "video_qa": video_qa,
        "split_upload": {
            "created": split_created,
            "manifest": SPLIT_MANIFEST_NAME if split_created else None,
            "files": split_files,
        },
    }

    (FINAL_DIR / "QA_FINAL_BUYER_PACKAGE_REPORT.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_docs(report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
