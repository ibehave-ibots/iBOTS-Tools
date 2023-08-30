from behave import given, when, then

@given(u'Mohammad has an upcoming workshop {Mohammad} and Sangeetha has an upcoming workshop {Sangeetha}')
def step_impl(context, Mohammad, Sangeetha):
    context.workshop_repo.add_workshop(Mohammad)
    context.workshop_repo.add_workshop(Sangeetha)
    

@when(u'the user checks upcoming workshops')
def step_impl(context):
    context.app.check_upcoming_workshops()


@then(u'they see a list containing workshops {Mohammad} and {Sangeetha}')
def step_impl(context, Mohammad, Sangeetha):
    for workshop in [Mohammad, Sangeetha]:
        assert any(workshop == w.id for w in context.app.model.upcoming_workshops)