from dataclasses import dataclass
from unittest.mock import Mock
import pytest
from external.zoom_api import ZoomAPI, RecurringMeetingSummary
from app import WorkshopRepo, WorkshopRecord

@dataclass(frozen=True)
class ZoomWorkshopRepo(WorkshopRepo):
    zoom_api: ZoomAPI
    user_id: str

    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        meetings = self.zoom_api.get_meetings(user_id=self.user_id)
        workshop_records = []
        for meeting in meetings:
            workshop_record = WorkshopRecord(
                link=None,
                title=meeting.topic,
                date=meeting.start_time[:10],
                capacity=None,
                id=str(meeting.id),
            )
            workshop_records.append(workshop_record)
        return workshop_records
        
def test_zoom_workshoprepo_returns_correct_workshops():
    
    zoom_api = Mock(ZoomAPI)
    zoom_api.get_meetings.return_value = [RecurringMeetingSummary(
        id=12345,
        topic='topic',
        agenda='agenda',
        start_time='2023-11-06T08:00:00Z'
    )]
    
    user_id = 'test_user_id'
    repo = ZoomWorkshopRepo(zoom_api=zoom_api, user_id=user_id)
    workshops = repo.get_upcoming_workshops()
    
    zoom_api.get_meetings.assert_called_with(user_id=user_id)
    assert len(workshops) == 1
    assert workshops[0].id == "12345"
    assert workshops[0].title == "topic"
    assert workshops[0].date == "2023-11-06"

