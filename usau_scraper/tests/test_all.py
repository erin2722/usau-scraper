import requests
from bs4 import BeautifulSoup

from usau_scraper import (
    queryTeam,
    getTeamRoster,
    getTeamInfo,
    getTeamSchedule,
    setArgs,
    fillInBasicInfo,
    getTournamentBracketResults,
    getTournamentPoolPlayResults,
    getTournamentWinner,
    getCollegeRankings,
    getClubRankings,
)

# ------------------------------- UNIT TESTS -------------------------------


# ------------------ queryTeam Tests ------------------
def test_query_team_multiple_teams():
    team_results = queryTeam({"schoolName": "Columbia", "competitionLevel": "College", "genderDivision": "Women"})

    expected_res_keys = ["British Columbia (Thunderbirds)", "Columbia (Curbside)", "Columbia-B (Baewatch)"]

    assert list(team_results.keys()) == expected_res_keys


def test_query_team_no_teams():
    team_results = queryTeam({"schoolName": "wiugwiugbiwug"})

    assert team_results == {}


def test_query_team_more_than_twenty():
    team_results = queryTeam({"competitionLevel": "College"})

    assert len(team_results) == 20


def test_query_team_uri_passed_in():
    teams = queryTeam({"teamURI": "TEST_URI"})

    assert len(teams) == 1
    assert teams["singleTeam"] == "TEST_URI"


# ------------------ setArgs Tests ------------------
def test_set_args():
    args = {
        "schoolName": "Columbia",
        "teamName": "Baewatch",
        "genderDivision": "Women",
        "state": "NY",
        "competitionLevel": "College",
        "competitionDivision": "Division 1",
        "teamDesignation": "B",
    }

    expectedData = {
        "__EVENTTARGET": "CT_Main_0$gvList$ctl23$ctl00$ctl00",
        "CT_Main_0$F_Status": "Published",
        "CT_Main_0$F_SchoolName": "Columbia",
        "CT_Main_0$F_TeamName": "Baewatch",
        "CT_Main_0$F_GenderDivisionId": 2,
        "CT_Main_0$F_StateId": "NY",
        "CT_Main_0$F_CompetitionLevelId": "College",
        "CT_Main_0$F_CompetitionDivisionId": 1,
        "CT_Main_0$F_Designation": 1,
    }

    data = setArgs(args)

    assert data == expectedData


# ------------------ fillInBasicInfo Tests ------------------
def test_basic_info():
    with requests.Session() as req:
        r = req.get(
            "https://play.usaultimate.org/teams/events/Eventteam/?TeamId=xPLDyRaZDSiR0OTzDBsYfzn8PJeIKdalFgjWpKUXiLI%3d"
        )
        soup = BeautifulSoup(r.content, 'html.parser')

        info = fillInBasicInfo(soup)

        expectedInfo = {
            "schoolName": "Columbia",
            "teamName": "Curbside",
            "competitionLevel": "College",
            "genderDivision": "Women",
            "location": "New York , New York",
        }

        assert info == expectedInfo


# ------------------------------- INTEGRATION TESTS -------------------------------


# ------------------ getTeamInfo Tests ------------------
def test_get_team_info():
    teams = getTeamInfo(schoolName="North Carolina", teamName="Pleiades")

    expectedTeamInfo = [
        {
            "schoolName": "North Carolina",
            "teamName": "Pleiades",
            "competitionLevel": "College",
            "genderDivision": "Women",
            "location": "Chapel Hill, North Carolina",
            "coaches": "Jessica Jones Head CoachMary Rippe Elisabeth Parker",
            "website": "http://www.uncpleiades.com",
            "facebook": "https://www.facebook.com/unc.pleiades/",
            "twitter": "https://twitter.com/UNC_Pleiades/",
        }
    ]

    assert teams["res"] == "OK"
    assert teams["teams"] == expectedTeamInfo


def test_get_team_info_not_found():
    teams = getTeamInfo(schoolName="wgiubwiugbiwugbwiubwgub")

    assert teams["res"] == "NOTFOUND"


# ------------------ getTeamSchedule Tests ------------------
def test_get_team_schedule():
    teams = getTeamSchedule(schoolName="Columbia", teamName="Curbside")

    expectedTournamentResults = {
        "games": [
            {
                "date": "March 04",
                "score": "7 - 9",
                "opponentCollege": "Cornell",
                "opponentHref": "/teams/events/Eventteam/?TeamId=swZShzB%2bFK4tsqtqa%2f511SwW9nXxGho7MjxCYzUxwlM%3d",
            },
            {
                "date": "March 04",
                "score": "9 - 6",
                "opponentCollege": "Rutgers",
                "opponentHref": "/teams/events/Eventteam/?TeamId=Cx6jfxJr%2bTJsYl3Z3urhSz4tpQxIcvCualgJhm1k%2b4w%3d",
            },
            {
                "date": "March 04",
                "score": "8 - 6",
                "opponentCollege": "Bates",
                "opponentHref": "/teams/events/Eventteam/?TeamId=qmVAo7N%2ftRZfIFCu881VvxKKXav4UKHaB842B%2bV%2fOD8%3d",
            },
            {
                "date": "March 05",
                "score": "6 - 8",
                "opponentCollege": "Williams",
                "opponentHref": "/teams/events/Eventteam/?TeamId=t1%2bUZ9UKbj6kJdnTioIuZWSnPEnaeyxXCvaufWX7QOQ%3d",
            },
            {
                "date": "March 05",
                "score": "8 - 5",
                "opponentCollege": "Harvard",
                "opponentHref": "/teams/events/Eventteam/?TeamId=Qes6Me2QohbI%2faNOUJQwedpQQwIdMXQLxWGTGRzTie8%3d",
            },
        ]
    }

    assert teams["res"] == "OK"
    assert teams["teams"][0]["tournaments"]["No Sleep Till Brooklyn 2023"] == expectedTournamentResults


# ------------------ getTeamRoster Tests ------------------
def test_get_team_roster():
    teams = getTeamRoster(schoolName="Columbia", teamName="Curbside")

    expectedPlayer = {
        "no": "7",
        "name": "Aya Lahlou",
        "pronouns": "S",
        "position": "",
        "year": "College (GR)",
        "height": "5'5\"",
    }

    assert teams["res"] == "OK"
    assert expectedPlayer in teams["teams"][0]["roster"]


# ------------------ getTournamentPoolPlayResults Tests ------------------
def test_get_tournament_pool_play():
    results = getTournamentPoolPlayResults("College", "Women", eventName="No Sleep Till Brooklyn", season=2023)

    expectedPoolAResults = {
        "Team": "Wellesley (1)",
        "W - L": "3 - 0",
    }

    assert results["res"] == "OK"
    del results["No Sleep Till Brooklyn 2023"]["pools"]["Pool A"][0]["Tie"]  # bc NaN != NaN
    assert results["No Sleep Till Brooklyn 2023"]["pools"]["Pool A"][0] == expectedPoolAResults


# ------------------ getTournamentBracketResults Tests ------------------
def test_get_tournament_bracket():
    results = getTournamentBracketResults("College", "Women", eventName="No Sleep Till Brooklyn", season=2023)

    expectedFinalsResults = {
        "date": "3/5/2023",
        "time": "1:00PM",
        "field": "8b",
        "winner": "Wellesley (1)",
        "loser": "Cornell (11)",
        "score": "10 - 4",
        "status": "Final",
    }

    assert results["res"] == "OK"
    assert results["No Sleep Till Brooklyn 2023"]["Championship Bracket"]["Finals"][0] == expectedFinalsResults


# ------------------ getTournamentWinner Tests ------------------
def test_get_tournament_winner():
    results = getTournamentWinner("College", "Women", eventName="No Sleep Till Brooklyn", season=2023)

    expectedResults = {"firstPlace": "Wellesley (1)", "secondPlace": "Cornell (11)"}

    assert results["res"] == "OK"
    assert results["No Sleep Till Brooklyn 2023"] == expectedResults


# ------------------ getCollegeRankings Tests ------------------
def test_get_college_rankings():
    teams = getCollegeRankings(genderDivision="Women")

    expectedTeam = {
        "Rank": "1",
        "Team": "North Carolina",
        "Power Rating": "2824",
        "Competition Level": "College",
        "Gender Division": "Women",
        "Competition Division": "Division I",
        "College Region": "Atlantic Coast",
        "College Conference": "Carolina DI",
        "Wins": "16",
        "Losses": "0",
    }

    assert teams["res"] == "OK"
    assert expectedTeam == teams["teams"][0]


# ------------------ getClubRankings Tests ------------------
def test_get_club_rankings():
    teams = getClubRankings(genderDivision="Men")

    expectedTeam = {
        "Rank": "1",
        "Team": "Truck Stop",
        "Power Rating": "2134",
        "Gender Division": "Men",
        "Competition Division": "Pro",
        "City": "Washington",
        "State": "DC",
        "Club Region": "Mid-Atlantic",
        "Club Section": "Capital",
        "Wins": "30",
        "Losses": "4",
    }

    assert teams["res"] == "OK"
    assert expectedTeam == teams["teams"][0]
