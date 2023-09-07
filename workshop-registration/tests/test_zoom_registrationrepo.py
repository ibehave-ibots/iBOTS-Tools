from unittest.mock import Mock

from adapters.registrationrepo_zoom import ZoomRegistrationRepo
from external.zoom_api.list_registrants import ZoomRegistrant, list_registrants


def test_zoom_registration_repo_returns_correct_registrations_for_a_given_workshop():
    # GIVEN 
    list_registrants = lambda access_token, meeting_id, status : {
        "approved":
            [
                ZoomRegistrant(
                    first_name='first_A',
                    last_name='last_A',
                    email='a@a.com',
                    status='approved'
                ),
            ],
        "pending": [],
        "denied":
            [
                ZoomRegistrant(
                    first_name='first_B',
                    last_name='last_B',
                    email='b@b.com',
                    status='denied'
                )
            ],
    }[status]
    repo = ZoomRegistrationRepo(list_registrants=list_registrants)
    
    # WHEN 
    registration_records = repo.get_registrations(workshop_id=Mock())

    # THEN
    assert len(registration_records) == 2
    assert registration_records[0].name == 'first_A last_A'
    assert registration_records[0].status == 'approved'
    assert hasattr(registration_records[0], "workshop_id")
    assert hasattr(registration_records[0], "id")


def test_zoom_registration_repo_returns_correct_registrations_for_a_given_zoom_workshop():
    repo = ZoomRegistrationRepo(list_registrants=list_registrants)
    registration_records = repo.get_registrations(workshop_id='838 4730 7377')
    assert len(registration_records) == 3