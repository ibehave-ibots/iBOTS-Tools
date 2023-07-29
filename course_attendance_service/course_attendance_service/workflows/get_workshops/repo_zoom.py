from __future__ import annotations
from datetime import datetime, timedelta
from typing import Set
from unittest.mock import Mock

from .workflows import WorkshopRepo, SessionRecord, WorkshopRecord
from .zoom_api import ZoomRestApi


class ZoomWorkshopRepo(WorkshopRepo):
    
    def __init__(self, zoom_api: ZoomRestApi) -> None:
            self.zoom_api = zoom_api
            self.access_token = 'TOP-SECRET'
            self.group_id = 'TOP-SECRET'
            
    def list_workshops(self) -> Set[str]:
        
        all_meeting_ids: Set[str] = set()
        user_ids = self.zoom_api.list_users_in_group(group_id=self.group_id)
        for user_id in user_ids:
            data = self.zoom_api.list_scheduled_meetings_of_user(access_token=self.access_token, user_id=user_id)
            meeting_ids = set(data['meetings'])
            all_meeting_ids.update(meeting_ids)
        return all_meeting_ids
    
    def get_workshop(self, workshop_id: str) -> WorkshopRecord:
        data = self.zoom_api.get_meeting(access_token=self.access_token, meeting_id=workshop_id)
        return WorkshopRecord(
            id=str(data['id']),
            name=data['topic'],
            description=data['agenda'],
            scheduled_start=(planned_start := datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%SZ')),
            scheduled_end=planned_start + timedelta(minutes=data['duration']),
            session_ids=[],
        )
    
    def get_session(self, session_id: str) -> SessionRecord:
        data = self.zoom_api.get_meeting(
            url = f"https://api.zoom.us/v2/meetings/{session_id}", 
            headers = {'Authorization': f"Bearer {self.access_token}"}
        )
        return SessionRecord(
            id=data['id'],
            scheduled_start=(start := datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%SZ')),
            scheduled_end=start + timedelta(minutes=data['duration']),
        )
        
