.. usau-scraper documentation master file, created by
   sphinx-quickstart on Sun Apr  2 21:26:33 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

usau-scraper documentation
===========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Installation
===================================
:code:`pip install usau-scraper`

How to Use
===================================
After installing the library, there are currently 3 functions available for use:
``getTeamInfo``, ``getTeamSchedule``, and ``getTeamRoster``.

Simply :code:`import * from usau_scraper`, and get started!

More extensive module documentation is here:
:ref:`modules`

Example Usage
===================================
After :code:`pip install --upgrade usau-scraper` in your python env:

::

   from usau_scraper import getTeamInfo, getTeamSchedule, getTeamRoster

   # Get a team's basic information
   print(getTeamInfo(
      schoolName = 'Columbia', 
      teamName = 'Baewatch', 
      genderDivision=2, 
      state='NY', 
      competitionLevel='College', 
      competitionDivision=1, 
      teamDesignation=1))

   # Get a team's schedule for the current season
   print(getTeamSchedule(schoolName='Columbia', teamName='Curbside'))

   # Get a team's roster for the current season
   print(getTeamRoster(schoolName='Columbia', teamName='Curbside'))

Additional usage examples are `in this notebook <https://colab.research.google.com/github/erin2722/usau-scraper/blob/main/examples/usau_scraper_example.ipynb#scrollTo=rEfGbe_ruqk4>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
