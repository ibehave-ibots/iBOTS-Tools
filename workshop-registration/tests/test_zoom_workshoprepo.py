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
    expected_outcome = 'iBOTS Workshop: Intro to Data Analysis with Python and Pandas '
    assert zoom_meeting.topic == expected_outcome