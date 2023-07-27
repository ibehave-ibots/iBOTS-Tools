from __future__ import annotations
from datetime import datetime, timedelta
from typing import Set
from unittest.mock import Mock

from .workflows import WorkshopRepo, SessionRecord, WorkshopRecord
from .zoom_api import ZoomRestApi


def test_repo_can_get_workshop_from_zoom_api():
    api = Mock(ZoomRestApi)
    api.get_meeting.return_value = {
        'id': 123,  # an int
        'topic': 'intro to python',
        'start_time':  '2021-12-25T9:30:00Z', # '%Y-%m-%dT%H:%M:%SZ'
        'duration': 60, # minutes
        'agenda': 'a neat workshop, join us!',
    }
    repo = ZoomWorkshopRepo(zoom_api=api)
    
    observed_workshop = repo.get_workshop(workshop_id='123')
    expected_workshop = WorkshopRecord(
        id='123',
        name='intro to python',
        description='a neat workshop, join us!',
        scheduled_start=datetime(2021, 12, 25, 9, 30, 0),
        scheduled_end=datetime(2021, 12, 25, 10, 30, 0),
        session_ids=[],
    )
    assert observed_workshop == expected_workshop


def test_repo_can_get_session_from_zoom_api():
    api = Mock(ZoomRestApi)
    api.get_meeting.return_value = {
        'id': 'XADSJFDSF-ADFAF',  # a string
        'start_time':  '2021-12-27T9:30:00Z', # '%Y-%m-%dT%H:%M:%SZ'
        'duration': 90, # minutes
    }
    repo = ZoomWorkshopRepo(zoom_api=api)
    observed_session = repo.get_session(session_id='XADSJFDSF-ADFAF')
    expected_session = SessionRecord(
        id='XADSJFDSF-ADFAF',
        scheduled_start=datetime(2021, 12, 27, 9, 30, 00),
        scheduled_end=datetime(2021, 12, 27, 11, 00, 00)
    )
    assert observed_session == expected_session


def test_repo_can_get_list_of_workshops_from_zoom_api():
    api = Mock(ZoomRestApi)
    api.list_users_in_group.return_value = ['emma', 'addy']
    api.list_scheduled_meetings_of_user.side_effect = [
        {'meetings': ['aa', 'bb', 'cc']},
        {'meetings': ['ee', 'ff', 'gg']},
    ]
    
    repo = ZoomWorkshopRepo(zoom_api=api)
    
    observed_workshop_ids = repo.list_workshops()
    expected_workshop_ids = {'aa', 'bb', 'cc', 'ee', 'ff', 'gg'}
    assert observed_workshop_ids == expected_workshop_ids
    


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
        
