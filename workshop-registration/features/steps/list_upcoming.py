from unittest.mock import Mock
from behave import given, when, then
from app import WorkshopRecord, RegistrationRecord

@given(u'{person} has workshops {workshop_ids}')
def step_impl(context, person, workshop_ids):
    if workshop_ids == "-":
        return
    for workshop_id in workshop_ids.split(','):
        workshop = WorkshopRecord(
            id=workshop_id,
            link=Mock(),
            title=Mock(),
            date=Mock(),
            capacity=20,
        )
        context.workshop_repo.add_workshop(workshop)

@given(u'one workshop with registration link "{link}", title "{title}", and date "{date}"')
def step_impl(context, link, title, date):
    workshop = WorkshopRecord(
        link=link, 
        title=title, 
        date=date,
        capacity=20,
        )
    context.workshop_repo.add_workshop(workshop)

@given(u'the following workshops exist')
def step_impl(context):
    for row in context.table:
        workshop = WorkshopRecord(
            link=row["link"], 
            title=row["title"], 
            date=row["date"],
            capacity=20,
            )
        context.workshop_repo.add_workshop(workshop)


@given(u'the following people registered for workshop at link "{link}" with a capacity of {capacity:d} participants')
def step_impl(context, link, capacity):
    workshop = WorkshopRecord(
        link=link, 
        title=Mock(),
        date=Mock(),
        capacity=capacity)
    context.workshop_repo.add_workshop(workshop)
    for row in context.table:
        registration = RegistrationRecord(
            workshop_id=workshop.id,
            name=row['name'],
            status=row['status'],
            email=Mock(),
            registered_on=Mock(),
            custom_questions=Mock(),
        )
        context.registration_repo.add_registration(registration)


@when(u'the user checks upcoming workshops')
def step_impl(context):
    context.app.check_upcoming_workshops()


@then(u'they see a list containing workshops {workshop_ids}')
def step_impl(context, workshop_ids):
    if workshop_ids == '-':
        return
    for workshop_id in workshop_ids.split(','):
        upcoming_workshops = context.presenter.show.call_args[1]['upcoming_workshops']
        assert any(workshop_id == w.id for w in upcoming_workshops)


@then(u'they see workshops\' details ("{link}", "{title}", "{date}")')
def step_impl(context, link, title, date):
    upcoming_workshops = context.presenter.show.call_args[1]['upcoming_workshops']
    assert upcoming_workshops[0].link == link
    assert upcoming_workshops[0].title == title
    assert upcoming_workshops[0].date == date


@then(u'they see the following workshops\' details')
def step_impl(context):
    upcoming_workshops = context.presenter.show.call_args[1]['upcoming_workshops']
    for observed, expected in zip(upcoming_workshops, context.table):
        assert observed.link == expected['link']
        assert observed.title == expected['title']
        assert observed.date == expected['date']


@then(u'they see the following worshops registration summary')
def step_impl(context):
    upcoming_workshops = context.presenter.show.call_args[1]['upcoming_workshops']
    for observed, expected in zip(upcoming_workshops, context.table):
        assert observed.link == expected['link']
        assert observed.num_approved == int(expected['num_approved'])
        assert observed.num_waitlisted == int(expected['num_waitlisted'])
        assert observed.num_rejected == int(expected['num_rejected'])
        assert observed.num_free_spots == int(expected['num_free_spots'])
