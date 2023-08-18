from unittest.mock import Mock
from behave import given, when, then

from scoreboard.workflow import calculate_scores
from scoreboard.vcs_repos import DummyVersionControlRepo
    
     
@given(u'the {team} branch is {n:d} commits ahead of the reference {ref} branch')
def step_impl(context, team, ref, n):
    branches = {ref: 0, team: n}
    context.vcs = DummyVersionControlRepo(**branches)
    
    
@when(u'the scores are calculated for teams {team} against reference branch {ref}')
def step_impl(context, team, ref):
    context.scores = calculate_scores(
        version_control_repo=context.vcs,
        ref_branch=ref, 
        target_branches=[team],
    )
    


@then(u'{team} is shown to have a score of {x:d}')
def step_impl(context, team, x):
    scoreboard = context.scores
    assert scoreboard[team] == x