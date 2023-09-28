import random
from typing import Generator, Literal, cast
import pytest
from external.zoom_api.get_meeting import get_meeting, Meeting
from external.zoom_api.list_registrants import list_registrants, ZoomRegistrant
from external.zoom_api.update_registration import update_registration
from pytest import mark
import requests

@mark.slow
def test_registrants_added(access_token, setup_sandbox, meeting_id):
    registrants = list_registrants(access_token=access_token, meeting_id=meeting_id, status="pending")
    assert len(registrants) > 0

@mark.slow
@mark.parametrize("new_status", ("approved", "denied"))
def test_change_zoom_registrant_status(access_token, setup_sandbox, meeting_id, new_status):
    registrants = list_registrants(access_token=access_token, meeting_id=meeting_id, status="pending")
    assert registrants[0].status == 'pending'

    update_registration(access_token=access_token, meeting_id=meeting_id, registrant=registrants[0], new_status=new_status)
    registrants_status_change = list_registrants(access_token=access_token, meeting_id=meeting_id, status=new_status)
    assert registrants_status_change[0].status == new_status

@pytest.fixture
def meeting_id() -> Literal['824 9123 9311']:
    meeting_id: Literal['824 9123 9311'] = '824 9123 9311'
    return meeting_id

@pytest.fixture
def setup_sandbox(access_token: str, meeting_id: str) -> Generator:
    fname = 'test'+str(random.randint(1, 10))
    params = {
    "first_name": fname,
    "last_name": 'last_name',
    "email": fname+str(random.randint(1, 100))+'@lname.com',
    }
    response = requests.post(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ','')}/registrants",
        headers={"Authorization": f"Bearer {access_token}"},
        json=params,
        )
    response.raise_for_status()
    yield
    registrant_id = response.json()['registrant_id']
    response = requests.delete(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}/registrants/{registrant_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        )
    response.raise_for_status()
