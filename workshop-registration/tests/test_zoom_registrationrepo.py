from dataclasses import dataclass
from typing import Callable, List
from unittest.mock import Mock

import pytest
from app import RegistrationRepo, RegistrationRecord
from external.zoom_api.list_registrants import Registrant, list_registrants
from external.zoom_api import create_access_token

@dataclass(frozen=True)
class ZoomRegistrationRepo(RegistrationRepo):
    list_registrants: Callable

    def get_registrations(self, workshop_id: str) -> List[RegistrationRecord]:
        access_token = create_access_token()
        registrants = self.list_registrants(meeting_id=workshop_id, access_token=access_token, status='approved')

        return registrants



def test_zoom_registration_repo_returns_correct_registrations_for_a_given_workshop():
    # GIVEN 
    list_registrants = Mock()
    list_registrants.return_value = [
        Registrant(),
        Registrant(),
    ]
    repo = ZoomRegistrationRepo(list_registrants=list_registrants)
    
    # WHEN 
    registrations = repo.get_registrations(workshop_id=Mock())

    # THEN
    assert len(registrations) == 2

