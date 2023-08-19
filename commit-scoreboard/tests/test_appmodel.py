import pytest
from hypothesis import given
from hypothesis.strategies import text

from scoreboard.core.app import AppModel



@given(team_name=text())
def test_can_add_new_teams_directly(team_name):
    model = AppModel()
    assert team_name not in model.statuses
    assert team_name not in model.settings

    model.add_teams(team_name)
    assert team_name in model.statuses
    assert team_name in model.settings


def test_can_add_multiple_teams_at_once():
    teams = ['team-a', 'the bears', 'the browns']
    model = AppModel()
    for team in teams:
        assert team not in model.team_names

    model.add_teams(teams)
    for team in teams:
        assert team in model.team_names


@pytest.mark.parametrize('interval', [1, 2, 3, 4, 5])
def test_can_specify_interval_when_adding_team(interval):
    model = AppModel()
    model.add_teams('example team', interval=interval)
    assert model.settings['example team'].interval == interval


@pytest.mark.parametrize('points', [1, 2, 3, 4, 5])
def test_can_specify_starting_points_when_adding_team(points):
    model = AppModel()
    model.add_teams('example team', points=points)
    assert model.statuses['example team'].points == points