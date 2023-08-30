from unittest.mock import Mock
from behave import given, when, then
from registration import Workshop

@given(u'Mohammad has an workshop {Mohammad} and Sangeetha has an workshop {Sangeetha}')
def step_impl(context, Mohammad, Sangeetha):
    for workshop_id in Mohammad.split(',') + Sangeetha.split(','):
        workshop = Workshop(
            id=workshop_id,
            link=Mock(),
            title=Mock(),
            date=Mock(),
        )
        context.workshop_repo.add_workshop(workshop)
    

@given(u'one workshop with registration link "{link}", title "{title}", and date "{date}"')
def step_impl(context, link, title, date):
    workshop = Workshop(link=link, title=title, date=date)
    context.workshop_repo.add_workshop(workshop)

@given(u'the following workshops exist')
def step_impl(context):
    for row in context.table:
        workshop = Workshop(link=row["link"], title=row["title"], date=row["date"])
        context.workshop_repo.add_workshop(workshop)


@when(u'the user checks upcoming workshops')
def step_impl(context):
    context.app.check_upcoming_workshops()



@then(u'they see a list containing workshops {Mohammad} and {Sangeetha}')
def step_impl(context, Mohammad, Sangeetha):
    for workshop_id in Mohammad.split(',') + Sangeetha.split(','):
        assert any(workshop_id == w.id for w in context.app.model.upcoming_workshops)


@then(u'they see workshops\' details ("{link}", "{title}", "{date}")')
def step_impl(context, link, title, date):
    assert context.app.model.upcoming_workshops[0].link == link
    assert context.app.model.upcoming_workshops[0].title == title
    assert context.app.model.upcoming_workshops[0].date == date


@then(u'they see the following workshops\' details')
def step_impl(context):
    for observed, expected in zip(context.app.model.upcoming_workshops, context.table):
        assert observed.link == expected['link']
        assert observed.title == expected['title']
        assert observed.date == expected['date']

