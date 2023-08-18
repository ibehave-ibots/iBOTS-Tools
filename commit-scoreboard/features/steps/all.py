from behave import given, when, then


######################
## Givens

@given(u'the interval setting for {team} is set to {interval:d}')
def step_impl(context, team, interval):
    context.app.model.settings[team].interval = interval


@given(u'that {team} already had {points:d} points')
def step_impl(context, team, points):
    context.app.model.statuses[team].points = points
    
@given(u'the {team} branch is {n:d} commits ahead of the reference {ref} branch')
def step_impl(context, team, ref, n):
    context.vcs.branch_commits = {ref: 0, team: n}
    
##################
## Whens 

@when(u'the {team} gets {points:d} points')
def step_impl(context, team, points):
    context.app.model.statuses[team].active_branch = team
    context.app.model.reference_branch = 'main'
    context.vcs.branch_commits = {context.app.model.reference_branch: 0, team: points}
    context.app.update_points()

    
@when(u'the scores are calculated for teams {team} against reference branch {ref}')
def step_impl(context, team, ref):
    context.app.model.statuses[team].active_branch = team
    context.app.model.reference_branch = ref
    context.app.update_points()
    
####################
## Thens

@then(u'the {team} ding sound should be {status}')
def step_impl(context, team, status):
    is_on = {'on': True, 'off': False}[status]
    display = context.display.update.call_args[1]['model']
    assert display.statuses[team].play_sound == is_on
    if is_on:
        context.speaker.play_team_sound.assert_called_with(team=team)
    else:
        context.speaker.play_team_sound.assert_not_called()


@then(u'{team} is shown to have a score of {x:d}')
def step_impl(context, team, x):
    display = context.display.update.call_args[1]['model']
    assert display.statuses[team].points == x