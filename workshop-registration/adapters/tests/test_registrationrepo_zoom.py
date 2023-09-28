import os
from unittest.mock import Mock, patch

from dotenv import load_dotenv
from pytest import mark
from app import RegistrationRepo, RegistrationRecord
from adapters.registrationrepo_zoom import ZoomRegistrationRepo
from external.zoom_api.list_registrants import ZoomRegistrant, list_registrants
from external.zoom_api import OAuthGetToken, update_registration

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



def test_zoom_registration_repo_changes_registrant_status():
    # GIVEN
    mock_oauth_get_token = Mock()
    mock_oauth_get_token.create_access_token.return_value = {"access_token": "fakeToken"}
    repo = ZoomRegistrationRepo(list_registrants = Mock(), 
                                update_registration = Mock(update_registration),
                                oauth_get_token = mock_oauth_get_token)
    new_status='approved'
    waitlisted_registrant = RegistrationRecord( 
                            workshop_id = "12345",
                            name = "Balexander Callman",
                            registered_on = "2023-09-01", 
                            custom_questions = [{"favourite colour": "borange"}], 
                            email = "a@c.com", 
                            status = "waitlisted",
                            id  = "999999"
                            )
    # WHEN status is changed to approved
    with patch("requests.put") as mock_request_put:
        mock_request_put.return_value = Mock()
        repo.change_registration_status(registration=waitlisted_registrant, new_status=new_status)

    # THEN check that repo.update_registration is called with correct args
    zoom_registrant = ZoomRegistrant(first_name = "Balexander" ,
                                    last_name = "Callman" ,
                                    email = "a@c.com",
                                    status = "pending",
                                    registered_on = "2023-09-01",
                                    custom_questions = [{"favourite colour": "borange"}],
                                    id = "999999"
                                    )

    repo.update_registration.assert_called_once_with(access_token= "fakeToken", 
                                                    meeting_id="12345",
                                                    registrant = zoom_registrant,
                                                    new_status= "approved")
    

# def test_zoom_registration_repo_update_registration_method_call():
    # GIVEN: we have an in-memory adapter for change status
    # AND a zoom adapter for change status
    # WHEN: we need to update a specific registration for each repo
    # THEN: both in-memory and zoom update_registration methods are called with the similarly typed arguments