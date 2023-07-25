from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple, Union

###### Tests


def test_total_number_of_registrants():
    # GIVEN: a workshop
    workshops = {
        "workshop1": [
            Registrant(name="Mo", affiliation="Uni Tuebingen", status="denied"),
            Registrant(name="Sang", affiliation="UKB", status="approved"),
            Registrant(name="Nick", affiliation="Uni Bonn", status="pending"),
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


def test_number_of_approved_registrants_is_correct():
    # GIVEN: a workshop
    workshops = {
        "workshop1": [
            Registrant(name="Mo", affiliation="Uni Tuebingen", status="denied"),
            Registrant(name="Sang", affiliation="UKB", status="approved"),
            Registrant(name="Nick", affiliation="Uni Bonn", status="pending"),
        ],
        "workshop2": [
            Registrant(name="Mo", affiliation="Uni Tuebingen", status="approved"),
            Registrant(name="Sang", affiliation="UKB", status="approved"),
            Registrant(name="Nick", affiliation="Uni Bonn", status="pending"),
        ],
    }
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    registration_workflows = RegistrationWorkflows(registrants_repo)

    # WHEN: asked for the number of approved particpants
    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )

    # THEN: the correct number of participants is returned
    assert registratants_report1.number_of_approved_registrants == 1
    assert registratants_report2.number_of_approved_registrants == 2


def test_number_of_denied_registrants_is_correct():
    # GIVEN: a workshop
    workshops = {
        "workshop1": [
            Registrant(name="Mo", affiliation="Uni Tuebingen", status="denied"),
            Registrant(name="Sang", affiliation="UKB", status="approved"),
            Registrant(name="Nick", affiliation="Uni Bonn", status="pending"),
        ],
        "workshop2": [
            Registrant(name="Mo", affiliation="Uni Tuebingen", status="approved"),
            Registrant(name="Sang", affiliation="UKB", status="approved"),
            Registrant(name="Nick", affiliation="Uni Bonn", status="pending"),
        ],
    }
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    registration_workflows = RegistrationWorkflows(registrants_repo)

    # WHEN: asked for the number of denied particpants
    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )

    # THEN: the correct number of participants is returned
    assert registratants_report1.number_of_denied_registrants == 1
    assert registratants_report2.number_of_denied_registrants == 0


def test_number_of_pending_registrants_is_correct():
    # GIVEN: a workshop
    workshops = {
        "workshop1": [
            Registrant(name="Mo", affiliation="Uni Tuebingen", status="denied"),
            Registrant(name="Sang", affiliation="UKB", status="approved"),
            Registrant(name="Nick", affiliation="Uni Bonn", status="pending"),
        ],
        "workshop2": [
            Registrant(name="Mo", affiliation="Uni Tuebingen", status="approved"),
            Registrant(name="Sang", affiliation="UKB", status="approved"),
            Registrant(name="Nick", affiliation="Uni Bonn", status="pending"),
        ],
    }
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    registration_workflows = RegistrationWorkflows(registrants_repo)

    # WHEN: asked for the number of pending particpants
    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )

    # THEN: the correct number of participants is returned
    assert registratants_report1.number_of_pending_registrants == 1
    assert registratants_report2.number_of_pending_registrants == 1


###### Entities


class Registrant(NamedTuple):
    name: str
    affiliation: Union[str, List[str]]
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


###### Repositories


class InMemoryRegistrantsRepo(RegistrantsRepo):
    def __init__(self, workshops: Dict[Any, List[Registrant]]):
        self.workshops = workshops

    def get_list_of_registrants(self, workshop_id: Any) -> List[Registrant]:
        return self.workshops[workshop_id]
