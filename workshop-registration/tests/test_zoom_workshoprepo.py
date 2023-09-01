from textwrap import dedent
from unittest.mock import Mock
from adapters import ZoomWorkshopRepo
from external.zoom_api import ZoomAPI, RecurringMeetingSummary, Meeting, Occurrence, ScheduledMeetingSummary
        
def test_zoom_workshoprepo_returns_correct_workshops():
    
    zoom_api = Mock(ZoomAPI)
    agenda = dedent("""
    Assessment & Credits:

    - No exams
    - 22 hours of coursework, equivalent to 0.75 ECTS credit

    
    ---
    Capacity: 105
    """)
    zoom_api.get_meetings.return_value = [RecurringMeetingSummary(
        id=12345,
        topic='topic',
        agenda=agenda,
        start_time='2023-11-06T08:00:00Z'
    )]
    zoom_api.get_meeting.return_value = Meeting(
        topic='topic',
        registration_url='link',
        occurrences=[Occurrence(start_time='2023-11-06T08:00:00Z')],
        agenda=agenda,
        id=12345,
    )
    
    user_id = 'test_user_id'
    repo = ZoomWorkshopRepo(zoom_api=zoom_api, user_id=user_id)
    workshops = repo.get_upcoming_workshops()
    
    zoom_api.get_meetings.assert_called_with(user_id=user_id)
    zoom_api.get_meeting.assert_called_with(meeting_id='12345')

    assert len(workshops) == 1
    assert workshops[0].id == "12345"
    assert workshops[0].title == "topic"
    assert workshops[0].date == "2023-11-06"
    assert workshops[0].link == 'link'
    assert workshops[0].capacity == 105

def test_only_zoom_workshops_are_returned():
    zoom_api = Mock(ZoomAPI)
    agenda = dedent("""
    Assessment & Credits:

    - No exams
    - 22 hours of coursework, equivalent to 0.75 ECTS credit

    
    ---
    Capacity: 105
    """)

    # Given that there are a mixture of zoom meetings
    zoom_api.get_meetings.return_value = [
        RecurringMeetingSummary(
            id=12345,
            topic='topic',
            agenda=agenda,
            start_time='2023-11-06T08:00:00Z'
        ),
        ScheduledMeetingSummary(
            id=23456,
            topic="topic",
            start_time='2023-10-06T08:00:00Z'
        )
    ]
    zoom_api.get_meeting.return_value = Meeting(
        topic='topic',
        registration_url='link',
        occurrences=[Occurrence(start_time='2023-11-06T08:00:00Z')],
        agenda=agenda,
        id=12345,
    )
    
    # When the user asks for zoom workshops
    user_id = 'test_user_id'
    repo = ZoomWorkshopRepo(zoom_api=zoom_api, user_id=user_id)
    workshops = repo.get_upcoming_workshops()
    
    # Then only workshops are seen
    assert len(workshops) == 1