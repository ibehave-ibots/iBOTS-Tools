from dataclasses import dataclass
from unittest.mock import Mock
import pytest
from external.zoom_api import ZoomAPI
from app import WorkshopRepo, WorkshopRecord

@dataclass(frozen=True)
class ZoomWorkshopRepo(WorkshopRepo):
    zoom_api: ZoomAPI
    
    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        meeting_ids = self.zoom_api.get_meeting_ids()
        meetings = []
        for meeting_id in meeting_ids:
            meeting = self.zoom_api.get_meeting(meeting_id=meeting_id)
            meetings.append(meeting)
        return meetings
        
@pytest.mark.skip
def test_zoom_workshoprepo_returns_correct_ids():
    zoom_api = Mock(ZoomAPI)
    repo = ZoomWorkshopRepo(zoom_api=zoom_api)
    
    # Given that there is an upcoming zoom workshop with id as 12345
    
    # When the user asks for upcoming workshops
    workshops = repo.get_upcoming_workshops()
    
    # Then the user sees a list of workshops containing an entry of workshop with id '12345'
    assert len(workshops) == 1