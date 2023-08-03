from datetime import date, datetime
from textwrap import dedent
from unittest.mock import Mock

import pytest

from .core.workshop_repo import WorkshopRepo
from .adapters.workshop_repo_inmemory import InMemoryWorkshopRepo
from .adapters.workshop_repo_zoom import ZoomWorkshopRepo
from .external.zoom_api import ZoomRestApi


@pytest.fixture()
def inmemory_workshop_repo() -> InMemoryWorkshopRepo:
    given_workshops = [
        {
            'id': 'ABCD', 
            'name': "Intro to Python",
            'description': "A fun workshop on Python!",
            'topics': [
                'What code is.',
                'Why to code.',
                'How to code.',
            ],
            'scheduled_start': date(2023, 8, 9),
            'scheduled_end': date(2023, 8, 14),
            'sessions': [
                {'id': 'aaa', 
                'scheduled_start': datetime(2023, 8, 9, 9, 30, 00), 
                'scheduled_end': datetime(2023, 8, 9, 13, 00),
                }],
            'organizer': 'The iBOTS',
        },
    ]
    
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    return repo
                               

@pytest.fixture
def zoom_workshop_repo() -> ZoomWorkshopRepo:
    api = Mock(ZoomRestApi)
    api.get_meeting.return_value = {
        'id': 'ABCD',  
        'topic': 'Intro to Python',
        'start_time':  '2023-08-09T9:30:00Z',
        'duration': 210, # minutes
        'agenda': dedent("""
            ## Workshop Description
            A fun workshop on Python!
            
            
            ## Workshop Topics:
              - What code is.
              - Why to code.
              - How to code.
              
            
            ## Organizer
            The iBOTS
   
   
        """),
    }
    repo = ZoomWorkshopRepo(zoom_api=api)
    return repo


@pytest.fixture(params=['inmemory_repo', 'zoom_repo'])
def workshop_repo(request, inmemory_workshop_repo, zoom_workshop_repo) -> WorkshopRepo:
    if request.param == 'inmemory_repo':
        return inmemory_workshop_repo
    elif request.param == 'zoom_repo':
        return zoom_workshop_repo
    
