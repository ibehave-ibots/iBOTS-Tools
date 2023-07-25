from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple, Union

###### Tests


def test_total_number_of_registrants():
    # GIVEN: a workshop
    workshops = {
        "workshop1": [
            Registrant(name="Mo", affiliation="Uni Tuebingen", status="Denied"),
            Registrant(name="Sang", affiliation="UKB", status="approved"),
            Registrant(name="Nick", affiliation="Uni Bonn", status="Pending"),
        ],
        "workshop2": [
            Registrant(name="Sang", affiliation="UKB", status="approved"),
            Registrant(name="Nick", affiliation="Uni Bonn", status="Pending"),
        ],
    }
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    registration_workflows = RegistrationWorkflows(registrants_repo)

    # WHEN: asked for the number registrants
    registrants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    registrants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )

    # THEN: correct number of registrants is returned
    assert registrants_report1.total_registrants == 3
    assert registrants_report2.total_registrants == 2


###### Entities


class Registrant(NamedTuple):
    name: str
    affiliation: Union[str, List[str]]
    status: str


###### Workflows


class RegistrantsRepo(ABC):
    @abstractmethod
    def get_list_of_registrants(self, workshop_id: Any) -> List[Registrant]:
        return 1


class RegistrantsReport(NamedTuple):
    registrants: List[Registrant]

    @property
    def total_registrants(self):
        return len(self.registrants)


class RegistrationWorkflows:
    def __init__(self, registrants_repo: RegistrantsRepo):
        self.registrants_repo = registrants_repo

    def get_registrants_report(self, workshop_id):
        registrants = self.registrants_repo.get_list_of_registrants(
            workshop_id=workshop_id
        )
        return RegistrantsReport(registrants)


###### Repositories


class InMemoryRegistrantsRepo(RegistrantsRepo):
    def __init__(self, workshops: Dict[Any, List[Registrant]]):
        self.workshops = workshops

    def get_list_of_registrants(self, workshop_id: Any) -> List[Registrant]:
        return self.workshops[workshop_id]
