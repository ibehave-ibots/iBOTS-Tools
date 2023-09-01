from __future__ import annotations
from typing import List
from .zoom_oauth import create_access_token
from .get_meeting import get_meeting, Meeting
from .get_meetings import get_meetings, MeetingSummary

class ZoomAPI:

    def _get_access_token(self) -> str:
        access_data = create_access_token()
        access_token = access_data['access_token']
        return access_token
    
    def get_meeting(self, meeting_id) -> Meeting:
        access_token = self._get_access_token()
        return get_meeting(access_token=access_token, meeting_id=meeting_id)
    
    def get_meetings(self, user_id: int) -> List[MeetingSummary]:
        access_token = self._get_access_token()
        return get_meetings(access_token=access_token, user_id=user_id)