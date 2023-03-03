import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

# CT_Main_0$F_GenderDivisionId:
# CT_Main_0$F_CompetitionDivisionId: 
# CT_Main_0$F_StateId: 
# CT_Main_0$F_TeamName: 
# CT_Main_0$F_SchoolName: 
# CT_Main_0$F_Designation: 
# CT_Main_0$F_RankSet: 
# CT_Main_0$F_Name: 
# CT_Main_0$F_RankSetDateLbound$cal: 
# CT_Main_0$F_RankSetDateUbound$cal: 

data = {
    "CT_Main_0$F_CompetitionLevelId": "College",
    "CT_Main_0$F_Status": "Published",
    "CT_Main_0$F_SchoolName": "Columbia",
}

'''
getTeamInfo() returns all information about the first 10 teams matching the query

Input: schoolName, teamName, genderDivision, state, competitionLevel, competitionDivision, teamDesignation

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
def getTeamInfo():
    pass

'''
getTeamSchedule() returns the season schedule and record of the first 10 teams matching the query

Input: schoolName, teamName, genderDivision, state, competitionLevel, competitionDivision, teamDesignation

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
def getTeamSchedule():
    pass


'''
getTeamRoster() returns the roster of the first 10 teams matching the query

Input: schoolName, teamName, genderDivision, state, competitionLevel, competitionDivision, teamDesignation

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
def getTeamRoster():
    pass


