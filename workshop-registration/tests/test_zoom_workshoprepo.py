
from typing import NamedTuple
import pytest
import requests
import os
from external.zoom_api.zoom_oauth import create_access_token

class Meeting(NamedTuple):
    topic: str

class ZoomAPI:

    def _get_access_token(self) -> str:
        access_data = create_access_token()
        access_token = access_data['access_token']
        return access_token
    

    def get_meeting(self, meeting_id) -> Meeting:
        access_token = self._get_access_token()
        
        response = requests.get(
            url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data = response.json()
        
        return Meeting(topic=data['topic'])
    
    

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