from __future__ import annotations
from abc import ABC
from datetime import datetime, timedelta
from typing import Protocol, Set, TypedDict, Union
from unittest.mock import Mock, patch

import requests

from .workflows import WorkshopRepo, PlannedSessionDTO, PlannedWorkshopDTO


def test_can_get_workshop():
    response = Mock()
    response.json.return_value = {
        'id': 123,  # an int
        'topic': 'intro to python',
        'start_time':  '2021-12-25T9:30:00Z', # '%Y-%m-%dT%H:%M:%SZ'
        'duration': 60, # minutes
        'agenda': 'a neat workshop, join us!',
    }    
    requests = Mock(HttpRequester)
    requests.get.return_value = response
    repo = ZoomWorkshopRepo(requests=requests)
    
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
    response = Mock()
    response.json.return_value = {
        'id': 'XADSJFDSF-ADFAF',  # a string
        'start_time':  '2021-12-27T9:30:00Z', # '%Y-%m-%dT%H:%M:%SZ'
        'duration': 90, # minutes
    }   
    requests = Mock(HttpRequester)
    requests.get.return_value = response
    repo = ZoomWorkshopRepo(requests=requests)
    observed_session = repo.get_session(session_id='XADSJFDSF-ADFAF')
    expected_session = PlannedSessionDTO(
        id='XADSJFDSF-ADFAF',
        start=datetime(2021, 12, 27, 9, 30, 00),
        end=datetime(2021, 12, 27, 11, 00, 00)
    )
    assert observed_session == expected_session


class HttpRequester(Protocol):
    def get(self, url: str, headers = None, params = None): ...
    def post(self, url: str, headers = None, params = None, data = None): ...
    

class ZoomWorkshopRepo(WorkshopRepo):
    
    def __init__(self, requests: HttpRequester = requests) -> None:
            self.requests = requests
            self.access_token = 'TOP-SECRET'
    
    def list_workshops(self) -> Set[str]:
        raise NotImplementedError
    
    def get_workshop(self, workshop_id: str) -> PlannedWorkshopDTO:
        response: ZoomGetMeetingResponse = self.requests.get(
            url = f"https://api.zoom.us/v2/meetings/{workshop_id}", 
            headers = {'Authorization': f"Bearer {self.access_token}"}
        ).json()
        return PlannedWorkshopDTO(
            id=str(response['id']),
            name=response['topic'],
            description=response['agenda'],
            planned_start=(planned_start := datetime.strptime(response['start_time'], '%Y-%m-%dT%H:%M:%SZ')),
            planned_end=planned_start + timedelta(minutes=response['duration']),
            session_ids=[],
        )
    
    def get_session(self, session_id: str) -> PlannedSessionDTO:
        response: ZoomGetMeetingResponse = self.requests.get(
            url = f"https://api.zoom.us/v2/meetings/{session_id}", 
            headers = {'Authorization': f"Bearer {self.access_token}"}
        ).json()
        return PlannedSessionDTO(
            id=response['id'],
            start=(start := datetime.strptime(response['start_time'], '%Y-%m-%dT%H:%M:%SZ')),
            end=start + timedelta(minutes=response['duration']),
        )
        
        
        
class ZoomGetMeetingResponse(TypedDict):
    id: Union[int, str]
    topic: str
    start_time: str # planned start: '%Y-%m-%dT%H:%M:%SZ'
    duration: int # minutes
    agenda: str
    
     