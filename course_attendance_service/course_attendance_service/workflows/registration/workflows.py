from abc import ABC, abstractmethod
from typing import Any, List, NamedTuple, Union

###### Entities


class Registrant(NamedTuple):
    user_id: str
    name: str
    affiliation: Union[str, List[str]]
    email: str
    status: str


###### Workflows


class RegistrantsRepo(ABC):
    @abstractmethod
    def get_list_of_registrants(self, workshop_id: Any) -> List[Registrant]:
        pass


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


class RegistrationWorkflows:
    def __init__(self, registrants_repo: RegistrantsRepo):
        self.registrants_repo = registrants_repo

    def get_registrants_report(self, workshop_id):
        registrants = self.registrants_repo.get_list_of_registrants(
            workshop_id=workshop_id
        )
        return RegistrantsReport(registrants)
