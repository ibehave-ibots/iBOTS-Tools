from dataclasses import dataclass
from textwrap import dedent
from unittest.mock import Mock

import yaml
from external.zoom_api import ZoomAPI, RecurringMeetingSummary, Meeting, Occurrence
from app import WorkshopRepo, WorkshopRecord

@dataclass(frozen=True)
class ZoomWorkshopRepo(WorkshopRepo):
    zoom_api: ZoomAPI
    user_id: str

    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        meeting_summaries = self.zoom_api.get_meetings(user_id=self.user_id)
        workshop_records = []
        for meeting_summary in meeting_summaries:
            meeting = self.zoom_api.get_meeting(meeting_id=str(meeting_summary.id))
            metadata = yaml.load(meeting.agenda.split("---")[1], Loader=yaml.Loader)
            workshop_record = WorkshopRecord(
                link=meeting.registration_url,
                title=meeting_summary.topic,
                date=meeting_summary.start_time[:10],
                capacity=metadata["Capacity"],
                id=str(meeting_summary.id),
            )
            workshop_records.append(workshop_record)
        return workshop_records
        
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