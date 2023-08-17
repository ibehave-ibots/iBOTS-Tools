from behave import given, when, then

def calculate_scores(team_1_commits):
    return 3

@given(u'the reference is the "main" branch')
def step_impl(context):
    context.reference_branch = "main"


@given(u'a team has made 3 commits on the "team-1" branch')
def step_impl(context):
    context.team1_branch_n_commits = 3


@when(u'the scores are calculated')
def step_impl(context):
    context.score = calculate_scores(team_1_commits = context.team1_branch_n_commits) 


@then(u'"team-1" is shown to have a score of 3')
def step_impl(context):
    assert context.score == 3