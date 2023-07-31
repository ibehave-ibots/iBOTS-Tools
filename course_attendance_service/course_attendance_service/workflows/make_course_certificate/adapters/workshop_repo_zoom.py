from __future__ import annotations
from datetime import datetime, timedelta
from typing import List, Set
from unittest.mock import Mock

from ..core.workflows import WorkshopRepo, SessionRecord, WorkshopRecord
from ..external.zoom_api import ZoomRestApi


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
        agenda = data['agenda']
        description = get_text_between(agenda, '## Workshop Description\n', '\n\n\n')
        organizer = get_text_between(agenda, '## Organizer\n', '\n\n\n')
        topics = self._strip_topics_from_agenda_text(agenda=agenda)
        return WorkshopRecord(
            id=str(data['id']),
            name=data['topic'],
            description=description,
            topics=topics,
            scheduled_start=(planned_start := datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%SZ')),
            scheduled_end=planned_start + timedelta(minutes=data['duration']),
            session_ids=[],
            organizer=organizer,
        )
    
    def _strip_topics_from_agenda_text(self, agenda: str) -> List[str]:
        text = get_text_between(agenda, '## Workshop Topics:\n', '\n\n\n')
        topics = [line.strip()[2:] for line in text.splitlines(keepends=False)]
        return topics
    
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
        




def get_text_between(text: str, header: str, footer: str) -> str:
        start = text.index(header) + len(header)
        end = text.index('\n\n\n', start)
        subtext = text[start:end]
        return subtext