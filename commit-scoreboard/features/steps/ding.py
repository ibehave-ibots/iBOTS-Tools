from collections import defaultdict
from dataclasses import dataclass, field
from unittest.mock import Mock
from behave import given, when, then

from scoreboard.app import TeamSettings, TeamState, AppState    


@given(u'the interval setting for {team} is set to {interval:d}')
def step_impl(context, team, interval):
    settings = {
        team: TeamSettings(interval=interval)
    }
    context.settings = settings

@given(u'that {team} already had {points:d} points')
def step_impl(context, team, points):
    context.app_state = AppState(
        statuses={team: TeamState(points=points)},
        settings=context.settings,
    )
    context.display = Mock()
    context.app_state.register_observer(context.display)


@when(u'the {team} gets {points:d} points')
def step_impl(context, team, points):    
    context.app_state.update_points(team, points)


@then(u'the {team} ding sound should be {status}')
def step_impl(context, team, status):
    is_on = {'on': True, 'off': False}[status]
    view = context.display.call_args[1]['statuses']
    assert view[team].play_sound == is_on
