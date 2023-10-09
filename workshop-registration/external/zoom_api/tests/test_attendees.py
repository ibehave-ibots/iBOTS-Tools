import pytest
from external.zoom_api.get_attendees import get_attendees, get_session_uuids, ZoomAttendee

@pytest.fixture
def meeting_id():
    return "81504158493"

@pytest.mark.slow
def test_correct_session_uuids_returned_from_meeting_id(access_token, meeting_id):
    session_uuids = get_session_uuids(access_token=access_token, meeting_id=meeting_id)
    assert len(session_uuids) == 2
    assert session_uuids[0] == "6OXVEeGCSIK8d0AA/zIxfA=="
    assert session_uuids[1] == "4e+m9S6iT6u6MMxpdYgWMQ=="
    
@pytest.mark.slow
def test_correct_attendees_are_returned(access_token, meeting_id):
    attendees = get_attendees(access_token=access_token, meeting_id=meeting_id)
    assert len(attendees) == 6
    assert isinstance(attendees[0], ZoomAttendee)
    assert attendees[0].join_time == '2023-10-06T11:02:34Z'