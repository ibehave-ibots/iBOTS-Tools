import random
import pytest
from external.zoom_api.get_meeting import get_meeting, Meeting
from external.zoom_api.list_registrants import list_registrants, ZoomRegistrant
from pytest import mark
import requests

def test_registrants_added(access_token, setup_sandbox, meeting_id):
    response = setup_sandbox

    registrants = list_registrants(access_token=access_token, meeting_id=meeting_id, status="pending")
    assert len(registrants) > 0

@pytest.fixture
def meeting_id():
    meeting_id = "824 9123 9311"
    return meeting_id
  
@pytest.fixture
def setup_sandbox(access_token: str, meeting_id: str) -> None:
    fname = 'test'+str(random.randint(1, 10))
    params = {
    "first_name": fname,
    "last_name": 'last_name',
    "email": fname+'@lname.com',
    }
    response = requests.post(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ','')}/registrants",
        headers={"Authorization": f"Bearer {access_token}"},
        json=params,
        )
    response.raise_for_status()
    yield response
    registrant_id = response.json()['registrant_id']
    response = requests.delete(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}/registrants/{registrant_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        )
    response.raise_for_status()
