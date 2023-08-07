from __future__ import annotations
from unittest.mock import Mock

from .repo_zoom import ZoomWorkshopRepo
from ...external.zoom_api import ZoomRestApi


def test_repo_can_get_list_of_workshops_from_zoom_api():
    api = Mock(ZoomRestApi)
    api.list_users_in_group.return_value = ['emma', 'addy']
    api.list_scheduled_meetings_of_user.side_effect = [
        {'meetings': ['aa', 'bb', 'cc']},
        {'meetings': ['ee', 'ff', 'gg']},
    ]
    
    repo = ZoomWorkshopRepo(zoom_api=api)
    
    observed_workshop_ids = repo.list_workshops()
    expected_workshop_ids = ['aa', 'bb', 'cc', 'ee', 'ff', 'gg']
    assert observed_workshop_ids == expected_workshop_ids
    