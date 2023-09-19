from dataclasses import dataclass
from typing import Callable, List

from app import RegistrationRepo, RegistrationRecord
from external.zoom_api import OAuthGetToken, list_registrants


@dataclass(frozen=True)
class ZoomRegistrationRepo(RegistrationRepo):
    oauth_get_token: OAuthGetToken
    list_registrants: Callable = list_registrants

    def get_registrations(self, workshop_id: str) -> List[RegistrationRecord]:
        access_token = self.oauth_get_token.create_access_token()["access_token"]
        registration_records = []
        zoom_status_mapping = {
            "approved": "approved",
            "pending": "waitlisted",
            "denied": "rejected",
        }
        for status in ["approved", "pending", "denied"]:
            zoom_registrants = self.list_registrants(
                access_token=access_token, meeting_id=workshop_id, status=status
            )
            for zoom_registrant in zoom_registrants:
                registration_record = RegistrationRecord(
                    workshop_id=workshop_id,
                    name=" ".join(
                        [zoom_registrant.first_name, zoom_registrant.last_name]
                    ),
                    status=zoom_status_mapping[zoom_registrant.status],
                    registered_on=zoom_registrant.registered_on,
                    custom_questions=zoom_registrant.custom_questions,
                    email=zoom_registrant.email
                )
                registration_records.append(registration_record)

        return registration_records
