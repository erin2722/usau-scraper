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
}

def buildTeamIdDict():
    with requests.Session() as req:
        url = "https://play.usaultimate.org/teams/events/rankings/"
        teamDict = {}

        for i in range(0, 10):
            r = req.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            data["__EVENTTARGET"] = "CT_Main_0$gvList$ctl23$ctl00$ctl0" + str(i)
            data['__VIEWSTATE'] = soup.find("input", id="__VIEWSTATE").get("value")
            data['__VIEWSTATEGENERATOR'] = soup.find("input", id="__VIEWSTATEGENERATOR").get("value")
            data['__EVENTVALIDATION'] = soup.find("input", id="__EVENTVALIDATION").get("value")
            r = req.post(url, data=data)

            soup = BeautifulSoup(r.content, 'html.parser')
            links = soup.findAll(id=re.compile("lnkTeam"))

            for link in links:
                teamDict[link.getText()] = link.get("href")[32:]
        
        f = open("usau-scraper/data/team_dict.json", "w")
        f.write(json.dumps(teamDict, indent=4))
        f.close()

        return teamDict
        