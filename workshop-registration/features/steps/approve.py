from behave import given, when, then
from typing import Literal

from mock import Mock

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

