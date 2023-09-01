import os
from external.zoom_api import ZoomAPI

def test_can_get_token():
    # Given secret information set as environment variables (account id, client id, client secret)
    account_id = os.environ.get('ACCOUNT_ID')
    assert account_id
    client_id = os.environ.get('CLIENT_ID')
    assert client_id
    client_secret = os.environ.get('CLIENT_SECRET')
    assert client_secret

    # When the user asks for access token
    zoom_api = ZoomAPI()
    access_token = zoom_api._get_access_token()

    # Then access token is returned
    assert access_token


def test_get_zoom_meeting_from_id():
    # Given a meeting id
    meeting_id = '860 6126 7458'

    # When we ask for zoom meeting
    zoom_api = ZoomAPI()
    zoom_meeting = zoom_api.get_meeting(meeting_id=meeting_id)

    # Then we see topic
    assert zoom_meeting.topic == 'iBOTS Workshop: Intro to Data Analysis with Python and Pandas '
    assert zoom_meeting.registration_url == 'https://us02web.zoom.us/meeting/register/tZItceiqqDwuH9yaRnk81FeBi3qwQP-3rgTI'
    for occurrence in zoom_meeting.occurrences:
        assert occurrence.start_time
    assert zoom_meeting.agenda
    assert zoom_meeting.id
    
def test_get_upcoming_zoom_meetings_from_user_id():
    # GIVEN there are upcoming zoom meetings for a user with a speific id
    user_id = os.environ["TEST_USER_ID"]
    
    # WHEN user asks for the upcoming zoom meetings
    zoom_api = ZoomAPI()
    zoom_meetings = zoom_api.get_meetings(user_id=user_id)
    
    # THEN a list of upcoming zoom meeetings is returned
    agenda_counter = 0
    for meeting in zoom_meetings:
        assert meeting.id
        assert meeting.topic
        assert meeting.start_time
        if hasattr(meeting, "agenda"):
            agenda_counter += 1
    assert agenda_counter>1