<p align="center">
<img width="500" alt="USAU logo surrounded by data icons" src="https://user-images.githubusercontent.com/16248113/235183543-063d7200-5dcb-491d-bdbe-2eeaea6b5eee.png">
</p>

The USAU scraper is a data collector that allows developers to easily aggregate and use team results, rosters, and schedule data from the [USAU website](https://play.usaultimate.org/events/tournament/?ViewAll=false&IsLeagueType=false&IsClinic=false&FilterByCategory=AE).

![Apache Liscence](https://img.shields.io/github/license/erin2722/usau-scraper?color=f72d2d)

[![PyPI](https://img.shields.io/pypi/v/usau-scraper?color=2d2df7)](https://pypi.org/project/usau-scraper/)

[![Docs](https://img.shields.io/badge/documentation-gh%20pages-%23fffb03)](https://erin2722.github.io/usau-scraper/)
[![Collab Example](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/erin2722/usau-scraper/blob/main/examples/usau_scraper_example.ipynb)

[![Build Status](https://github.com/erin2722/usau-scraper/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/erin2722/usau-scraper/actions?query=workflow%3A%22Build+Status%22)
![Open Issues](https://img.shields.io/github/issues/erin2722/usau-scraper?color=f79502)
[![codecov](https://codecov.io/gh/erin2722/usau-scraper/branch/main/graph/badge.svg)](https://codecov.io/gh/erin2722/usau-scraper)

## Overview

USAU (USA Ultimate) is the governing body of ultimate frisbee, and its website (which is notoriously hard to navigate) contains all of the information about high school, college, and club ultimate frisbee teams. Right now, there is no easy way to access this data. USAU scraper solves this problem by scraping the USAU website for data and therefore allowing other developers to easily use the data on the USAU site. This project will open the door to more data analytic projects concerning ultimate frisbee.

## Installation

`pip install --upgrade usau-scraper`

## Example Usage

```python
from usau_scraper import *

# Get a team's basic information
print(getTeamInfo(
    schoolName = 'Columbia',
    teamName = 'Baewatch',
    genderDivision='Women',
    state='NY',
    competitionLevel='College',
    competitionDivision='Division 1',
    teamDesignation='B'))

# Get a team's schedule for the current season
print(getTeamSchedule(schoolName='Columbia', teamName='Curbside'))

# Get a team's roster for the current season
print(getTeamRoster(schoolName='Columbia', teamName='Curbside'))

# Get the pool play results for a tournament
print(getTournamentPoolPlayResults("College", "Women", eventName="No Sleep Till Brooklyn", season=2023))

# Get the bracket results for a tournament
print(getTournamentBracketResults("College", "Women", eventName="Centex", season=2022))

# Get the winner for a tournament
print(getTournamentWinner("College", "Women", eventName="Stanford Invite", season=2023))

# Get the top 20 women's college teams
print(getCollegeRankings(genderDivision="Women"))

# Get the top 20 women's club teams
print(getClubRankings(genderDivision="Women"))
```

Additional usage examples are [in this notebook](https://colab.research.google.com/github/erin2722/usau-scraper/blob/main/examples/usau_scraper_example.ipynb#scrollTo=20Fjgtxr35ES).

## Features (MVP)

- [x] A function that, given a team name, returns basic information about them.
- [x] A function that, given a team name, returns their schedule and record.
- [x] A function that, given a team name, returns its roster.
- [x] A function that, given a tournament name, returns the results of the tournament.

## Additional features

- [x] A function that, given a college division, returns the current standings of that division.
- [ ] An additional plugin to ultiworld to show recent articles given a team name or college division.
- [ ] More features tbd!

## Possible Applications

- A seeding helper that, given a list of team names, returns their records for the season and their record against top 25 teams.
