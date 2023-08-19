import pytest
from hypothesis import given
from hypothesis.strategies import text

from scoreboard.core.app import AppModel



@given(team_name=text())
def test_can_add_new_teams_directly(team_name):
    model = AppModel()
    assert team_name not in model.statuses
    assert team_name not in model.settings

    model.add_team(team_name)
    assert team_name in model.statuses
    assert team_name in model.settings


@pytest.mark.parametrize('interval', [1, 2, 3, 4, 5])
def test_can_specify_interval_when_adding_team(interval):
    model = AppModel()
    model.add_team('example team', interval=interval)
    assert model.settings['example team'].interval == interval


@pytest.mark.parametrize('points', [1, 2, 3, 4, 5])
def test_can_specify_starting_points_when_adding_team(points):
    model = AppModel()
    model.add_team('example team', points=points)
    assert model.statuses['example team'].points == points