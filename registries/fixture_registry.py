from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TeamRef:
    code: str
    name: str
    group: str

@dataclass(frozen=True, slots=True)
class FixtureRef:
    match_id: int
    group: str
    round_label: str
    team_a: TeamRef
    team_b: TeamRef
    @property
    def page_number(self) -> int:
        return 70 + self.match_id
    @property
    def display_label(self) -> str:
        return f"{self.match_id:03d}  {self.team_a.code} vs {self.team_b.code}"
    @property
    def title(self) -> str:
        return f"Match {self.match_id:03d} — {self.team_a.code} vs {self.team_b.code}"

GROUP_TEAMS: dict[str, tuple[TeamRef, TeamRef, TeamRef, TeamRef]] = {
    letter: tuple(TeamRef(f"{letter}{i}", f"Group {letter} Team {i}", letter) for i in range(1, 5))  # type: ignore[assignment]
    for letter in "ABCDEFGHIJKL"
}
GROUP_TEAMS.update({
    "A": (TeamRef("MEX", "Mexico", "A"), TeamRef("RSA", "South Africa", "A"), TeamRef("KOR", "Korea Republic", "A"), TeamRef("CZE", "Czechia", "A")),
    "B": (TeamRef("CAN", "Canada", "B"), TeamRef("BIH", "Bosnia & Herz.", "B"), TeamRef("QAT", "Qatar", "B"), TeamRef("SUI", "Switzerland", "B")),
    "C": (TeamRef("BRA", "Brazil", "C"), TeamRef("HAI", "Haiti", "C"), TeamRef("MAR", "Morocco", "C"), TeamRef("SCO", "Scotland", "C")),
    "D": (TeamRef("USA", "United States", "D"), TeamRef("AUS", "Australia", "D"), TeamRef("PAR", "Paraguay", "D"), TeamRef("TUR", "Turkiye", "D")),
})

def build_group_fixtures() -> tuple[FixtureRef, ...]:
    fixtures: list[FixtureRef] = []
    match_id = 1
    for group in "ABCDEFGHIJKL":
        t1, t2, t3, t4 = GROUP_TEAMS[group]
        pairings = (("Round 1", t1, t2), ("Round 1", t3, t4), ("Round 2", t1, t3), ("Round 2", t2, t4), ("Round 3", t1, t4), ("Round 3", t2, t3))
        for round_label, team_a, team_b in pairings:
            fixtures.append(FixtureRef(match_id, group, round_label, team_a, team_b))
            match_id += 1
    return tuple(fixtures)

def build_knockout_fixtures() -> tuple[FixtureRef, ...]:
    tbd = TeamRef("TBD", "To Be Decided", "KO")
    fixtures: list[FixtureRef] = []
    for match_id in range(73, 105):
        if match_id <= 88:
            round_label = "Round of 32"
        elif match_id <= 96:
            round_label = "Round of 16"
        elif match_id <= 100:
            round_label = "Quarterfinal"
        elif match_id <= 102:
            round_label = "Semifinal"
        elif match_id == 103:
            round_label = "Third Place"
        else:
            round_label = "Final"
        fixtures.append(FixtureRef(match_id, "KO", round_label, tbd, tbd))
    return tuple(fixtures)

FIXTURES: tuple[FixtureRef, ...] = build_group_fixtures() + build_knockout_fixtures()

def get_fixture(match_id: int) -> FixtureRef:
    if not 1 <= match_id <= 104:
        raise ValueError(f"Invalid match_id: {match_id}")
    return FIXTURES[match_id - 1]

def get_group_teams(group: str) -> tuple[TeamRef, TeamRef, TeamRef, TeamRef]:
    return GROUP_TEAMS[group.upper()]

def get_group_fixtures(group: str) -> tuple[FixtureRef, ...]:
    return tuple(fixture for fixture in FIXTURES if fixture.group == group.upper())

def get_index_range(index_page_number: int) -> tuple[int, int]:
    if index_page_number == 22:
        return 1, 36
    if index_page_number == 23:
        return 37, 72
    if index_page_number == 24:
        return 73, 104
    raise ValueError(f"Page {index_page_number} is not a match index page")

def get_index_fixtures(index_page_number: int) -> tuple[FixtureRef, ...]:
    first, last = get_index_range(index_page_number)
    return tuple(get_fixture(match_id) for match_id in range(first, last + 1))

def validate_fixture_registry() -> None:
    if len(FIXTURES) != 104:
        raise AssertionError(f"Expected 104 fixtures, found {len(FIXTURES)}")
    if [fixture.match_id for fixture in FIXTURES] != list(range(1, 105)):
        raise AssertionError("Fixture IDs are not contiguous from 001 to 104")
