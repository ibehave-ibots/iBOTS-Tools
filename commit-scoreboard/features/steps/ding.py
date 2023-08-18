from unittest.mock import Mock
from behave import given, when, then

from scoreboard.app import TeamSettings, AppModel, Application, TeamState, ScoreboardView
from scoreboard.vcs_repos import DummyVersionControlRepo


@given(u'the interval setting for {team} is set to {interval:d}')
def step_impl(context, team, interval):
    settings = {
        team: TeamSettings(interval=interval)
    }
    context.settings = settings

@given(u'that {team} already had {points:d} points')
def step_impl(context, team, points):
    context.vcs = DummyVersionControlRepo()
    context.display = Mock(ScoreboardView)
    context.app = Application(
        view = context.display,
        model=AppModel(
            settings=context.settings,
            statuses={team: TeamState(active_branch=team, points=points)},
            reference_branch='main',
        ),
        vcs_repo=context.vcs,
    )


@when(u'the {team} gets {points:d} points')
def step_impl(context, team, points):
    context.vcs.branch_commits = {context.app.model.reference_branch: 0, team: points}
    context.app.update_points()


@then(u'the {team} ding sound should be {status}')
def step_impl(context, team, status):
    is_on = {'on': True, 'off': False}[status]
    display = context.display.update.call_args[1]['model']
    assert display.statuses[team].play_sound == is_on
