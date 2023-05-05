.. usau-scraper documentation master file, created by
   sphinx-quickstart on Sun Apr  2 21:26:33 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

usau-scraper documentation
===========================================

.. image:: ../assets/project-logo.png
  :width: 400
  :align: center
  :alt: USAU logo surrounded by gears

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   developer

Installation
===================================
:code:`pip install --upgrade usau-scraper`

How to Use
===================================
Simply :code:`from usau_scraper import *`, and get started!

More extensive module documentation is here:
:ref:`modules`

Example Usage
===================================
After :code:`pip install --upgrade usau-scraper` in your python env:

::

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

Additional usage examples are `in this notebook <https://colab.research.google.com/github/erin2722/usau-scraper/blob/main/examples/usau_scraper_example.ipynb#scrollTo=rEfGbe_ruqk4>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
