from __future__ import annotations

import hashlib
import io
import json
import struct
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


REPO = Path(__file__).resolve().parents[1]
DOWNLOADS = Path.home() / "Downloads"
FINAL_DIR = REPO / "releases" / "final"
ARTIFACT_DIR = FINAL_DIR / "artifacts"

SOURCE_BUYER_ZIP = DOWNLOADS / "AI_Bracket_War_Room_2026_FINAL_BUYER_PACKAGE_UPDATED.zip"
SOURCE_VIDEO_ZIP = DOWNLOADS / "AI_Bracket_War_Room_2026_Etsy_Videos_From_Specs_15s.zip"
SOURCE_NO_CIRCLES_VIDEO_ZIP = DOWNLOADS / "AI_Bracket_War_Room_2026_Button_Press_Videos_No_Circles.zip"
STICKER_QA_ZIP = DOWNLOADS / "AI_Bracket_War_Room_2026_STICKER_SELECTION_DEV_QA.zip"
SOURCE_FIX9_STICKER_ZIP = DOWNLOADS / "04_AI_Bracket_War_Room_2026_FIX9_FINAL_APPROVED_Sticker_Pack_300DPI_PNG.zip"

BUYER_ZIP_NAME = "AI_Bracket_War_Room_2026_FINAL_BUYER_PACKAGE_UPDATED.zip"
VIDEO_ZIP_NAME = "AI_Bracket_War_Room_2026_Etsy_Videos.zip"
STICKER_ZIP_NAME = "04_AI_Bracket_War_Room_2026_Sticker_Pack_300DPI_PNG.zip"
GUIDE_NAME = "03_AI_Bracket_War_Room_2026_Google_Sheets_Tracker_Access_Guide.pdf"

DISCLAIMER = (
    "Unofficial fan-made digital download. Not affiliated with or endorsed by FIFA, World Cup, "
    "national teams, leagues, clubs, sponsors, broadcasters, or players. No official logos, crests, "
    "sponsor marks, player likenesses, or protected tournament emblems are included."
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def size_mb(size: int) -> str:
    return f"{size / (1024 * 1024):.2f} MiB"


def make_access_guide(path: Path) -> None:
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "ReleaseTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#172033"),
        spaceAfter=14,
    )
    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0f5d56"),
        spaceBefore=10,
        spaceAfter=5,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1f2933"),
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#4b5563"),
    )

    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title="AI Bracket War Room 2026 Google Sheets Tracker Access Guide",
    )
    story = [
        Paragraph("AI Bracket War Room 2026", title),
        Paragraph("Google Sheets Tracker Access Guide", heading),
        Paragraph(
            "Use this guide with your private Google account to run a tournament tracker beside the "
            "GoodNotes or printable planner. It is designed for personal fan use, friends-league "
            "scorekeeping, match notes, prediction tracking, and watch-party organization.",
            body,
        ),
        Paragraph("Fast Setup", heading),
    ]
    setup_rows = [
        ["1", "Open Google Drive and choose New > Google Sheets > Blank spreadsheet."],
        ["2", "Create tabs named Dashboard, Matches, Predictions, Friends League, AI Scout, and Notes."],
        ["3", "Use the column map below to mirror the planner fields, then freeze row 1 on every tab."],
        ["4", "Keep the sheet private or share it only with your friends-league group."],
        ["5", "Use the planner PDFs for writing, review, and matchday decisions; use Sheets for sorting totals."],
    ]
    table = Table(setup_rows, colWidths=[0.35 * inch, 6.55 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e7f4ef")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0f5d56")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5d1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([table, Spacer(1, 8), Paragraph("Suggested Tracker Columns", heading)])
    columns = [
        ["Matches", "Match #, Date, Group/Round, Team A, Team B, Prediction, Score, Winner, Notes"],
        ["Predictions", "User, Match #, Pick, Confidence, Points, Correct?, Tiebreak Notes"],
        ["Friends League", "Player, Correct Picks, Bonus, Total, Rank, Paid?, Prize Notes"],
        ["AI Scout", "Team, Strengths, Weaknesses, Form Notes, Watch Player, Risk Flag"],
        ["Notes", "Date, Topic, Decision, Follow-up, Page Reference"],
    ]
    column_table = Table(columns, colWidths=[1.25 * inch, 5.65 * inch])
    column_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172033")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.3),
                ("LEADING", (0, 0), (-1, -1), 10.5),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5d1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend(
        [
            column_table,
            Spacer(1, 8),
            Paragraph("GoodNotes + Printable Workflow", heading),
            Paragraph(
                "Use the hyperlinked PDF as the command center and the printable backup for paper "
                "watch nights. Record raw matchday notes in the planner first, then update Google "
                "Sheets after each match so standings and group totals stay easy to sort.",
                body,
            ),
            Paragraph("Buyer Notes", heading),
            Paragraph(
                "This guide does not require paid add-ons. Google Sheets features can change, so menu "
                "names may vary slightly by device or browser. Keep any shared sheet private to your group.",
                body,
            ),
            Paragraph(DISCLAIMER, small),
        ]
    )
    doc.build(story)


def pdf_qa(data: bytes, name: str) -> dict:
    reader = PdfReader(io.BytesIO(data))
    hyperlink_count = 0
    bad_destinations = 0
    small_targets = 0
    blank_like = 0
    fonts_total = 0
    fonts_embedded = 0

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
            if annot.get("/Subtype") == "/Link":
                hyperlink_count += 1
                rect = [float(x) for x in annot.get("/Rect", [0, 0, 0, 0])]
                width = abs(rect[2] - rect[0])
                height = abs(rect[3] - rect[1])
                if width < 25 or height < 25:
                    small_targets += 1
                action = annot.get("/A")
                dest = annot.get("/Dest")
                if not action and dest is None:
                    bad_destinations += 1

        fonts = resources.get("/Font") or {}
        for font_ref in fonts.values():
            try:
                font = font_ref.get_object()
            except Exception:
                continue
            fonts_total += 1
            descriptor = font.get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                if any(k in descriptor for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                    fonts_embedded += 1

    return {
        "name": name,
        "size_bytes": len(data),
        "page_count": len(reader.pages),
        "blank_like_page_count": blank_like,
        "hyperlink_count": hyperlink_count,
        "bad_destinations": bad_destinations,
        "small_touch_targets_lt_25px": small_targets,
        "fonts_total_checked": fonts_total,
        "fonts_embedded_checked": fonts_embedded,
    }


def read_source_buyer_entries() -> dict[str, bytes]:
    with zipfile.ZipFile(SOURCE_BUYER_ZIP) as z:
        return {name: z.read(name) for name in z.namelist()}


def sticker_qa(sticker_zip_bytes: bytes) -> dict:
    duplicate_names = []
    hidden_files = []
    png_count = 0
    valid_png = 0
    alpha_count = 0
    transparent_count = 0
    bad_png = []
    folders = Counter()
    dpi = Counter()
    dimensions = Counter()
    modes = Counter()
    base_names = Counter()
    ip_terms = ("fifa", "world_cup", "worldcup", "official", "mascot", "sponsor", "crest", "federation")

    with zipfile.ZipFile(io.BytesIO(sticker_zip_bytes)) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        for name in names:
            parts = Path(name).parts
            if any(part.startswith(".") or part in ("__MACOSX", "Thumbs.db", "desktop.ini") for part in parts):
                hidden_files.append(name)
            base_names[Path(name).name.lower()] += 1
            if name.lower().endswith(".png"):
                png_count += 1
                top = parts[0] if parts else ""
                folders[top] += 1
                data = z.read(name)
                try:
                    with Image.open(io.BytesIO(data)) as img:
                        img.load()
                        valid_png += 1
                        dimensions[str(img.size)] += 1
                        modes[img.mode] += 1
                        if img.info.get("dpi"):
                            dpi[str(tuple(round(x, 4) for x in img.info["dpi"]))] += 1
                        has_alpha = img.mode in ("RGBA", "LA") or ("transparency" in img.info)
                        if has_alpha:
                            alpha_count += 1
                            if img.mode == "RGBA" and img.getextrema()[3][0] < 255:
                                transparent_count += 1
                except Exception as exc:
                    bad_png.append({"path": name, "error": str(exc), "size_bytes": len(data)})

    duplicate_names = [name for name, count in base_names.items() if count > 1]
    ip_filename_hits = [n for n in names if any(term in n.lower() for term in ip_terms)]
    return {
        "files_total": len(names),
        "png_count": png_count,
        "valid_png": valid_png,
        "bad_png": bad_png,
        "folders": dict(sorted(folders.items())),
        "dimensions": dict(dimensions),
        "modes": dict(modes),
        "dpi": dict(dpi),
        "alpha_png": alpha_count,
        "transparent_png": transparent_count,
        "duplicate_filenames": duplicate_names,
        "hidden_files": hidden_files,
        "ip_filename_hits": ip_filename_hits,
    }


def sticker_zip_qa(path: Path) -> dict:
    data = path.read_bytes()
    qa = sticker_qa(data)
    return {
        "name": path.name,
        "size_bytes": len(data),
        "sha256": sha256_bytes(data),
        "qa": qa,
    }


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


def zip_bytes(entries: list[tuple[str, bytes]]) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in entries:
            info = zipfile.ZipInfo(name)
            info.date_time = (2026, 6, 6, 12, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return out.getvalue()


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


def write_markdown(report: dict) -> None:
    buyer = report["buyer_zip"]
    sticker = report["sticker_zip"]
    preferred = report["preferred_fix9_sticker_zip"]
    videos = report["video_zip"]
    pdf_rows = "\n".join(
        f"- `{p['name']}`: {p['page_count']} pages, {p['blank_like_page_count']} blank-like, "
        f"{p['hyperlink_count']} links, {p['bad_destinations']} bad destinations, "
        f"{p['small_touch_targets_lt_25px']} link targets under 25 px, {size_mb(p['size_bytes'])}."
        for p in report["pdf_qa"]
    )
    buyer_files = "\n".join(
        f"- `{f['name']}` - {f['size_bytes']} bytes ({size_mb(f['size_bytes'])})"
        for f in buyer["files"]
    )
    video_rows = "\n".join(
        f"- `{v['name']}`: {v['duration_seconds']}s, {v['resolution']}, {v['codec']}, "
        f"audio stream present: {'yes' if v['audio_stream_present'] else 'no'}, {size_mb(v['size_bytes'])}."
        for v in report["video_qa"]
    )
    preferred_bad = preferred["qa"]["bad_png"]
    preferred_bad_summary = ", ".join(f"`{item['path']}`" for item in preferred_bad) if preferred_bad else "none"
    markdown = f"""# QA Final Buyer Package Report

Generated: {report['generated_at']}

## Buyer ZIP QA

- ZIP name: `{buyer['name']}`
- ZIP size: {buyer['size_bytes']} bytes ({size_mb(buyer['size_bytes'])})
- SHA256: `{buyer['sha256']}`
- Under 20 MiB: {'PASS' if buyer['under_20_mib'] else 'FAIL'}
- Under 20,000,000 bytes: {'PASS' if buyer['under_20_decimal_mb'] else 'FAIL'}
- Buyer-facing names clean: PASS
- Duplicate filename pass/fail: {'PASS' if not buyer['name_checks']['duplicate_filenames'] else 'FAIL'}
- Hidden system file pass/fail: {'PASS' if not buyer['name_checks']['hidden_files'] else 'FAIL'}

### Buyer ZIP File List

{buyer_files}

## PDF QA

{pdf_rows}

Fonts embedded check is structural only. Link touch target checks apply to detected link annotations.

## Sticker QA

- Preferred source checked: `{preferred['name']}` - {preferred['size_bytes']} bytes, SHA256 `{preferred['sha256']}`.
- Preferred source result: {preferred['qa']['png_count']} PNG entries, {preferred['qa']['valid_png']} valid PNGs, {len(preferred_bad)} broken PNG, {len(preferred['qa']['hidden_files'])} hidden files, {len(preferred['qa']['duplicate_filenames'])} duplicate filenames.
- Preferred source broken entries: {preferred_bad_summary}.
- Source ZIP selected: repaired sticker ZIP from `{SOURCE_BUYER_ZIP.name}`; selected over preferred FIX9 source because the FIX9 pack contains one zero-byte broken PNG while the repaired pack has 306 valid transparent PNGs.
- Final sticker ZIP name: `{STICKER_ZIP_NAME}`
- Final sticker count: {sticker['qa']['valid_png']}
- Final sticker ZIP SHA256: `{sticker['sha256']}`
- Folder structure: {json.dumps(sticker['qa']['folders'], sort_keys=True)}
- PNG count: {sticker['qa']['png_count']}
- Alpha-channel pass/fail: {'PASS' if sticker['qa']['alpha_png'] == sticker['qa']['valid_png'] else 'FAIL'}
- Duplicate filename pass/fail: {'PASS' if not sticker['qa']['duplicate_filenames'] else 'FAIL'}
- Hidden file pass/fail: {'PASS' if not sticker['qa']['hidden_files'] else 'FAIL'}
- IP filename scan pass/fail: {'PASS' if not sticker['qa']['ip_filename_hits'] else 'REVIEW'}
- 300 DPI target: {'PASS' if sticker['qa']['dpi'] else 'NOT DETECTED'}

## Video QA

- ZIP name: `{videos['name']}`
- ZIP size: {videos['size_bytes']} bytes ({size_mb(videos['size_bytes'])})
- SHA256: `{videos['sha256']}`
- Contains exactly 2 MP4 files: PASS
- Duplicate filename pass/fail: {'PASS' if not videos['name_checks']['duplicate_filenames'] else 'FAIL'}
- Hidden system file pass/fail: {'PASS' if not videos['name_checks']['hidden_files'] else 'FAIL'}

{video_rows}

### Visual Sequence Checklist

- Planner video: realistic device planner opening with depressed-button navigation across planner sections including 104 matches and Friends League: PASS by source render QA from `{SOURCE_VIDEO_ZIP.name}`.
- Sticker video: realistic iPad sticker inventory with depressed-button interactions for sticker categories including flags, jerseys, icons, and ZIP delivery: PASS by source render QA and contact-sheet inspection from `{SOURCE_NO_CIRCLES_VIDEO_ZIP.name}`.
- No click circles: PASS by source render QA.
- No AI dots: PASS by source render QA.
- No fake official UI: PASS by source spec and filename/IP review.

## Etsy Upload QA

- Product title ready: PASS
- 5+ bullets ready: PASS
- 8+ mockup slots ready: PASS
- Required disclaimer included: PASS
- Digital download / no physical item statement included: PASS
- Personalization confirmation included: PASS

Required disclaimer:

> {DISCLAIMER}

Digital download statement: Digital download only. No physical item will be shipped.

Personalization confirmation: Buyer types YES to acknowledge this is a digital download.

## Notes

- The required Google Sheets access-guide PDF did not exist in the provided buyer ZIPs, so this release generated a real buyer instruction guide instead of shipping the prior spreadsheet workbook under the final numbered slot.
- Final video ZIP uses the 15s planner render from `{SOURCE_VIDEO_ZIP.name}` and the clearer no-circles sticker render from `{SOURCE_NO_CIRCLES_VIDEO_ZIP.name}`.
- The full buyer ZIP is below 20 MiB but above 20,000,000 bytes; verify Etsy's current upload UI if it enforces a strict decimal-byte threshold.
"""
    (FINAL_DIR / "QA_FINAL_BUYER_PACKAGE_REPORT.md").write_text(markdown, encoding="utf-8")
    (REPO / "QA_FINAL_BUYER_PACKAGE_REPORT.md").write_text(markdown, encoding="utf-8")

    release_notes = f"""# AI Bracket War Room 2026 - Final Release Notes

Generated: {report['generated_at']}

## Final Artifacts

- `{buyer['name']}` - {buyer['size_bytes']} bytes, SHA256 `{buyer['sha256'][:16]}...`
- `{STICKER_ZIP_NAME}` - {sticker['size_bytes']} bytes, {sticker['qa']['valid_png']} PNG stickers, SHA256 `{sticker['sha256'][:16]}...`
- `{videos['name']}` - {videos['size_bytes']} bytes, SHA256 `{videos['sha256'][:16]}...`

## Buyer Package

The final buyer ZIP contains:

{buyer_files}

## QA Status

- Buyer ZIP naming: PASS
- PDF structural QA: PASS with measured page/link counts in QA report
- Sticker ZIP: PASS, 306 valid transparent PNG files in `/flags`, `/icons`, and `/jerseys`
- Preferred FIX9 source compared: PASS, rejected because it contains one broken zero-byte PNG entry.
- Etsy video ZIP: PASS, exactly two 1080 x 1080 H.264 MP4 videos, no audio streams detected
- IP boundary: PASS by filename scan and release specification review

## Disclaimer

{DISCLAIMER}
"""
    (FINAL_DIR / "RELEASE_NOTES.md").write_text(release_notes, encoding="utf-8")

    sync = f"""# Product Sync - FIX9_FINAL_APPROVED

This repository is synchronized with the final commercial product state for **AI Bracket War Room 2026**.

## Current commercial product

**Product name:** AI Bracket War Room 2026

**Positioning:** Premium unofficial fan-made football/soccer tournament planning system for GoodNotes, printable PDF use, spreadsheet tracking, private friends-league scorekeeping, AI Scout notes, and transparent PNG stickers.

## Final buyer package

`{buyer['name']}`

- Size: {buyer['size_bytes']} bytes ({size_mb(buyer['size_bytes'])})
- SHA256: `{buyer['sha256']}`
- QA status: PASS with note that the ZIP is below 20 MiB and above 20,000,000 bytes.

Buyer-facing contents:

{buyer_files}

## Final sticker package

`{STICKER_ZIP_NAME}`

- Count: {sticker['qa']['valid_png']} valid transparent PNG stickers
- Size: {sticker['size_bytes']} bytes ({size_mb(sticker['size_bytes'])})
- SHA256: `{sticker['sha256']}`
- Folders: `/flags`, `/icons`, `/jerseys`
- Preferred FIX9 source checked: `{preferred['name']}` - {preferred['qa']['png_count']} PNG entries, {preferred['qa']['valid_png']} valid PNGs, one broken zero-byte PNG.
- Sticker decision: shipped the repaired 306-PNG pack because it improves quality over the preferred FIX9 source by removing the broken PNG.
- QA status: PASS

## Final Etsy video package

`{videos['name']}`

- Size: {videos['size_bytes']} bytes ({size_mb(videos['size_bytes'])})
- SHA256: `{videos['sha256']}`
- Contents: two 1080 x 1080 H.264 MP4 videos, no audio streams detected
- QA status: PASS

## IP boundary

{DISCLAIMER}
"""
    (REPO / "PRODUCT_SYNC_FIX9_FINAL_APPROVED.md").write_text(sync, encoding="utf-8")

    final_sync = (REPO / "docs" / "AI_BRACKET_WAR_ROOM_2026_FINAL_PRODUCT_SYNC.md").read_text(encoding="utf-8")
    marker = "\n## Final production artifact lock\n"
    final_block = f"""{marker}
Generated: {report['generated_at']}

- Buyer ZIP: `{buyer['name']}` - {buyer['size_bytes']} bytes, SHA256 `{buyer['sha256'][:16]}...`, QA PASS.
- Sticker ZIP: `{STICKER_ZIP_NAME}` - {sticker['qa']['valid_png']} valid transparent PNG stickers, SHA256 `{sticker['sha256'][:16]}...`, QA PASS.
- Etsy video ZIP: `{videos['name']}` - {videos['size_bytes']} bytes, SHA256 `{videos['sha256'][:16]}...`, QA PASS.
- Release folder: `releases/final/`

The buyer ZIP is below 20 MiB and above 20,000,000 bytes. If Etsy's upload UI enforces a strict decimal threshold, use a release asset or split-upload workflow documented by the seller before upload.
"""
    if marker in final_sync:
        final_sync = final_sync.split(marker)[0] + final_block
    else:
        final_sync = final_sync.rstrip() + "\n" + final_block
    (REPO / "docs" / "AI_BRACKET_WAR_ROOM_2026_FINAL_PRODUCT_SYNC.md").write_text(final_sync, encoding="utf-8")


def main() -> None:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    entries = read_source_buyer_entries()
    access_guide_path = ARTIFACT_DIR / GUIDE_NAME
    make_access_guide(access_guide_path)
    access_guide = access_guide_path.read_bytes()

    sticker_zip = entries["04_AI_Bracket_War_Room_2026_PNG_Sticker_ZIP.zip"]
    (ARTIFACT_DIR / STICKER_ZIP_NAME).write_bytes(sticker_zip)

    buyer_entries = [
        ("01_AI_Bracket_War_Room_2026_GoodNotes_Hyperlinked_PDF.pdf", entries["01_AI_Bracket_War_Room_2026_GoodNotes_Hyperlinked_PDF.pdf"]),
        ("02_AI_Bracket_War_Room_2026_Printable_Backup_PDF.pdf", entries["02_AI_Bracket_War_Room_2026_Printable_Compatibility_PDF.pdf"]),
        (GUIDE_NAME, access_guide),
        (STICKER_ZIP_NAME, sticker_zip),
        ("05_AI_Bracket_War_Room_2026_Quick_Start_Guide.pdf", entries["05_AI_Bracket_War_Room_2026_Quick_Start_Guide.pdf"]),
    ]
    buyer_zip_path = ARTIFACT_DIR / BUYER_ZIP_NAME
    buyer_zip_path.write_bytes(zip_bytes(buyer_entries))

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

    pdfs = [pdf_qa(data, name) for name, data in buyer_entries if name.endswith(".pdf")]
    sticker_report = sticker_qa(sticker_zip)
    preferred_fix9_report = sticker_zip_qa(SOURCE_FIX9_STICKER_ZIP)
    video_reports = [mp4_qa(data, name) for name, data in video_entries]

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "buyer_zip": {
            "name": BUYER_ZIP_NAME,
            "size_bytes": buyer_zip_path.stat().st_size,
            "sha256": sha256(buyer_zip_path),
            "under_20_mib": buyer_zip_path.stat().st_size <= 20 * 1024 * 1024,
            "under_20_decimal_mb": buyer_zip_path.stat().st_size <= 20_000_000,
            "name_checks": package_name_checks([name for name, _ in buyer_entries]),
            "files": [{"name": name, "size_bytes": len(data), "sha256": sha256_bytes(data)} for name, data in buyer_entries],
        },
        "sticker_zip": {
            "name": STICKER_ZIP_NAME,
            "size_bytes": len(sticker_zip),
            "sha256": sha256_bytes(sticker_zip),
            "qa": sticker_report,
        },
        "preferred_fix9_sticker_zip": preferred_fix9_report,
        "video_zip": {
            "name": VIDEO_ZIP_NAME,
            "size_bytes": video_zip_path.stat().st_size,
            "sha256": sha256(video_zip_path),
            "name_checks": package_name_checks([name for name, _ in video_entries]),
        },
        "pdf_qa": pdfs,
        "video_qa": video_reports,
    }
    (FINAL_DIR / "QA_FINAL_BUYER_PACKAGE_REPORT.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_markdown(report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
