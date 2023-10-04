from unittest.mock import Mock, patch
from pytest import mark
from typing import Literal

from app import RegistrantWorkflows, RegistrationRecord
from app.registrant_workflows import ZoomRegistrantStatusError
from app.app import App
from adapters import InMemoryRegistrationRepo


@mark.parametrize(
    ("status", "new_status"),
    [
    ("rejected", "approved"),
    ("rejected", "waitlisted"),
    ("approved", "rejected"),
    ("approved", "waitlisted"),
    ]
    )
def test_registration_decision_cannot_be_changed(status, new_status):

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
                status=status,
                )
            ],
    )

    workflow = RegistrantWorkflows(
                registration_repo=repo,
                presenter=Mock()
                )
    #WHEN
    # the registrant's status is changed 
    with patch.object(InMemoryRegistrationRepo, "update_registration"):
        try:
            workflow.update_registrant_status(
                                workshop_id="12345", 
                                registration_id="54321",
                                to_status=new_status)
        except:
            pass
        #THEN
        # the registrant's status is NOT updated
        workflow.registration_repo.update_registration.assert_not_called()