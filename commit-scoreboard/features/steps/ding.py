from unittest.mock import Mock
from behave import given, when, then

from scoreboard.app import TeamSettings, TeamState, Application    


@given(u'the interval setting for {team} is set to {interval:d}')
def step_impl(context, team, interval):
    settings = {
        team: TeamSettings(interval=interval)
    }
    context.settings = settings

@given(u'that {team} already had {points:d} points')
def step_impl(context, team, points):
    context.display = Mock()
    context.app = Application(
        statuses={team: TeamState(points=points)},
        settings=context.settings,
        view = context.display
    )


@when(u'the {team} gets {points:d} points')
def step_impl(context, team, points):    
    context.app.update_points(team, points)


@then(u'the {team} ding sound should be {status}')
def step_impl(context, team, status):
    is_on = {'on': True, 'off': False}[status]
    display = context.display.update.call_args[1]['statuses']
    assert display[team].play_sound == is_on
