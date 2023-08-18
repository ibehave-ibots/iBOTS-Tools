from unittest.mock import Mock
from behave import given, when, then

from scoreboard.app import TeamSettings, AppModel, Application, TeamState, ScoreboardView


@given(u'the interval setting for {team} is set to {interval:d}')
def step_impl(context, team, interval):
    settings = {
        team: TeamSettings(interval=interval)
    }
    context.settings = settings

@given(u'that {team} already had {points:d} points')
def step_impl(context, team, points):
    context.display = Mock(ScoreboardView)
    context.app = Application(
        model=AppModel(
            statuses={team: TeamState(points=points)},
            settings=context.settings,
        ),
        view = context.display
    )


@when(u'the {team} gets {points:d} points')
def step_impl(context, team, points):    
    context.app.update_points(team, points)


@then(u'the {team} ding sound should be {status}')
def step_impl(context, team, status):
    is_on = {'on': True, 'off': False}[status]
    display = context.display.update.call_args[1]['model']
    assert display.statuses[team].play_sound == is_on
