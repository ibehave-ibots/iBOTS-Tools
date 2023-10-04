from unittest.mock import Mock, patch
from pytest import mark
from typing import Literal

from app import RegistrantWorkflows, RegistrationRecord
from app.registrant_workflows import ZoomRegistrantStatusError
from app.app import App
from adapters import InMemoryRegistrationRepo


@mark.parametrize("new_status",[("rejected","waitlisted","approved")])
def test_registration_decision_cannot_be_changed(new_status: Literal['approved','rejected', 'waitlisted']):

    #GIVEN
    #a registrant has a status that is NOT waitlisted
    repo = InMemoryRegistrationRepo(
        registrations=[
            RegistrationRecord(
                id="54321",
                workshop_id="12345",
                name="eve",
                email="e@e.com",
                registered_on="25092023",
                custom_questions=[{'value': 'Prof. Sangee'}],
                status='approved',
                )
            ],
    )

    app= App(
            workshop_workflow=Mock(),
            registrant_workflows=RegistrantWorkflows(
                registration_repo=repo,
                presenter=Mock(),
            )
    )
    #WHEN
    # the registrant's status is changed 
    with patch.object(InMemoryRegistrationRepo, "update_registration" ):
        try:
            app.update_registration_status(
                                workshop_id= "12345", 
                                registration_id= "54321",
                                to_status= 'waitlisted')
        except ZoomRegistrantStatusError as e:
            pass
        #THEN
        # the registrant's status is NOT updated
        app.registrant_workflows.registration_repo.update_registration.assert_not_called()