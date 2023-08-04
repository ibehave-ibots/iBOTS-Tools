from __future__ import annotations
from collections import defaultdict
from datetime import date, datetime
from textwrap import dedent
from unittest.mock import Mock

from ..core.workflow import SessionRecord, WorkshopRecord
from ...external.zoom_api import ZoomRestApi
from .workshop_repo_zoom import ZoomWorkshopRepo


def test_repo_can_get_workshop_from_zoom_api():
    api = Mock(ZoomRestApi)
    api.get_meeting.return_value = {
        'id': 123,  # an int
        'topic': 'intro to python',
        'start_time':  '2021-12-25T9:30:00Z', # '%Y-%m-%dT%H:%M:%SZ'
        'duration': 60, # minutes
        'agenda': dedent("""
            ## Workshop Description
            a neat workshop, join us!
            
            
            ## Workshop Topics:
              - What is Python?
              - Where is Python?
              - Why is Python?
              
            
            ## Organizer
            The Awesome iBOTS
   
   
        """),
    }
    repo = ZoomWorkshopRepo(zoom_api=api)
    
    observed_workshop = repo.get_workshop(workshop_id='123')
    expected_workshop = WorkshopRecord(
        id='123',
        name='intro to python',
        description='a neat workshop, join us!',
        topics=[
            'What is Python?',
            'Where is Python?',
            'Why is Python?',
        ],
        scheduled_start=date(2021, 12, 25),
        scheduled_end=date(2021, 12, 25),
        session_ids=[],
        organizer='The Awesome iBOTS',
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



def test_repo_interprets_multisession_workshops_as_a_longer_workshop():
    api = Mock(ZoomRestApi)
    api.get_meeting.return_value = {
        'id': 123, 
        'start_time':  '2021-12-25T9:30:00Z', 
        'duration': 60, 
        'agenda': '',
        'topic': '',
        'occurences': [
            {'start_time': '2021-12-25T9:30:00Z', 'duration': 0},
            {'start_time': '2021-12-26T9:30:00Z', 'duration': 0},
            {'start_time': '2021-12-27T9:30:00Z', 'duration': 0},
            
        ],
    }
    
    repo = ZoomWorkshopRepo(zoom_api=api)
    
    workshop = repo.get_workshop(workshop_id=123)
    assert workshop.scheduled_start == date(2021, 12, 25)
    assert workshop.scheduled_end == date(2021, 12, 27)
    
    