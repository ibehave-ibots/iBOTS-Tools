from typing import List, NamedTuple
from .entities import Registrant
from .contact_info_presenter_repo import ContactInfoPresenterRepo
from .registrants_repo import RegistrantsRepo

###### Workflows


class RegistrantsReport(NamedTuple):
    registrants: List[Registrant]

    def get_registrants_for_a_specific_status(self, status: str) -> int:
        status_specific_registrants = [
            registrant
            for registrant in self.registrants
            if registrant.status.lower() == status.lower()
        ]
        return status_specific_registrants

    def get_number_of_registrants_for_a_specific_status(self, status: str) -> int:
        return len(self.get_registrants_for_a_specific_status(status=status))

    @property
    def total_number_of_registrants(self) -> int:
        return len(self.registrants)

    @property
    def number_of_approved_registrants(self) -> int:
        return self.get_number_of_registrants_for_a_specific_status(status="approved")

    @property
    def number_of_denied_registrants(self) -> int:
        return self.get_number_of_registrants_for_a_specific_status(status="denied")

    @property
    def number_of_pending_registrants(self) -> int:
        return self.get_number_of_registrants_for_a_specific_status(status="pending")

    @property
    def all_registrants(self) -> List[Registrant]:
        return self.registrants

    @property
    def approved_registrants(self) -> List[Registrant]:
        return self.get_registrants_for_a_specific_status(status="approved")

    @property
    def denied_registrants(self) -> List[Registrant]:
        return self.get_registrants_for_a_specific_status(status="denied")

    @property
    def pending_registrants(self) -> List[Registrant]:
        return self.get_registrants_for_a_specific_status(status="pending")


class RegistrantsContactInfo(NamedTuple):
    registrants = List[Registrant]


class RegistrationWorkflows(NamedTuple):
    registrants_repo: RegistrantsRepo
    contact_info_repo: ContactInfoPresenterRepo

    def get_registrants_report(self, workshop_id):
        registrants = self.registrants_repo.get_list_of_registrants(
            workshop_id=workshop_id
        )
        return RegistrantsReport(registrants)

    def display_approved_registrants_contact_info(self, workshop_id):
        registrants = self.registrants_repo.get_list_of_registrants(
            workshop_id=workshop_id
        )
        approved_registrants = [
            registrant for registrant in registrants if registrant.status == "approved"
        ]
        self.contact_info_repo.display_contact_info(registrants=approved_registrants)
