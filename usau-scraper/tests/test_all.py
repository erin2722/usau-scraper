from usau-scraper import buildTeamIdDict
from unittest.mock import patch


def test_build_team_ids():
    df = buildTeamIdDict()
