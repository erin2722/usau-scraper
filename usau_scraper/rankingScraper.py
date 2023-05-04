"""
.. module:: rankingScraper
   :synopsis: A module for scraping team rankings.

.. moduleauthor:: Cherie Liu
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://play.usaultimate.org"


def getCollegeRankings(**kwargs):
    '''getCollegeRankings() returns top 20 teams for inputted gender at the college competition level.

    Args:
        ``genderDivision`` (string): Women, Men, or Mixed (for Club only)

    Returns:
        results:
            ::

                {
                    res: OK, NOTFOUND
                    teams: [
                        {
                            rank,
                            team,
                            powerRating,
                            competitionLevel,
                            genderDivison,
                            competitionDivision,
                            collegeRegion,
                            collegeConference,
                            wins,
                            losses
                        },
                        ...
                    ]
                }
    '''
    kwargs["competitionLevel"] = "College"
    teams = queryRankings(kwargs)
    if len(teams) == 0:
        return {"res": "NOTFOUND"}
    else:
        return {"res": "OK", "teams": teams}


def getClubRankings(**kwargs):
    '''getClubRankings() returns top 20 teams for inputted gender at the club competition level.

    Args:
        ``genderDivision`` (string): Women, Men, or Mixed (for Club only)

    Returns:
        results:
            ::

                {
                    res: OK, NOTFOUND
                    teams: [
                        {
                            rank,
                            team,
                            powerRating,
                            genderDivison,
                            competitionDivision,
                            city,
                            state,
                            clubRegion,
                            clubSection,
                            wins,
                            losses
                        },
                        ...
                    ]
                }
    '''
    kwargs["competitionLevel"] = "Club"
    teams = queryRankings(kwargs)
    if len(teams) == 0:
        return {"res": "NOTFOUND"}
    else:
        return {"res": "OK", "teams": teams}


def queryRankings(args):
    with requests.Session() as req:
        endpoint = "/teams/events/team_rankings/?RankSet=" + args["competitionLevel"] + "-" + args["genderDivision"]
        r = req.get(BASE_URL + endpoint)
        soup = BeautifulSoup(r.content, 'html.parser')

        r = req.post(BASE_URL + endpoint)
        soup = BeautifulSoup(r.content, 'html.parser')

        table = soup.find('table', id="CT_Main_0_gvList")
        dfs = pd.read_html(str(table))[0].head(20)
        teamsDict = dfs.to_dict('records')

        return teamsDict
