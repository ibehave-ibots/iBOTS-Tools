from unittest.mock import Mock, patch
from external.zoom_api.get_meeting import get_meeting, Meeting
from pytest import mark


@mark.slow
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


@mark.slow
def test_get_zoom_session_from_id(access_token):
    # Given a meeting id
    meeting_id = "838 4730 7377"

    # When we ask for zoom meeting
    zoom_meeting = get_meeting(access_token=access_token, meeting_id=meeting_id)

    # Then we see topic
    assert zoom_meeting.topic == "Test workshop"
    assert zoom_meeting.agenda
    assert zoom_meeting.id


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

