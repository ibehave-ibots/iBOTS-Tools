import random
from typing import Generator, Literal, cast
import pytest
from external.zoom_api.get_meeting import get_meeting, Meeting
from external.zoom_api.list_registrants import list_registrants, ZoomRegistrant
from external.zoom_api.update_registration import zoom_call_update_registration
from external.zoom_api.create_or_delete_registrant import create_random_zoom_registrant, delete_zoom_registrant
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

    registrant = registrants[0]
    updated_registrant = ZoomRegistrant(
            first_name = registrant.first_name,
            last_name = registrant.last_name,
            email = registrant.email,
            status = new_status,
            registered_on = registrant.registered_on,
            custom_questions = registrant.custom_questions,
            id = registrant.id
            )
    zoom_call_update_registration(access_token=access_token, meeting_id=meeting_id, registrant=updated_registrant)
    registrants_status_change = list_registrants(access_token=access_token, meeting_id=meeting_id, status=new_status)
    assert registrants_status_change[0].status == new_status

@pytest.fixture
def meeting_id() -> Literal['824 9123 9311']:
    meeting_id: Literal['824 9123 9311'] = '824 9123 9311'
    return meeting_id

@pytest.fixture
def setup_sandbox(access_token: str, meeting_id: str) -> Generator:
    registrant_id = create_random_zoom_registrant(access_token=access_token, meeting_id=meeting_id, status="pending")
    yield
    delete_zoom_registrant(access_token=access_token, meeting_id=meeting_id, registrant_id=registrant_id)