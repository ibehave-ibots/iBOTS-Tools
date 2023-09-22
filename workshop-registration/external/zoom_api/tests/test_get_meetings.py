from unittest.mock import Mock, patch
from external.zoom_api.get_meetings import get_meetings
from pytest import mark


@mark.slow
def test_get_upcoming_zoom_meetings_from_user_id(access_token, user_id):
    # GIVEN there are upcoming zoom meetings for a user with a speific id

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
