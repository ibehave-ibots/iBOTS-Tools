from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple, Union

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

    @property
    def total_registrants(self) -> int:
        return len(self.registrants)

    def get_number_of_registrants_for_a_specific_status(self, status: str) -> int:
        return sum(
            [
                1 if registrant.status.lower() == status.lower() else 0
                for registrant in self.registrants
            ]
        )

    @property
    def number_of_approved_registrants(self) -> int:
        return self.get_number_of_registrants_for_a_specific_status(status="approved")

    @property
    def number_of_denied_registrants(self) -> int:
        return self.get_number_of_registrants_for_a_specific_status(status="denied")

    @property
    def number_of_pending_registrants(self) -> int:
        return self.get_number_of_registrants_for_a_specific_status(status="pending")


class RegistrationWorkflows:
    def __init__(self, registrants_repo: RegistrantsRepo):
        self.registrants_repo = registrants_repo

    def get_registrants_report(self, workshop_id):
        registrants = self.registrants_repo.get_list_of_registrants(
            workshop_id=workshop_id
        )
        return RegistrantsReport(registrants)
