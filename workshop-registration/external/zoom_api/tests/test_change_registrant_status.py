from unittest.mock import Mock
from external.zoom_api import create_meeting
from external.zoom_api.get_meeting import Meeting
from external.zoom_api.get_meetings import get_meetings
from external.zoom_api.list_registrants import list_registrants
from external.zoom_api.list_registrants import ZoomRegistrant
from pytest import mark


def test_sandbox_meeting_gets_created(access_token, user_id):
    #GIVEN
    meetings = get_meetings(access_token=access_token, user_id=user_id)
    assert all(meeting.topic!='SANDBOX_MEETING' for meeting in meetings)

    meeting = Meeting(
        topic="SANDBOX_MEETING",
        registration_url=Mock(),
        occurrences=Mock(),
        agenda=Mock(),
        id=Mock()
    )
    #WHEN 
    create_meeting(access_token=access_token, user_id=user_id, meeting=meeting)
    #THEN
    meetings = get_meetings(access_token=access_token, user_id=user_id)
    assert [meeting.topic for meeting in meetings].count('SANDBOX_MEETING') ==1

def test_sandbox_meeting_has_registrants_added(access_token, user_id):
    #GIVEN 
    meetings = get_meetings(access_token=access_token, user_id=user_id)
    assert any(meeting.topic=='SANDBOX_MEETING' for meeting in meetings)   
    for meeting in meetings:
        if meeting.topic =='SANDBOX_MEETING':
            meeting_id = meeting.id
            break

    registrants = [
        ZoomRegistrant(
            first_name="Test",
            last_name="name 1",
            status="pending",
            registered_on="2023-09-21",
            custom_questions=[
                {"research group":"ibehave"}
            ]
        ),
        ZoomRegistrant(
            first_name="Test",
            last_name="name 2",
            status="pending",
            registered_on="2023-09-19",
            custom_questions=[
                {"research group":"ibehave"}
            ]
        )        


    ]
    #WHEN
    add_registrants(access_token=access_token, user_id=user_id, meeting_id=meeting_id, registrants=registrants)

    #THEN
    all_registrants = list_registrants(access_token=access_token,
                                       meeting_id=meeting_id)
    assert len(all_registrants) == 2
    assert all(registrant.status == "pending" for registrant in all_registrants)
    

   
@mark.skip
def test_zoom_registrant_status_change():
    #GIVEN
    workshop_id = Mock()
    registrant_id = Mock()
    new_status = Mock()

    assert workshop_id == "860 5777 0725"
    #WHEN

    #THEN