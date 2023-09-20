
from unittest.mock import Mock
from adapters.registrationrepo_inmemory import InMemoryRegistrationRepo
from app.registrationrepo import RegistrationRecord
from app.registrant_workflows import RegistrantWorkflows

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
    