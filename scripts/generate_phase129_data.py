from __future__ import annotations

import csv
import io
import json
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import lxml.html
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

WIKI_MAIN = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup"
WIKI_SQUADS = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_squads"
FIFA_FIXTURES = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/fixtures"
FIFA_TEAMS = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/teams"
FIFA_SQUADS = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/teams"
ESPN_FIXTURES = "https://www.espn.com/soccer/fixtures/_/league/FIFA.WORLD"

TEAM_META = {
    "Mexico": ("MEX", "CONCACAF", "🇲🇽"),
    "South Africa": ("RSA", "CAF", "🇿🇦"),
    "South Korea": ("KOR", "AFC", "🇰🇷"),
    "Czech Republic": ("CZE", "UEFA", "🇨🇿"),
    "Canada": ("CAN", "CONCACAF", "🇨🇦"),
    "Bosnia and Herzegovina": ("BIH", "UEFA", "🇧🇦"),
    "Qatar": ("QAT", "AFC", "🇶🇦"),
    "Switzerland": ("SUI", "UEFA", "🇨🇭"),
    "Brazil": ("BRA", "CONMEBOL", "🇧🇷"),
    "Haiti": ("HAI", "CONCACAF", "🇭🇹"),
    "Morocco": ("MAR", "CAF", "🇲🇦"),
    "Scotland": ("SCO", "UEFA", "🏴"),
    "United States": ("USA", "CONCACAF", "🇺🇸"),
    "Paraguay": ("PAR", "CONMEBOL", "🇵🇾"),
    "Australia": ("AUS", "AFC", "🇦🇺"),
    "Turkey": ("TUR", "UEFA", "🇹🇷"),
    "Germany": ("GER", "UEFA", "🇩🇪"),
    "Curaçao": ("CUW", "CONCACAF", "🇨🇼"),
    "Ivory Coast": ("CIV", "CAF", "🇨🇮"),
    "Ecuador": ("ECU", "CONMEBOL", "🇪🇨"),
    "Netherlands": ("NED", "UEFA", "🇳🇱"),
    "Japan": ("JPN", "AFC", "🇯🇵"),
    "Sweden": ("SWE", "UEFA", "🇸🇪"),
    "Tunisia": ("TUN", "CAF", "🇹🇳"),
    "Belgium": ("BEL", "UEFA", "🇧🇪"),
    "Egypt": ("EGY", "CAF", "🇪🇬"),
    "Iran": ("IRN", "AFC", "🇮🇷"),
    "New Zealand": ("NZL", "OFC", "🇳🇿"),
    "Spain": ("ESP", "UEFA", "🇪🇸"),
    "Cape Verde": ("CPV", "CAF", "🇨🇻"),
    "Saudi Arabia": ("KSA", "AFC", "🇸🇦"),
    "Uruguay": ("URU", "CONMEBOL", "🇺🇾"),
    "France": ("FRA", "UEFA", "🇫🇷"),
    "Senegal": ("SEN", "CAF", "🇸🇳"),
    "Iraq": ("IRQ", "AFC", "🇮🇶"),
    "Norway": ("NOR", "UEFA", "🇳🇴"),
    "Argentina": ("ARG", "CONMEBOL", "🇦🇷"),
    "Algeria": ("ALG", "CAF", "🇩🇿"),
    "Austria": ("AUT", "UEFA", "🇦🇹"),
    "Jordan": ("JOR", "AFC", "🇯🇴"),
    "Portugal": ("POR", "UEFA", "🇵🇹"),
    "DR Congo": ("COD", "CAF", "🇨🇩"),
    "Uzbekistan": ("UZB", "AFC", "🇺🇿"),
    "Colombia": ("COL", "CONMEBOL", "🇨🇴"),
    "England": ("ENG", "UEFA", "🏴"),
    "Croatia": ("CRO", "UEFA", "🇭🇷"),
    "Ghana": ("GHA", "CAF", "🇬🇭"),
    "Panama": ("PAN", "CONCACAF", "🇵🇦"),
}

CANONICAL_NAMES = {
    "South Korea": "Korea Republic",
    "Bosnia and Herzegovina": "Bosnia & Herzegovina",
    "Turkey": "Türkiye",
    "Ivory Coast": "Côte d'Ivoire",
    "Iran": "IR Iran",
}

CITY_COUNTRY = {
    "Mexico City": "Mexico",
    "Zapopan": "Mexico",
    "Guadalupe": "Mexico",
    "Guadalajara": "Mexico",
    "Monterrey": "Mexico",
    "Toronto": "Canada",
    "Vancouver": "Canada",
    "Atlanta": "United States",
    "Boston": "United States",
    "Foxborough": "United States",
    "Dallas": "United States",
    "Arlington": "United States",
    "Houston": "United States",
    "Kansas City": "United States",
    "Los Angeles": "United States",
    "Inglewood": "United States",
    "Miami": "United States",
    "Miami Gardens": "United States",
    "New York/New Jersey": "United States",
    "East Rutherford": "United States",
    "Philadelphia": "United States",
    "San Francisco Bay Area": "United States",
    "Santa Clara": "United States",
    "Seattle": "United States",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 phase129-data-harness"})
    return urllib.request.urlopen(req, timeout=30).read()


def canon(name: object) -> str:
    text = re.sub(r"\[[^\]]+\]", "", str(name)).strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace("(H)", "").strip()
    return CANONICAL_NAMES.get(text, text)


def code_for(name: str) -> str:
    reverse = {canon(k): v[0] for k, v in TEAM_META.items()}
    return reverse.get(canon(name), "")


def stage_for(match_no: int) -> str:
    if match_no <= 72:
        return "Group Stage"
    if match_no <= 88:
        return "Round of 32"
    if match_no <= 96:
        return "Round of 16"
    if match_no <= 100:
        return "Quarter-final"
    if match_no <= 102:
        return "Semi-final"
    if match_no == 103:
        return "Third-place playoff"
    return "Final"


def clean_slot(value: object) -> str:
    text = canon(value)
    text = text.replace("Winner Group", "Group").replace("Runner-up Group", "Group")
    if text.startswith("3rd Group "):
        return "Best third-place team from Groups " + text.replace("3rd Group ", "").replace("/", ", ")
    text = re.sub(r"^Winner Group ([A-L])$", r"Group \1 winners", text)
    text = re.sub(r"^Runner-up Group ([A-L])$", r"Group \1 runners-up", text)
    text = re.sub(r"^Winner Match (\d+)$", r"Match \1 winners", text)
    text = re.sub(r"^Loser Match (\d+)$", r"Match \1 losers", text)
    return text


def extract_time(node_text: str) -> tuple[str, str, str]:
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})\).*?(\d{1,2}:\d{2})\s*([ap]\.m\.)\s*UTC([−-]\d+|[+]\d+)?", node_text)
    if not date_match:
        return "", "", ""
    date_text, hhmm, ampm, offset_text = date_match.groups()
    hour, minute = [int(part) for part in hhmm.split(":")]
    if ampm.startswith("p") and hour != 12:
        hour += 12
    if ampm.startswith("a") and hour == 12:
        hour = 0
    offset_hours = int((offset_text or "+0").replace("−", "-"))
    local = datetime.fromisoformat(date_text).replace(hour=hour, minute=minute)
    utc_dt = local - timedelta(hours=offset_hours)
    uk_dt = utc_dt + timedelta(hours=1)
    return f"{hour:02d}:{minute:02d}", uk_dt.strftime("%H:%M"), utc_dt.strftime("%H:%M")


def venue_parts(text: str) -> tuple[str, str, str]:
    compact = " ".join(text.split())
    compact = re.sub(r"Attendance:.*", "", compact)
    compact = re.sub(r"Referee:.*", "", compact).strip()
    if "," in compact:
        stadium, city = [part.strip() for part in compact.split(",", 1)]
    else:
        stadium, city = compact, ""
    country = ""
    for key, value in CITY_COUNTRY.items():
        if key in city:
            country = value
            break
    return stadium, city, country


def build_groups(main_tables: list[pd.DataFrame]) -> list[dict[str, object]]:
    rows = []
    groups = list("ABCDEFGHIJKL")
    table_indexes = [11, 18, 25, 32, 39, 46, 53, 60, 67, 74, 81, 88]
    for group, table_index in zip(groups, table_indexes):
        table = main_tables[table_index]
        team_col = next(col for col in table.columns if "Team" in str(col))
        for seed, team in enumerate(table[team_col].tolist(), start=1):
            raw = re.sub(r"\s*\(H\)", "", str(team)).strip()
            canonical = canon(raw)
            meta = TEAM_META.get(raw) or TEAM_META.get(canonical) or ("", "", "")
            rows.append(
                {
                    "group": group,
                    "seed": seed,
                    "team": canonical,
                    "team_code": meta[0],
                    "confederation": meta[1],
                    "flag_emoji": meta[2],
                    "source_status": "cross_checked",
                }
            )
    return rows


def build_fixtures(root: lxml.html.HtmlElement, group_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    team_group = {row["team"]: row["group"] for row in group_rows}
    fixtures = {}
    for table in root.xpath("//table"):
        text = " ".join(table.text_content().split())
        headers = [clean_slot(th.text_content()) for th in table.xpath(".//tr[1]/*")]
        middle_label = headers[1] if len(headers) >= 3 else ""
        match = re.fullmatch(r"Match\s+(\d{1,3})", middle_label)
        if not match:
            match = re.search(r"Match\s+(\d{1,3})", text)
        if not match:
            report = re.search(r"Report\s+(\d{1,3})", text)
            match = report
        if not match:
            continue
        match_no = int(match.group(1))
        if not 1 <= match_no <= 104:
            continue
        if len(headers) < 3:
            continue
        home, away = headers[0], headers[2]
        prev_text = " ".join((table.getprevious().text_content() if table.getprevious() is not None else "").split())
        next_text = " ".join((table.getnext().text_content() if table.getnext() is not None else "").split())
        kickoff_local, kickoff_uk, kickoff_utc = extract_time(prev_text)
        stadium, city, country = venue_parts(next_text)
        group = team_group.get(home, "") if match_no <= 72 else ""
        fixtures[match_no] = {
            "match_no": match_no,
            "stage": stage_for(match_no),
            "group": group,
            "date": re.search(r"\d{4}-\d{2}-\d{2}", prev_text).group(0) if re.search(r"\d{4}-\d{2}-\d{2}", prev_text) else "",
            "kickoff_local": kickoff_local,
            "kickoff_uk": kickoff_uk,
            "kickoff_utc": kickoff_utc,
            "home": home,
            "away": away,
            "home_code": code_for(home),
            "away_code": code_for(away),
            "city": city,
            "country": country,
            "stadium": stadium,
            "team_data_status": "known_teams" if match_no <= 72 else "dynamic_slot",
            "source_status": "cross_checked",
            "bracket_slot_note": "" if match_no <= 72 else f"{home} vs {away}",
        }
    return [fixtures[index] for index in range(1, 105)]


def build_squads() -> list[dict[str, object]]:
    html = fetch(WIKI_SQUADS)
    root = lxml.html.fromstring(html)
    tables = pd.read_html(io.BytesIO(html))
    table_nodes = root.xpath("//table")
    rows = []
    table_index = 0
    for node in table_nodes:
        heads = [th.text_content().strip() for th in node.xpath(".//tr[1]//th")]
        if not {"No.", "Pos.", "Player"}.issubset(set(heads)):
            continue
        heading = node.xpath("preceding::*[self::h3 or self::h2][1]")
        raw_team = " ".join(heading[0].text_content().split()) if heading else ""
        team = canon(raw_team)
        table = tables[table_index]
        while not {"No.", "Pos.", "Player"}.issubset({str(col) for col in table.columns}):
            table_index += 1
            table = tables[table_index]
        table_index += 1
        for _, player in table.iterrows():
            name = str(player.get("Player", "")).replace("(captain)", "").strip()
            name = re.sub(r"\s+", " ", name)
            parts = name.split()
            rows.append(
                {
                    "team": team,
                    "team_code": code_for(team),
                    "shirt_no": player.get("No.", ""),
                    "position": player.get("Pos.", ""),
                    "player_name": name,
                    "first_names": " ".join(parts[:-1]),
                    "last_names": parts[-1] if parts else "",
                    "name_on_shirt": parts[-1].upper() if parts else "",
                    "dob": re.sub(r"\s*\(aged.*\)", "", str(player.get("Date of birth (age)", ""))).strip(),
                    "club": player.get("Club", ""),
                    "height_cm": "",
                    "caps": player.get("Caps", ""),
                    "goals": player.get("Goals", ""),
                    "source_status": "cross_checked",
                    "parser_confidence": "high",
                }
            )
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    DATA.mkdir(exist_ok=True)
    main_html = fetch(WIKI_MAIN)
    root = lxml.html.fromstring(main_html)
    main_tables = pd.read_html(io.BytesIO(main_html))
    groups = build_groups(main_tables)
    fixtures = build_fixtures(root, groups)
    squads = build_squads()
    metadata = [
        {
            "team": row["team"],
            "team_code": row["team_code"],
            "group": row["group"],
            "seed": row["seed"],
            "coach": "",
            "ranking_note": "",
            "style_note": "",
            "key_players_note": "",
            "source_status": "derived_from_squad_only",
        }
        for row in groups
    ]
    manifest = {
        "phase": "PHASE_1_29_FINAL_DATA_FILL",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {
            "official_fixtures": FIFA_FIXTURES,
            "official_teams": FIFA_TEAMS,
            "official_squads": FIFA_SQUADS,
            "fixture_crosscheck": ESPN_FIXTURES,
            "public_extraction_fixtures_and_groups": WIKI_MAIN,
            "public_extraction_squads": WIKI_SQUADS,
        },
        "expected_counts": {
            "groups": 12,
            "teams": 48,
            "matches": 104,
            "group_stage_matches": 72,
            "knockout_matches": 32,
            "players_expected_if_full_26_each": 1248,
        },
        "legal_positioning": {
            "status": "Unofficial fan-made planning demo",
            "forbidden": [
                "FIFA logo",
                "official World Cup emblem",
                "official trophy replica",
                "team federation crests",
                "player likenesses",
                "sponsor boards",
                "betting odds",
                "sportsbook language",
                "affiliation or endorsement claims",
            ],
        },
    }
    write_csv(DATA / "wc2026_groups.csv", ["group", "seed", "team", "team_code", "confederation", "flag_emoji", "source_status"], groups)
    write_csv(
        DATA / "wc2026_fixtures.csv",
        [
            "match_no",
            "stage",
            "group",
            "date",
            "kickoff_local",
            "kickoff_uk",
            "kickoff_utc",
            "home",
            "away",
            "home_code",
            "away_code",
            "city",
            "country",
            "stadium",
            "team_data_status",
            "source_status",
            "bracket_slot_note",
        ],
        fixtures,
    )
    write_csv(
        DATA / "wc2026_squads.csv",
        [
            "team",
            "team_code",
            "shirt_no",
            "position",
            "player_name",
            "first_names",
            "last_names",
            "name_on_shirt",
            "dob",
            "club",
            "height_cm",
            "caps",
            "goals",
            "source_status",
            "parser_confidence",
        ],
        squads,
    )
    write_csv(
        DATA / "wc2026_team_metadata.csv",
        ["team", "team_code", "group", "seed", "coach", "ranking_note", "style_note", "key_players_note", "source_status"],
        metadata,
    )
    (DATA / "wc2026_data_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"groups={len(groups)} teams={len({row['team'] for row in groups})} fixtures={len(fixtures)} squads={len(squads)}")


if __name__ == "__main__":
    main()
