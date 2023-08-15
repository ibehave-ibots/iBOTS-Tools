from behave import given, when, then

@given(u'a session id for a session where Nick and Sangeetha attended')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a session id for a session where Nick and Sangeetha attended')


@when(u'the user asks for attendees for that session')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user asks for attendees for that session')


@then(u'they see names of Nick and Sangeetha')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then they see names of Nick and Sangeetha')