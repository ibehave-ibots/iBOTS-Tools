from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock

from .workflows import PlannedSessionDTO, PlannedWorkshopDTO
from .zoom_api import ZoomRestApi
from .repo_zoom import ZoomWorkshopRepo


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
    expected_workshop = PlannedWorkshopDTO(
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
    expected_session = PlannedSessionDTO(
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
    