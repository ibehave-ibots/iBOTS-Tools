from typing import NamedTuple
import pytest
from .repo_inmemory import InMemoryRegistrantsRepo
from .workflows import RegistrationWorkflows


class MockRegistrant(NamedTuple):
    status: str


@pytest.fixture
def workshops():
    return {
        "workshop1": [
            MockRegistrant(status="denied"),
            MockRegistrant(status="approved"),
            MockRegistrant(status="pending"),
        ],
        "workshop2": [
            MockRegistrant(status="approved"),
            MockRegistrant(status="approved"),
            MockRegistrant(status="pending"),
            MockRegistrant(status="denied"),
        ],
    }


def test_total_number_of_registrants(workshops):
    # GIVEN: a workshop
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
    assert registrants_report2.total_registrants == 4


def test_number_of_approved_registrants(workshops):
    # GIVEN: a workshop
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


def test_number_of_denied_registrants(workshops):
    # GIVEN: a workshop
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
    assert registratants_report2.number_of_denied_registrants == 1


def test_number_of_pending_registrants(workshops):
    # GIVEN: a workshop
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
