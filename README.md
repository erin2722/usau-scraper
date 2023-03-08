# USAU Scraper

The USAU scraper is a data collector that allows developers to easily aggregate and use team results, rosters, and schedule data from the [USAU website](https://play.usaultimate.org/events/tournament/?ViewAll=false&IsLeagueType=false&IsClinic=false&FilterByCategory=AE).

![Apache Liscence](https://img.shields.io/github/license/erin2722/usau-scraper) 
![Open Issues](https://img.shields.io/github/issues/erin2722/usau-scraper?color=blue)
[![Build Status](https://github.com/erin2722/usau-scraper/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/ColumbiaOSS/example-project-python/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/erin2722/usau-scraper/branch/main/graph/badge.svg)](https://codecov.io/gh/erin2722/usau-scraper)

## Overview

USAU (USA Ultimate) is the governing body of ultimate frisbee, and its website (which is notoriously hard to navigate) contains all of the information about high school, college, and club ultimate frisbee teams. Right now, there is no easy way to access this data. USAU scraper solves this problem by scraping the USAU website for data and therefore allowing other developers to easily use the data on the USAU site. This project will open the door to more data analytic projects concerning ultimate frisbee.

### Features (MVP)

- [x] A function that, given a team name, returns basic information about them.
- [x] A function that, given a team name, returns their schedule and record.
- [x] A function that, given a team name, returns its roster.
- [ ] A function that, given a tournament name, returns the results of the tournament.

### Additional features

- [ ] A function that, given a college division, returns the current standings of that division.
- [ ] An additional plugin to ultiworld to show current top 25 teams.
- [ ] An additional plugin to ultiworld to show recent articles given a team name or college division.
- [ ] More features tbd!

### Possible Applications

- A seeding helper that, given a list of team names, returns their records for the season and their record against top 25 teams.
