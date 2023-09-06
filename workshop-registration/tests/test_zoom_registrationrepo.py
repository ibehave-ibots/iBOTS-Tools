from dataclasses import dataclass
from typing import List
from unittest.mock import Mock

import pytest
from app import RegistrationRepo, RegistrationRecord
from external.zoom_api import ZoomAPI
from external.zoom_api.list_registrants import Registrant

@dataclass(frozen=True)
class ZoomRegistrationRepo(RegistrationRepo):
    zoom_api: ZoomAPI
    
    def get_registrations(self, workshop_id: str) -> List[RegistrationRecord]:
        registrants = self.zoom_api.list_registrants(meeting_id=workshop_id)

        return registrants



def test_zoom_registration_repo_returns_correct_registrations_for_a_given_workshop():
    # GIVEN 
    zoom_api=ZoomAPI()
    zoom_api.list_registrants = Mock()
    zoom_api.list_registrants.return_value = [
        Registrant(),
        Registrant(),
    ]
    
    repo = ZoomRegistrationRepo(zoom_api=zoom_api)
    # WHEN 
    registrations = repo.get_registrations(workshop_id=Mock())

    # THEN
    assert len(registrations) == 2

