import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json


BASE_URL = "https://play.usaultimate.org"

'''
getTeamInfo() returns all information about the first 10 teams matching the query

Input: schoolName, teamName, genderDivision, state, competitionLevel, competitionDivision, teamDesignation as named arguments

Output: 
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
            wins,
            losses,
        },
        ...
    ]
}

'''
def getTeamInfo(
    schoolName = None, 
    teamName = None, 
    genderDivision = None, 
    state = None, 
    competitionLevel = None, 
    competitionDivision = None, 
    teamDesignation = None):
    pass

'''
getTeamSchedule() returns the season schedule and record of the first 10 teams matching the query

Input: schoolName, teamName, genderDivision, state, competitionLevel, competitionDivision, teamDesignation as named arguments

Output: 
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
            tournaments: [
                {
                    name,
                    games: [
                        {
                            date,
                            score,
                            opponent
                        },
                        ...
                    ]
                },
                ...
            ]
        },
        ...
    ]
}
'''
def getTeamSchedule(
    schoolName = None, 
    teamName = None, 
    genderDivision = None, 
    state = None, 
    competitionLevel = None, 
    competitionDivision = None, 
    teamDesignation = None):
    pass


'''
getTeamRoster() returns the roster of the first 10 teams matching the query

Input: schoolName, teamName, genderDivision, state, competitionLevel, competitionDivision, teamDesignation as named arguments

Output: 
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
            roster: [
                {
                    no,
                    name,
                    pronouns,
                    position,
                    year,
                    height,
                    points,
                    assists,
                    ds,
                    turns
                },
                ...
            ]
        },
        ...
    ]
}
'''
def getTeamRoster(
    schoolName = None, 
    teamName = None, 
    genderDivision = None, 
    state = None, 
    competitionLevel = None, 
    competitionDivision = None, 
    teamDesignation = None):
    pass


def queryTeam(**kwargs):
    with requests.Session() as req:
        endpoint = "/teams/events/rankings/"
        data = setArgs(kwargs)
        teamDict = {}
        r = req.get(BASE_URL + endpoint)
        soup = BeautifulSoup(r.content, 'html.parser')
        data['__VIEWSTATE'] = soup.find("input", id="__VIEWSTATE").get("value")
        data['__VIEWSTATEGENERATOR'] = soup.find("input", id="__VIEWSTATEGENERATOR").get("value")
        data['__EVENTVALIDATION'] = soup.find("input", id="__EVENTVALIDATION").get("value")
        r = req.post(BASE_URL + endpoint, data=data)

        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.findAll(id=re.compile("lnkTeam"))

        for link in links:
            teamDict[link.getText()] = link.get("href")
        
        print(json.dumps(teamDict, indent=4))
        
        return teamDict


def setArgs(args):
    # TODO: add input validation
    # TODO: document the mappings from text options => ids and add them in here
    data = {
        "__EVENTTARGET": "CT_Main_0$gvList$ctl23$ctl00$ctl00",
        "CT_Main_0$F_Status": "Published",
        "CT_Main_0$F_SchoolName": args["schoolName"] if "schoolName" in args else "",
        "CT_Main_0$F_TeamName": args["teamName"] if "teamName" in args else "",
        "CT_Main_0$F_GenderDivisionId": args["genderDivision"] if "genderDivision" in args else "",
        "CT_Main_0$F_StateId": args["state"] if "state" in args else "",
        "CT_Main_0$F_CompetitionLevelId": args["competitionLevel"] if "competitionLevel" in args else "",
        "CT_Main_0$F_CompetitionDivisionId": args["competitionDivision"] if "competitionDivision" in args else "",
        "CT_Main_0$F_Designation": args["teamDesignation"] if "teamDesignation" in args else "",
    }

    return data
