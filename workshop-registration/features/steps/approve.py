from behave import given, when, then
from typing import Literal

from unittest.mock import Mock

from app import RegistrationRecord

@given(u'a workshop with the following registrants')
def step_impl(context):
    for row in context.table:
        registration = RegistrationRecord(
            workshop_id='12345',
            name=row['name'],
            custom_questions=[{'value': row['group']}],
            email=row['email'],
            status=row['status'],
            registered_on=row['date'],
        )
        context.registration_repo.add_registration(registration)
    


@when(u'the user checks for a list of {status} registrants')
def step_impl(context, status: Literal['approved', 'rejected', 'waitlisted', 'all']):
    status = None if status == "all" else status
    context.app.list_registrants(workshop_id='12345', status=status)
    

@then(u'they see the following registrants summary')
def step_impl(context):
    registrants = context.list_registrants_presenter.show.call_args[1]['registrants']
    for observed, expected in zip(registrants, context.table):
        assert observed.name == expected['name'], f"{observed} {expected}"
        assert observed.email == expected['email'], f"{observed} {expected}"
        assert observed.group_name == expected['group'], f"{observed} {expected}"
        assert observed.registered_on == expected['date'], f"{observed} {expected}"



@given(u'the status of eve is {status}')
def step_impl(context, status):
    registration = RegistrationRecord(
        workshop_id='334456',
        name='eve',
        custom_questions=[{'value': 'AG Bashiri'}],
        email='e@e.com',
        status=status,
        registered_on='2023-04-22',
        id="12345",
    )
    context.registration_repo.add_registration(registration)

@when(u'the user {action} eve')
def step_impl(context, action):
    statuses = {
        'approves': 'approved',
        'rejects': 'rejected',
    }
    status = statuses[action]
    context.app.update_registration_status(
        workshop_id='334456', 
        registration_id='12345', 
        to_status=status,
    )


@then(u'the status of eve is {status}')
def step_impl(context, status):
    workshop_id = '334456'
    registration_id='12345'

    eve = context.registration_repo.get_registration(workshop_id=workshop_id, registration_id=registration_id)
     
    assert eve.status == status, f"obs: {eve.status}, exp: {status}"

    registrant = context.list_registrants_presenter.show_update.call_args[1]['registrant']
    assert registrant.status == status, f"obs: {registrant.status}, exp: {status}"
    assert registrant.name == 'eve'
    assert registrant.id == '12345'
    assert registrant.workshop_id == '334456'
    assert registrant.email == 'e@e.com'
    assert registrant.registered_on == '2023-04-22'
    assert registrant.group_name == 'AG Bashiri'


@then(u'an error is raised')
def step_impl(context):
    msg = context.registration_repo.show_error.call_args[1]['message']
    assert msg 


