"""
.. module:: teamScraper
   :synopsis: A module for scraping team schedule and roster information.

.. moduleauthor:: Erin McNulty
"""

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://play.usaultimate.org"


def getTeamInfo(**kwargs):
    '''getTeamInfo() returns all information about the first 20 teams matching the query

    Args:
        ``schoolName`` (string): The school that the team is affiliated with (ex. Columbia).

        ``teamName`` (string): The name of the team (ex. Pleiades).

        ``genderDivision`` (string): The gender division that the team competes in.
        Must be one of: Women, Men, Mixed, Boys, Girls.

        ``state`` (string): Postal abbreviation of the state the team is in.

        ``competitionLevel`` (string): The competition level that the team plays at.
        Must be one of: Club, College, High School, or Middle School.

        ``competitionDivision`` (string): The competition division that the team plays in.
        Must be one of: Classic, Developmental, Division 1, or Division 3.

        ``teamDesignation`` (string): If the team is a B or a C team. Must be B or C.

        ``teamURI`` (string): If querying based on team URI, will simply return the results of the team with
        this URI andignore other parameters.

    Returns:
        results:
            ::

                {
                    res: OK, NOTFOUND
                    teams: [
                        {
                            schoolName,
                            teamName,
                            competitionLevel,
                            genderDivision,
                            location,
                            coaches,
                            website,
                            facebook,
                            twitter,
                        },
                        ...
                    ]
                }

    '''
    teams = queryTeam(kwargs)

    if len(teams) == 0:
        return {"res": "NOTFOUND"}

    with requests.Session() as req:
        res = {"res": "OK", "teams": []}

        for _, endpoint in teams.items():
            r = req.get(BASE_URL + endpoint)
            soup = BeautifulSoup(r.content, 'html.parser')

            team = fillInBasicInfo(soup)

            coaches = soup.find(id="CT_Main_0_ucTeamDetails_dlHeadCoach")
            if coaches is not None:
                team["coaches"] = re.sub(r"[^a-zA-Z0-9 - , ]", "", coaches.find("dd").getText())

            website = soup.find(id="CT_Main_0_ucTeamDetails_dlWebsite")
            if website is not None:
                team["website"] = website.find("a").getText()

            facebook = soup.find(id="CT_Main_0_ucTeamDetails_dlFacebook")
            if facebook is not None:
                team["facebook"] = facebook.find("a").getText()

            twitter = soup.find(id="CT_Main_0_ucTeamDetails_dlTwitter")
            if twitter is not None:
                team["twitter"] = twitter.find("a").getText()

            res["teams"].append(team)

        return res


def getTeamSchedule(**kwargs):
    '''getTeamSchedule() returns the season schedule and record of the first 20 teams matching the query

    Args:
        ``schoolName`` (string): The school that the team is affiliated with (ex. Columbia).

        ``teamName`` (string): The name of the team (ex. Pleiades).

        ``genderDivision`` (string): The gender division that the team competes in.
        Must be one of: Women, Men, Mixed, Boys, Girls.

        ``state`` (string): Postal abbreviation of the state the team is in.

        ``competitionLevel`` (string): The competition level that the team plays at.
        Must be one of: Club, College, High School, or Middle School.

        ``competitionDivision`` (string): The competition division that the team plays in.
        Must be one of: Classic, Developmental, Division 1, or Division 3.

        ``teamDesignation`` (string): If the team is a B or a C team. Must be B or C.

        ``teamURI`` (string): If querying based on team URI, will simply return the results of the team with
        this URI and ignore other parameters.

    Returns:
        ::

            {
                res: OK, NOTFOUND
                teams: [
                    {
                        schoolName,
                        teamName,
                        competitionLevel,
                        genderDivision,
                        wins,
                        losses,
                        tournaments: {
                            name: {
                                games: [
                                    {
                                        date,
                                        score,
                                        opponentCollege,
                                        opponentTeamPage
                                    },
                                    ...
                                ]
                            },
                            ...
                        },
                    },
                    ...
                ]
            }'''
    teams = queryTeam(kwargs)

    if len(teams) == 0:
        return {"res": "NOTFOUND"}

    with requests.Session() as req:
        res = {"res": "OK", "teams": []}

        for _, endpoint in teams.items():
            r = req.get(BASE_URL + endpoint)
            soup = BeautifulSoup(r.content, 'html.parser')

            team = fillInBasicInfo(soup)
            team["wins"] = 0
            team["losses"] = 0
            team["tournaments"] = {}

            scheduleTable = soup.find(id="CT_Right_0_gvEventScheduleScores")

            if scheduleTable is None:
                res["teams"].append(team)
                continue

            scheduleTableRows = scheduleTable.findAll("tr")
            currentTournament = ""

            for row in scheduleTableRows:
                cells = row.findAll("td")

                if len(cells) == 1:
                    currentTournament = cells[0].find("a").getText()
                    team["tournaments"][currentTournament] = {"games": []}
                else:
                    date = cells[0].find("span").getText()
                    score = cells[1].find("a").getText()
                    oppCollege = cells[2].find("a").getText()
                    oppHref = cells[2].find("a").get("href")

                    game = {"date": date, "score": score, "opponentCollege": oppCollege, "opponentHref": oppHref}

                    if not cells[1].get("class") is None:
                        if cells[1].get("class")[0] == "win":
                            team["wins"] += 1
                        elif cells[1].get("class")[0] == "loss":
                            team["losses"] += 1

                    team["tournaments"][currentTournament]["games"].append(game)

            res["teams"].append(team)

        return res


def getTeamRoster(**kwargs):
    '''getTeamRoster() returns the roster of the first 20 teams matching the query

    Args:
        ``schoolName`` (string): The school that the team is affiliated with (ex. Columbia).

        ``teamName`` (string): The name of the team (ex. Pleiades).

        ``genderDivision`` (string): The gender division that the team competes in.
        Must be one of: Women, Men, Mixed, Boys, Girls.

        ``state`` (string): Postal abbreviation of the state the team is in.

        ``competitionLevel`` (string): The competition level that the team plays at.
        Must be one of: Club, College, High School, or Middle School.

        ``competitionDivision`` (string): The competition division that the team plays in.
        Must be one of: Classic, Developmental, Division 1, or Division 3.

        ``teamDesignation`` (string): If the team is a B or a C team. Must be B or C.

        ``teamURI`` (string): If querying based on team URI, will simply return the results of the team with
        this URI and ignore other parameters.

    Returns:
        results:
            ::

                {
                    res: OK, NOTFOUND
                    teams: [
                        {
                            schoolName,
                            teamName,
                            competitionLevel,
                            genderDivision,
                            roster: [
                                {
                                    no,
                                    name,
                                    pronouns,
                                    position,
                                    year,
                                    height,
                                },
                                ...
                            ]
                        },
                        ...
                    ]
                }
    '''

    teams = queryTeam(kwargs)

    if len(teams) == 0:
        return {"res": "NOTFOUND"}

    with requests.Session() as req:
        res = {"res": "OK", "teams": []}

        for _, endpoint in teams.items():
            r = req.get(BASE_URL + endpoint)
            soup = BeautifulSoup(r.content, 'html.parser')

            team = fillInBasicInfo(soup)

            team["roster"] = []

            rosterTable = soup.find(id="CT_Main_0_ucTeamDetails_gvList")

            rosterRows = rosterTable.findAll("tr")

            for row in rosterRows[1:]:
                cells = row.findAll("td")
                player = {}
                player["no"] = cells[0].getText()
                player["name"] = cells[1].getText()
                player["pronouns"] = cells[2].getText().strip()
                player["position"] = cells[3].getText().strip()
                player["year"] = cells[4].getText().strip()
                player["height"] = cells[5].getText().strip()

                team["roster"].append(player)

            res["teams"].append(team)

        return res


def fillInBasicInfo(soup):
    team = {}
    schoolTeam = soup.find(class_="profile_info").find("h4").getText()
    schoolTeamList = schoolTeam.split(" (")

    team["schoolName"] = schoolTeamList[0].strip()
    team["teamName"] = schoolTeamList[1].strip()[:-1]
    team["competitionLevel"] = soup.find(id="CT_Main_0_ucTeamDetails_dlCompetitionLevel").find("dd").getText()
    team["genderDivision"] = soup.find(id="CT_Main_0_ucTeamDetails_dlGenderDivision").find("dd").getText()
    team["location"] = soup.find(id="CT_Main_0_ucTeamDetails_dlCity").getText().strip()

    return team


def queryTeam(args):
    if "teamURI" in args:
        return {"singleTeam": args["teamURI"]}

    with requests.Session() as req:
        endpoint = "/teams/events/rankings/"
        teamDict = {}
        r = req.get(BASE_URL + endpoint)
        soup = BeautifulSoup(r.content, 'html.parser')

        data = setArgs(args)
        data['__VIEWSTATE'] = soup.find("input", id="__VIEWSTATE").get("value")
        data['__VIEWSTATEGENERATOR'] = soup.find("input", id="__VIEWSTATEGENERATOR").get("value")
        data['__EVENTVALIDATION'] = soup.find("input", id="__EVENTVALIDATION").get("value")
        r = req.post(BASE_URL + endpoint, data=data)
        soup = BeautifulSoup(r.content, 'html.parser')

        links = soup.findAll(id=re.compile("lnkTeam"))

        for link in links:
            teamDict[link.getText()] = link.get("href")

        return teamDict


def setArgs(args):
    designation_mappings = {
        "Gender": {"Boys": 20, "Girls": 19, "Men": 17, "Mixed": 1, "Women": 2},
        "Division": {"Classic": 10, "Developmental": 4, "Division 1": 1, "Division 3": 3},
        "Designation": {"B": 1, "C": 2},
    }

    checkArgs(designation_mappings, args)

    data = {
        "__EVENTTARGET": "CT_Main_0$gvList$ctl23$ctl00$ctl00",
        "CT_Main_0$F_Status": "Published",
        "CT_Main_0$F_SchoolName": args["schoolName"] if "schoolName" in args else "",
        "CT_Main_0$F_TeamName": args["teamName"] if "teamName" in args else "",
        "CT_Main_0$F_GenderDivisionId": designation_mappings["Gender"][args["genderDivision"]]
        if "genderDivision" in args
        else "",
        "CT_Main_0$F_StateId": args["state"] if "state" in args else "",
        "CT_Main_0$F_CompetitionLevelId": args["competitionLevel"] if "competitionLevel" in args else "",
        "CT_Main_0$F_CompetitionDivisionId": designation_mappings["Division"][args["competitionDivision"]]
        if "competitionDivision" in args
        else "",
        "CT_Main_0$F_Designation": designation_mappings["Designation"][args["teamDesignation"]]
        if "teamDesignation" in args
        else "",
    }

    return data


def checkArgs(designation_mappings, args):
    if "genderDivision" in args:
        if args["genderDivision"] not in designation_mappings["Gender"]:
            raise ValueError("Gender Division must be one of: Boys, Girls, Men, Mixed, Women")

    if "competitionDivision" in args:
        if args["competitionDivision"] not in designation_mappings["Division"]:
            raise ValueError("Competition Division must be one of: Classic, Developmental, Division 1, Division 3")

    if "teamDesignation" in args:
        if args["teamDesignation"] not in designation_mappings["Designation"]:
            raise ValueError("Competition Designation must be B or C")

    if "competitionLevel" in args:
        if args["competitionLevel"] not in ["Club", "College", "High School", "Middle School"]:
            raise ValueError("Competition Level must be one of: Club, College, High School, Middle School")
