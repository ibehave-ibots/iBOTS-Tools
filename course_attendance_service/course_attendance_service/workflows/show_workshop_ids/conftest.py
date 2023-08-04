from unittest.mock import Mock

import pytest

from .core.workflow import WorkshopRepo
from .adapters.repo_inmemory import InMemoryWorkshopRepo
from .adapters.repo_zoom import ZoomWorkshopRepo
from ..external.zoom_api import ZoomRestApi

    
@pytest.fixture
def zoom_workshop_repo():
    api = Mock(ZoomRestApi)
    api.list_users_in_group.return_value = ['emma', 'addy']
    api.list_scheduled_meetings_of_user.side_effect = [
        {'meetings': ['AA', 'BB']},
        {'meetings': ['CC']},
    ]
    repo = ZoomWorkshopRepo(zoom_api=api)
    return repo

      
@pytest.fixture
def inmemory_workshop_repo() -> InMemoryWorkshopRepo:
    given_workshops = [
        {'id': 'AA'}, 
        {'id': 'BB'}, 
        {'id': 'CC'}, 
    ]
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    return repo
  
  
@pytest.fixture(params=['in-memory', 'zoom'])
def workshop_repo(request, zoom_workshop_repo, inmemory_workshop_repo) -> WorkshopRepo:
    if request.param == 'in-memory':
        return inmemory_workshop_repo
    elif request.param == 'zoom':
        return zoom_workshop_repo
        