import os
from unittest.mock import Mock, patch
from dotenv import load_dotenv
from pytest import fixture, mark
from external.zoom_api.zoom_oauth import OAuthGetToken
from external.zoom_api.get_meeting import get_meeting, Meeting
from external.zoom_api.get_meetings import get_meetings
from external.zoom_api.list_registrants import list_registrants
from external.zoom_api.list_group_members import list_group_members


@fixture(scope="session")
def access_token():
    load_dotenv()
    oauth = OAuthGetToken(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        account_id=os.environ["ACCOUNT_ID"],
    )
    access_data = oauth.create_access_token()
    return access_data["access_token"]

@fixture(scope='session')
def user_id():
    load_dotenv()
    user_id = os.environ['TEST_USER_ID']
    return user_id

def test_can_get_token(access_token):
    assert access_token


def test_get_zoom_workshop_from_id(access_token):
    # Given a meeting a id
    meeting_id = "860 6126 7458"

    # When we ask for zoom meeting
    zoom_meeting = get_meeting(access_token=access_token, meeting_id=meeting_id)

    # Then we see topic
    assert (
        zoom_meeting.topic
        == "iBOTS Workshop: Intro to Data Analysis with Python and Pandas "
    )
    assert (
        zoom_meeting.registration_url
        == "https://us02web.zoom.us/meeting/register/tZItceiqqDwuH9yaRnk81FeBi3qwQP-3rgTI"
    )
    for occurrence in zoom_meeting.occurrences:
        assert occurrence.start_time
    assert zoom_meeting.agenda
    assert zoom_meeting.id


def test_get_zoom_session_from_id(access_token):
    # Given a meeting id
    meeting_id = "899 0138 0945"

    # When we ask for zoom meeting
    zoom_meeting = get_meeting(access_token=access_token, meeting_id=meeting_id)

    # Then we see topic
    assert zoom_meeting.topic == "Feedback on workshop material (Jens and Mo)"
    assert zoom_meeting.agenda == ""
    assert zoom_meeting.id


def test_get_upcoming_zoom_meetings_from_user_id(access_token):
    # GIVEN there are upcoming zoom meetings for a user with a speific id
    user_id = os.environ["TEST_USER_ID"]

    # WHEN user asks for the upcoming zoom meetings
    zoom_meetings = get_meetings(access_token=access_token, user_id=user_id)

    # THEN a list of upcoming zoom meeetings is returned
    agenda_counter = 0
    for meeting in zoom_meetings:
        assert meeting.id
        assert meeting.topic
        assert meeting.start_time
        if hasattr(meeting, "agenda"):
            agenda_counter += 1
    assert agenda_counter >= 1


@mark.parametrize("status,num", [("approved", 2), ("pending", 0), ("denied", 1)])
def test_get_registrants_gets_right_number_of_registrants_from_meeting_id(
    access_token, status, num
):
    # Given a meeting id
    meeting_id = "838 4730 7377"
    

    # When we ask for zoom meeting
    registrants = list_registrants(
        access_token=access_token, meeting_id=meeting_id, status=status
    )

    # THEN
    assert len(registrants) == num
    for registrant in registrants:
        assert hasattr(registrant, "first_name")
        assert hasattr(registrant, "last_name")
        assert hasattr(registrant, "email")
        assert hasattr(registrant, "status")
        assert hasattr(registrant, "registered_on")
        assert hasattr(registrant, "custom_questions")


def test_workshop_without_registration_link_is_returned_as_a_meeting():

    # GIVEN
    zoom_data = {
        "topic": Mock(),
        "occurrences": [{"start_time": Mock()}, {"start_time": Mock()}],
        "agenda": Mock(),
        "id": Mock(),
        "type": 8,
    }
     
    # WHEN
    with patch("requests.get") as mock_request_get:
        mock_response = Mock()
        mock_request_get.return_value = mock_response
        mock_response.json.return_value = zoom_data
        meeting = get_meeting(access_token=Mock(), meeting_id=Mock())
    
    # THEN
    assert isinstance(meeting, Meeting)


def test_empty_agenda_is_returned_when_agenda_is_missing(access_token):
    # GIVEN
    zoom_data = {'meetings':
            [  
                {
                'created_at': Mock(),
                'duration': Mock(),
                'host_id': Mock(),
                'id': Mock(),
                'join_url': Mock(),
                'start_time': Mock(),
                'timezone': Mock(),
                'topic': Mock(),
                'type': 8,
                'uuid': Mock()
                 }
            ]
        }
    # WHEN
    with patch("requests.get") as mock_request_get:
        mock_response = Mock()
        mock_request_get.return_value = mock_response
        mock_response.json.return_value = zoom_data
        meetings = get_meetings(access_token=Mock(), user_id=Mock())

    #THEN
    assert len(meetings) ==1
    assert meetings[0].agenda ==''



def test_get_user_ids_from_group_id(access_token):
    #given 
    group_id = "b_r8HCDBSSqe8gHUVfIyaQ"
    user_1 = "NblGhypARWa7TjfyN2zqaQ"
    user_2 = "vrxh8FQGQk2IFYTsm8a7qg"

    #when
    user_ids = list_group_members(access_token=access_token, group_id=group_id)

    #then
    assert any(user.id == user_1 for user in user_ids)
    assert any(user.id == user_2 for user in user_ids)
