
from unittest.mock import Mock, patch

import pytest
from adapters.registrationrepo_inmemory import InMemoryRegistrationRepo
from app.registrationrepo import RegistrationRecord
from app.registrant_workflows import RegistrantWorkflows, ZoomRegistrantStatusError

def test_listing_registrants_provides_all_correct_fields():
    # GIVEN
    workshop_id = '1234'

    repo = InMemoryRegistrationRepo()
    repo.add_registration(
        RegistrationRecord(
            workshop_id=workshop_id,
            name='Nick',
            registered_on='2023-9-21',
            custom_questions=[{'value': 'AG Del Grosso' }],
            email='fake@email.com',
            status='rejected',
        )
        )
    
    mock_presenter = Mock()
    app = RegistrantWorkflows(registration_repo=repo, presenter =mock_presenter)


    # WHEN
    app.list_registrants(workshop_id=workshop_id)

    # THEN
    registrant = mock_presenter.show.call_args[1]['registrants'][0]
    assert registrant.name == 'Nick'
    assert registrant.email == 'fake@email.com'
    assert registrant.status == 'rejected'
    assert registrant.registered_on == '2023-9-21'
    assert registrant.group_name == 'AG Del Grosso'
    
    
@pytest.mark.parametrize(
    ("status", "to_status"), 
    [("approved", "rejected"), 
     ("approved", "waitlisted"),
     ("rejected", "approved"),
     ("rejected", "waitlisted")
     ])
def test_error_is_raised_when_user_wants_to_change_decided_status(status, to_status):
    # GIVEN there is a registration with status approved
    workshop_id = '1234'
    registration_id = "4321"
    
    repo = InMemoryRegistrationRepo()
    repo.add_registration(
        RegistrationRecord(
            workshop_id=workshop_id,
            name='Nick',
            registered_on='2023-9-21',
            custom_questions=[{'value': 'AG Del Grosso' }],
            email='fake@email.com',
            status=status,
            id=registration_id,
        )
        )
    
    mock_presenter = Mock()
    workflow = RegistrantWorkflows(registration_repo=repo, presenter =mock_presenter)
    
    # WHEN the used wants to reject the registration
    with patch('app.registrant_workflows.RegistrantWorkflows.show_error', new=Mock()) as mock_show_error:
        workflow.update_registrant_status(workshop_id=workshop_id, registration_id=registration_id, to_status=to_status)
    
    # THEN an error is raised
    args = mock_show_error.call_args[0]
    error_msg = args[0]
    assert isinstance(error_msg, str)
    assert "Decision cannot be reversed" in error_msg
    assert "Nick" in error_msg
    assert status in error_msg

    with pytest.raises(ZoomRegistrantStatusError) as excinfo:
        workflow.show_error(error_msg)
        assert error_msg == str(excinfo.value)
       