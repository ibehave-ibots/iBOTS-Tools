from unittest.mock import Mock
from behave import given, when, then


from scoreboard.vcs_repos import DummyVersionControlRepo
from scoreboard.app import TeamSettings, AppModel, Application, TeamState, ScoreboardView

     
@given(u'the {team} branch is {n:d} commits ahead of the reference {ref} branch')
def step_impl(context, team, ref, n):
    branches = {ref: 0, team: n}
    context.vcs = DummyVersionControlRepo(**branches)
    
    
@when(u'the scores are calculated for teams {team} against reference branch {ref}')
def step_impl(context, team, ref):
    context.display = Mock(ScoreboardView)
    context.app = Application(
        view = context.display,
        model=AppModel(
            settings={team: TeamSettings()},
            statuses={team: TeamState(active_branch=team)},
            reference_branch=ref,
        ),
        vcs_repo=context.vcs,
    )
    context.app.update_points()
    


@then(u'{team} is shown to have a score of {x:d}')
def step_impl(context, team, x):
    display = context.display.update.call_args[1]['model']
    display.statuses[team].points == x