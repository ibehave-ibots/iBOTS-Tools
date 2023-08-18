from unittest.mock import Mock
from behave import given, when, then

from scoreboard.app import TeamSettings, AppModel, Application, TeamState, ScoreboardView
from scoreboard.vcs_repos import DummyVersionControlRepo


@given(u'the interval setting for {team} is set to {interval:d}')
def step_impl(context, team, interval):
    context.app.model.settings[team].interval = interval


@given(u'that {team} already had {points:d} points')
def step_impl(context, team, points):
    context.app.model.statuses[team].points = points
    

@when(u'the {team} gets {points:d} points')
def step_impl(context, team, points):
    context.app.model.statuses[team].active_branch = team
    context.app.model.reference_branch = 'main'
    context.vcs.branch_commits = {context.app.model.reference_branch: 0, team: points}
    context.app.update_points()


@then(u'the {team} ding sound should be {status}')
def step_impl(context, team, status):
    is_on = {'on': True, 'off': False}[status]
    display = context.display.update.call_args[1]['model']
    assert display.statuses[team].play_sound == is_on
