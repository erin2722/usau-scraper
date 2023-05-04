"""
.. module:: tournamentScraper
   :synopsis: A module for scraping tournament results

.. moduleauthor:: Erin McNulty
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

BASE_URL = "https://play.usaultimate.org"


def getTournamentPoolPlayResults(competitionLevel, genderDivision, **kwargs):
    '''getTournamentPoolPlayResults() returns the pool play and consolation results of a tournament.

        If the query returns multiple tournaments, returns the result of the first tournament that
        appears on the usau site which the query is issued.

    Args:
        ``competitionLevel`` (string) (required): The competition level of the tournament.
        Must be one of: Club, College, or High School.

        ``genderDivision`` (string) (required): The gender division to view tournament results for.
        Must be one of: Women, Men, Mixed, Boys, Girls.

        ``eventName`` (string): The name of the tournament.

        ``state`` (string): Postal abbreviation of the state the tournament was in.

        ``season`` (int): The season that the tournament occured in.
        Must be after 2006

    Returns:
        results:
            ::

                {
                    res: OK, NOTFOUND
                    tournamentName: {
                        pools: {
                            poolName: [
                                {
                                    name,
                                    wins,
                                    losses
                                },
                                ...
                            ],
                            ...
                        },
                        rounds: {
                            roundName: {
                                sectionName: [
                                    {
                                        date,
                                        time,
                                        field,
                                        team1Name,
                                        team2Name,
                                        score,
                                        status
                                    },
                                    ...
                                ]
                            }
                        }
                    }
                }


    '''
    tournamentName, tournamentLink = queryTournament(competitionLevel, genderDivision, kwargs)

    if tournamentName == '':
        return {"res": "NOTFOUND"}

    with requests.Session() as req:
        response = {"res": "OK"}
        response[tournamentName] = {}
        response[tournamentName]["pools"] = {}
        response[tournamentName]["rounds"] = {}

        r = req.get(tournamentLink + "/schedule/" + genderDivision + "/" + competitionLevel + genderDivision)
        soup = BeautifulSoup(r.content, 'html.parser')

        roundNames = soup.find_all(id=re.compile("CT_Main_0_rptTabs_ctl.._liTab"))
        index2RoundName = []

        for listItem in roundNames:
            roundName = listItem.find("a").getText()
            response[tournamentName]["rounds"][roundName] = {}
            index2RoundName.append(roundName)

        roundResultsDiv = soup.find("div", {"class": "slides"})
        roundResults = roundResultsDiv.find_all("section", {"class": "slide"})

        i = 0
        for roundResult in roundResults:
            if roundResult.get("id") == "poolSlide":
                # ----------------- Add in pool results to pool play -------------------
                pools = roundResult.find_all("div", {"class": "pool"})

                for pool in pools:
                    poolName = pool.find("h3").getText()
                    response[tournamentName]["pools"][poolName] = []

                    poolTable = pool.find("table")
                    poolResults = pd.read_html(str(poolTable), na_values=None)

                    for poolResult in poolResults:
                        response[tournamentName]["pools"][poolName] = poolResult.to_dict("records")

                # ----------------- Add in non-bracket results -------------------
                sections = roundResult.find_all("table", {"class": "scores_table"})

                for section in sections:
                    sectionName = section.find("th").getText()
                    sectionResults = pd.read_html(str(section), header=0, na_values=None)

                    for sectionResult in sectionResults:
                        sectionResult.columns = sectionResult.iloc[0]
                        sectionResult = sectionResult[1:]
                        sectionResult = sectionResult.drop("Options", axis=1)
                        response[tournamentName]["rounds"][index2RoundName[i]][sectionName] = sectionResult.to_dict(
                            "records"
                        )

            if response[tournamentName]["rounds"][index2RoundName[i]] == {}:
                del response[tournamentName]["rounds"][index2RoundName[i]]

            i += 1

        return response


def getTournamentBracketResults(competitionLevel, genderDivision, **kwargs):
    '''getTournamentBracketResults() returns the bracket results of a tournament.

    If the query returns multiple tournaments, returns the result of the first tournament that
    appears on the usau site which the query is issued.

    Args:
        ``competitionLevel`` (string) (required): The competition level of the tournament.
        Must be one of: Club, College, or High School.

        ``genderDivision`` (string) (required): The gender division to view tournament results for.
        Must be one of: Women, Men, Mixed, Boys, Girls.

        ``eventName`` (string): The name of the tournament.

        ``state`` (string): Postal abbreviation of the state the tournament was in.

        ``season`` (int): The season that the tournament occured in.
        Must be after 2006

    Returns:
        results:
            ::

                {
                    res: OK, NOTFOUND
                    tournamentName: {
                        bracketName: {
                            roundName: [
                                {
                                    date,
                                    time,
                                    field,
                                    winner,
                                    loser,
                                    score,
                                    status
                                },
                                ...
                            ]
                        }
                    }
                }
    '''
    tournamentName, tournamentLink = queryTournament(competitionLevel, genderDivision, kwargs)

    if tournamentName == '':
        return {"res": "NOTFOUND"}

    with requests.Session() as req:
        response = {"res": "OK"}
        response[tournamentName] = {}

        r = req.get(tournamentLink + "/schedule/" + genderDivision + "/" + competitionLevel + genderDivision)
        soup = BeautifulSoup(r.content, 'html.parser')

        roundResults = soup.find("div", {"class": "slides"}).find_all("section", {"class": "slide"})

        for roundResult in roundResults:
            if roundResult.get("id") == "bracketSlide":
                # -------------- Add in bracket results --------------------
                sections = roundResult.find_all("section", {"class": "section page"})

                for section in sections:
                    sectionName = section.find("h3").getText().strip()
                    response[tournamentName][sectionName] = {}

                    rounds = section.find_all("div", {"class": "bracket_col"})

                    for r in rounds:
                        roundName = r.find("h4").getText()
                        response[tournamentName][sectionName][roundName] = []

                        games = r.find_all("div", {"class": "bracket_game"})

                        for game in games:
                            status = game.find("span", {"class": "game-status"}).getText()

                            if status == "Final":
                                date, time, am_pm = game.find("span", {"class": "date"}).getText().split(" ")
                                time = time + am_pm
                                field = game.find("p", {"class": "location"}).getText()
                                winnerDiv = game.find("div", {"class": "winner"})
                                loserDiv = game.find("div", {"class": "loser"})
                                winner = winnerDiv.find("span", {"class": "isName"}).find("a").getText()
                                loser = loserDiv.find("span", {"class": "isName"}).find("a").getText()
                                scoreW = winnerDiv.find("span", {"class": "isScore"}).getText().strip()
                                scoreL = loserDiv.find("span", {"class": "isScore"}).getText().strip()
                                score = scoreW + " - " + scoreL

                                gameDict = {
                                    "date": date,
                                    "time": time,
                                    "field": field,
                                    "winner": winner,
                                    "loser": loser,
                                    "score": score,
                                    "status": status,
                                }

                                response[tournamentName][sectionName][roundName].append(gameDict)

        return response


def getTournamentWinner(competitionLevel, genderDivision, **kwargs):
    '''getTournamentWinner() returns the first and second place results of a tournament.

    If the query returns multiple tournaments, returns the result of the first tournament that
    appears on the usau site which the query is issued.

    Args:
        ``competitionLevel`` (string) (required): The competition level of the tournament.
        Must be one of: Club, College, or High School.

        ``genderDivision`` (string) (required): The gender division to view tournament results for.
        Must be one of: Women, Men, Mixed, Boys, Girls.

        ``eventName`` (string): The name of the tournament.

        ``state`` (string): Postal abbreviation of the state the tournament was in.

        ``season`` (int): The season that the tournament occured in.
        Must be after 2006

    Returns:
        results:
            ::

                {
                    res: OK, NOTFOUND
                    tournamentName: {
                        firstPlace,
                        secondPlace
                    }
                }
    '''
    bracketPlayResults = getTournamentBracketResults(competitionLevel, genderDivision, **kwargs)

    if bracketPlayResults["res"] == "NOTFOUND":
        return bracketPlayResults

    tournamentName = list(bracketPlayResults)[1]
    firstBracket = list(bracketPlayResults[tournamentName])[0]
    firstGame = list(bracketPlayResults[tournamentName][firstBracket])[0]

    tournamentResDict = {
        "firstPlace": bracketPlayResults[tournamentName][firstBracket][firstGame][0]["winner"],
        "secondPlace": bracketPlayResults[tournamentName][firstBracket][firstGame][0]["loser"],
    }

    res = {"res": "OK"}
    res[tournamentName] = tournamentResDict

    return res


def queryTournament(competitionLevel, genderDivision, args):
    if "tournamentURI" in args:
        return {"singleTournament": args["tournamentURI"]}

    with requests.Session() as req:
        endpoint = "/events/tournament/"

        r = req.get(BASE_URL + endpoint, params=setArgs(competitionLevel, genderDivision, args))
        soup = BeautifulSoup(r.content, 'html.parser')

        tournaments = soup.find("div", {"class": "search-results"}).findChildren("tr")

        if len(tournaments) > 1:
            tournamentName = tournaments[1].find("a").getText()
            tournamentLink = tournaments[1].find("a").get("href")

            return tournamentName, tournamentLink

        return '', ''


def seasonToId(season):
    if season > 2018:
        return season - 2005
    elif season > 2010:
        return season - 2010
    else:
        return 2019 - season


def setArgs(competitionLevel, genderDivision, args):
    designation_mappings = {
        'College - Mixed': 4,
        'College - Women': 28,
        'College - Men': 27,
        'High School - Mixed': 3,
        'High School - Girls': 30,
        'High School - Boys': 29,
        'Club - Women': 22,
        'Club - Mixed': 7,
        'Club - Men': 21,
    }

    checkArgs(competitionLevel, genderDivision, args)

    competitionLevelId = designation_mappings[competitionLevel + " - " + genderDivision]

    queryParams = {
        'ViewAll': 'true',
        'IsLeagueType': 'false',
        'IsClinic': 'false',
        'FilterByCategory': 'AT',
        'CompetitionLevelId': competitionLevelId,
        'SeasonId': seasonToId(args["season"]) if "season" in args else "",
        'EventName': args["eventName"] if "eventName" in args else "",
        'DateFrom': args["dateFrom"] if "dateFrom" in args else "",
        'DateTo': args["dateTo"] if "dateTo" in args else "",
    }

    return queryParams


def checkArgs(competitionLevel, genderDivision, args):
    if genderDivision not in ['Boys', 'Girls', 'Men', 'Mixed', 'Women']:
        raise ValueError("Gender Division must be one of: Boys, Girls, Men, Mixed, Women")

    if competitionLevel not in ["Club", "College", "High School"]:
        raise ValueError("Competition Level must be one of: Club, College, High School")

    if "season" in args:
        if args["season"] < 2006:
            raise ValueError("Season must be after 2006")
