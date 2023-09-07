from dataclasses import dataclass
from typing import Callable, List
from unittest.mock import Mock

from app import RegistrationRepo, RegistrationRecord
from external.zoom_api import create_access_token

@dataclass(frozen=True)
class ZoomRegistrationRepo(RegistrationRepo):
    list_registrants: Callable

    def get_registrations(self, workshop_id: str) -> List[RegistrationRecord]:
        access_token = create_access_token()["access_token"]
        registration_records = []
        for status in ["approved", "pending", "denied"]:
            zoom_registrants = self.list_registrants(access_token=access_token, meeting_id=workshop_id, status=status)
            for zoom_registrant in zoom_registrants:
                registration_record = RegistrationRecord(
                    workshop_id=Mock(),
                    name=" ".join([zoom_registrant.first_name, zoom_registrant.last_name]),
                    status=zoom_registrant.status
                )
                registration_records.append(registration_record)
            
        return registration_records