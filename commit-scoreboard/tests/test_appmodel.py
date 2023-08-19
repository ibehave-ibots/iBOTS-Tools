import pytest
from hypothesis import given
from hypothesis.strategies import text

from scoreboard.core.app import AppModel


@given(team_name=text())
def test_can_get_team_names(team_name):
    model = AppModel.create(team_names=[team_name])
    assert model.team_names == [team_name]


@given(team_name=text())
def test_can_add_new_teams_directly(team_name):
    model = AppModel()
    assert team_name not in model.statuses
    assert team_name not in model.settings

    model.add_team(team_name)
    assert team_name in model.statuses
    assert team_name in model.settings



    