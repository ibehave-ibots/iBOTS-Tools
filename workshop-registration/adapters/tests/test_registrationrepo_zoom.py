import os
from unittest.mock import Mock

from dotenv import load_dotenv
from pytest import mark
from adapters.registrationrepo_zoom import ZoomRegistrationRepo
from external.zoom_api.list_registrants import ZoomRegistrant, list_registrants
from external.zoom_api import OAuthGetToken

def test_zoom_registration_repo_returns_correct_registrations_for_a_given_workshop():
    # GIVEN
    list_registrants = lambda access_token, meeting_id, status: {
        "approved": [
            ZoomRegistrant(
                first_name="first_A",
                last_name="last_A",
                email="a@a.com",
                status="approved",
                registered_on="2023-07-19T11:27:47Z",
                custom_questions=[{"title": "Affiliation", "value": "OthersA"}],
                id="random_a"
            ),
        ],
        "pending": [
            ZoomRegistrant(
                first_name="first_C",
                last_name="last_B",
                email="c@c.com",
                status="pending",
                registered_on="2023-07-19T11:27:47Z",
                custom_questions=[{"title": "Affiliation", "value": "OthersB"}],
                id="random_b"
            )
        ],
        "denied": [
            ZoomRegistrant(
                first_name="first_B",
                last_name="last_B",
                email="b@b.com",
                status="denied",
                registered_on="2023-07-19T11:27:47Z",
                custom_questions=[{"title": "Affiliation", "value": "OthersC"}],
                id="random_c"
            )
        ],
    }[status]

    oauth = Mock(OAuthGetToken)
    oauth.create_access_token.return_value = {'access_token': "OPEN-SESAME"}
    repo = ZoomRegistrationRepo(list_registrants=list_registrants, oauth_get_token=oauth)

    # WHEN
    registration_records = repo.get_registrations(workshop_id=Mock())

    # THEN
    assert len(registration_records) == 3
    assert registration_records[0].name == "first_A last_A"
    assert registration_records[0].status == "approved"
    assert hasattr(registration_records[0], "workshop_id")
    assert hasattr(registration_records[0], "id")

    assert registration_records[1].status == "waitlisted"
    assert registration_records[2].status == "rejected"

    assert hasattr(registration_records[0], "registered_on")
    assert hasattr(registration_records[0], "custom_questions")
    
    assert hasattr(registration_records[0], "email")


@mark.slow
def test_zoom_registration_repo_returns_correct_registrations_for_a_given_zoom_workshop():
    load_dotenv()
    oauth = OAuthGetToken(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        account_id=os.environ["ACCOUNT_ID"],
    )

    repo = ZoomRegistrationRepo(list_registrants=list_registrants, oauth_get_token=oauth)
    workshop_id = "838 4730 7377"

    registration_records = repo.get_registrations(workshop_id=workshop_id)
    assert len(registration_records) == 3
    assert registration_records[0].workshop_id == workshop_id



#TODO change ZoomRegistrant to RegistrationRecord, maybe? Think about it!!
def test_zoom_registration_repo_approves_registrant():
    # GIVEN
    list_registrants = lambda access_token, meeting_id, status: {
        "approved": [
            ZoomRegistrant(
                first_name="first_A",
                last_name="last_A",
                email="a@a.com",
                status="approved",
                registered_on="2023-07-19T11:27:47Z",
                custom_questions=[{"title": "Affiliation", "value": "OthersA"}],
                id="random_a"
            ),
        ],
        "pending": [
            ZoomRegistrant(
                first_name="first_C",
                last_name="last_B",
                email="c@c.com",
                status="pending",
                registered_on="2023-07-19T11:27:47Z",
                custom_questions=[{"title": "Affiliation", "value": "OthersB"}],
                id="random_b"
            )
        ],
        "denied": [
            ZoomRegistrant(
                first_name="first_B",
                last_name="last_B",
                email="b@b.com",
                status="denied",
                registered_on="2023-07-19T11:27:47Z",
                custom_questions=[{"title": "Affiliation", "value": "OthersC"}],
                id="random_c"
            )
        ],
    }[status]

    registrant_to_approve = ZoomRegistrant(
                first_name="first_C",
                last_name="last_B",
                email="c@c.com",
                status="waitlisted",
                registered_on="2023-07-19T11:27:47Z",
                custom_questions=[{"title": "Affiliation", "value": "OthersB"}],
                id="random_b"
            )

    oauth = Mock(OAuthGetToken)
    oauth.create_access_token.return_value = {'access_token': "OPEN-SESAME"}
    repo = ZoomRegistrationRepo(list_registrants=list_registrants, 
                                oauth_get_token=oauth)
    registration_records = repo.get_registrations(workshop_id=Mock())

    # WHEN
    repo.update_registration(registration=registrant_to_approve, new_status='approved')

    # THEN
    updated_registrants = repo.get_registrations(workshop_id=Mock())
    assert len(updated_registrants) == 3
    assert updated_registrants[1].email == "c@c.com"
    assert updated_registrants[1].status == "approved"