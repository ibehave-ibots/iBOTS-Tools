from textwrap import dedent
from unittest.mock import Mock

from pytest import mark
from adapters import ZoomWorkshopRepo
from external.zoom_api import RecurringMeetingSummary, Meeting, Occurrence, ScheduledMeetingSummary, OAuthGetToken


def test_zoom_workshoprepo_returns_correct_workshops():
    agenda = dedent("""
    Assessment & Credits:

    - No exams
    - 22 hours of coursework, equivalent to 0.75 ECTS credit

    
    ---
    Capacity: 105
    """)
    get_meetings = Mock()
    get_meetings.return_value = [RecurringMeetingSummary(
        id=12345,
        topic='topic',
        agenda=agenda,
        start_time='2023-11-06T08:00:00Z'
    )]

    get_meeting = Mock()
    get_meeting.return_value = Meeting(
        topic='topic',
        registration_url='link',
        occurrences=[Occurrence(start_time='2023-11-06T08:00:00Z')],
        agenda=agenda,
        id=12345,
    )
    
    user_id = 'test_user_id'
    oauth = Mock(OAuthGetToken)
    oauth.create_access_token.return_value = {'access_token': "OPEN-SESAME"}
    repo = ZoomWorkshopRepo(user_id=user_id, get_meeting=get_meeting, get_meetings=get_meetings, oauth_get_token=oauth)
    workshops = repo.get_upcoming_workshops()


    assert len(workshops) == 1
    assert workshops[0].id == "12345"
    assert workshops[0].title == "topic"
    assert workshops[0].date == "2023-11-06"
    assert workshops[0].link == 'link'
    assert workshops[0].capacity == 105

def test_only_zoom_workshops_are_returned():
    agenda = dedent("""
    Assessment & Credits:

    - No exams
    - 22 hours of coursework, equivalent to 0.75 ECTS credit

    
    ---
    Capacity: 105
    """)

    # Given that there are a mixture of zoom meetings
    get_meeting = Mock()
    get_meeting.return_value = Meeting(
        topic='topic',
        registration_url='link',
        occurrences=[Occurrence(start_time='2023-11-06T08:00:00Z')],
        agenda=agenda,
        id=12345,
    )
    
    get_meetings = Mock()
    get_meetings.return_value = [
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

    # When the user asks for zoom workshops
    user_id = 'test_user_id'

    oauth = Mock(OAuthGetToken)
    oauth.create_access_token.return_value = {'access_token': "OPEN-SESAME"}
    repo = ZoomWorkshopRepo(user_id=user_id, get_meeting=get_meeting, get_meetings=get_meetings, oauth_get_token=oauth)
    workshops = repo.get_upcoming_workshops()
    
    # Then only workshops are seen
    assert len(workshops) == 1