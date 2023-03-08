# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import re
# import json


'''
Input: eventName, competitionLevel, genderDivision, competitionDivision, state

Output:
{
    res: OK, NOTFOUND
    tournaments: [
        {
            name,
            pools: [
                {
                    poolName,
                    teams: [
                        {
                            name,
                            wins,
                            losses
                        },
                        ...
                    ],
                    games: [
                        {
                            time,
                            team1Name,
                            team2Name,
                            score
                        },
                        ...
                    ]
                }
            ]
        }
    ]
}


'''


def getTournamentPoolPlayResults():
    pass


'''
Input: eventName, competitionLevel, genderDivision, competitionDivision, state

Output:
{
    res: OK, NOTFOUND
    tournaments: [
        {
            name,
            firstPlace,
            secondPlace
        },
        ...
    ]
'''


def getTournamentWinner():
    pass
