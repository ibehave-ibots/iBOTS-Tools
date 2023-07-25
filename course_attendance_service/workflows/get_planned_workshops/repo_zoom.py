from __future__ import annotations
from abc import ABC
from datetime import datetime, timedelta
from typing import List, Protocol, Set, TypedDict, Union
from unittest.mock import Mock, patch

import requests

from .workflows import WorkshopRepo, PlannedSessionDTO, PlannedWorkshopDTO


def test_can_get_workshop():
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
    expected_workshop = PlannedWorkshopDTO(
        id='123',
        name='intro to python',
        description='a neat workshop, join us!',
        planned_start=datetime(2021, 12, 25, 9, 30, 0),
        planned_end=datetime(2021, 12, 25, 10, 30, 0),
        session_ids=[],
    )
    assert observed_workshop == expected_workshop


def test_can_get_session():
    api = Mock(ZoomRestApi)
    api.get_meeting.return_value = {
        'id': 'XADSJFDSF-ADFAF',  # a string
        'start_time':  '2021-12-27T9:30:00Z', # '%Y-%m-%dT%H:%M:%SZ'
        'duration': 90, # minutes
    }
    repo = ZoomWorkshopRepo(zoom_api=api)
    observed_session = repo.get_session(session_id='XADSJFDSF-ADFAF')
    expected_session = PlannedSessionDTO(
        id='XADSJFDSF-ADFAF',
        start=datetime(2021, 12, 27, 9, 30, 00),
        end=datetime(2021, 12, 27, 11, 00, 00)
    )
    assert observed_session == expected_session


def test_can_get_list_of_workshops():
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
            
    def list_workshops(self) -> Set[str]:
        group_id = 'TOP-SECRET'    
        all_meeting_ids: Set[str] = set()
        
        user_ids = self.zoom_api.list_users_in_group(group_id=group_id)
        for user_id in user_ids:
            data = self.zoom_api.list_scheduled_meetings_of_user(access_token=self.access_token, user_id=user_id)
            meeting_ids = set(data['meetings'])
            all_meeting_ids.update(meeting_ids)
        return all_meeting_ids
    
    def get_workshop(self, workshop_id: str) -> PlannedWorkshopDTO:
        data = self.zoom_api.get_meeting(access_token=self.access_token, meeting_id=workshop_id)
        return PlannedWorkshopDTO(
            id=str(data['id']),
            name=data['topic'],
            description=data['agenda'],
            planned_start=(planned_start := datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%SZ')),
            planned_end=planned_start + timedelta(minutes=data['duration']),
            session_ids=[],
        )
    
    def get_session(self, session_id: str) -> PlannedSessionDTO:
        data: ZoomGetMeetingResponseData = self.zoom_api.get_meeting(
            url = f"https://api.zoom.us/v2/meetings/{session_id}", 
            headers = {'Authorization': f"Bearer {self.access_token}"}
        )
        return PlannedSessionDTO(
            id=data['id'],
            start=(start := datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%SZ')),
            end=start + timedelta(minutes=data['duration']),
        )
        

class ZoomRestApi:
    
    @staticmethod
    def get_meeting(access_token, meeting_id) -> ZoomGetMeetingResponseData:
        response = requests.get(
            url = f"https://api.zoom.us/v2/meetings/{meeting_id}", 
            headers = {'Authorization': f"Bearer {access_token}"}
        )
        response.raise_for_status()
        data: ZoomGetMeetingResponseData = response.json()
        return data
    
    @staticmethod
    def list_scheduled_meetings_of_user(access_token, user_id) -> ZoomListMeetingsResponseData:
        response = requests.get(
            url=f"https://api.zoom.us/v2/users/{user_id}/meetings",
            params={'type': 'scheduled'},  #, 'from': from_date, 'to': to_date}
            headers = {'Authorization': f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data: ZoomListMeetingsResponseData = response.json()
        return data
        
        
    @staticmethod
    def list_users_in_group(access_token, group_id):
        response = requests.get(
            url = f"https://api.zoom.us/v2/groups/{group_id}/members",
            headers = {'Authorization': f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data: ZoomListMeetingsResponseData = response.json()
        return data
        
        
        
class ZoomGetMeetingResponseData(TypedDict):
    id: Union[int, str]
    topic: str
    start_time: str # planned start: '%Y-%m-%dT%H:%M:%SZ'
    duration: int # minutes
    agenda: str
    
class ZoomListMeetingsResponseData(TypedDict):
            meetings: None