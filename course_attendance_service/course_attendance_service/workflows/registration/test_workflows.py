from typing import NamedTuple
from unittest.mock import Mock
import pytest
from .repo_inmemory import InMemoryRegistrantsRepo
from .workflows import RegistrationWorkflows, Registrant


@pytest.fixture
def workshops():
    return {
        "workshop1": [
            Mock(Registrant, status="denied"),
            Mock(Registrant, status="approved"),
            Mock(Registrant, status="pending"),
        ],
        "workshop2": [
            Mock(Registrant, status="approved"),
            Mock(Registrant, status="approved"),
            Mock(Registrant, status="pending"),
            Mock(Registrant, status="denied"),
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
    assert registrants_report1.total_number_of_registrants == 3
    assert registrants_report2.total_number_of_registrants == 4


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


def test_registrants_are_correct(workshops):
    # GIVEN: a workshop
    # WHEN: asked for a list of registrants
    # THEN: correct registrants are returned
    
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    registration_workflows = RegistrationWorkflows(registrants_repo)
    
    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    expected_outcome1 = ["denied", "approved", "pending"]
    observed_outcome1 = [registrant.status for registrant in registratants_report1.registrants]
    assert observed_outcome1 == expected_outcome1
    
    
    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    expected_outcome2 = ["approved", "approved", "pending", "denied"]
    observed_outcome2 = [registrant.status for registrant in registratants_report2.registrants]
    assert observed_outcome2 == expected_outcome2


def test_approved_registrants_are_correct(workshops):
    # GIVEN: a workshop
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    registration_workflows = RegistrationWorkflows(registrants_repo)

    # WHEN: asked for a list of approved registrants
    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    expected_outcome1 = ["approved"]
    observed_outcome1 = [registrant.status for registrant in registratants_report1.registrants if registrant.status == "approved"]
    assert observed_outcome1 == expected_outcome1
    
    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    expected_outcome2 = ["approved", "approved"]
    observed_outcome2 = [registrant.status for registrant in registratants_report2.registrants if registrant.status == "approved"]
    assert observed_outcome2 == expected_outcome2


def test_denied_registrants_are_correct(workshops):
    # GIVEN: a workshop
    # WHEN: asked for a list of registrants    
    # THEN: correct registrants are returned
    
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    registration_workflows = RegistrationWorkflows(registrants_repo)

    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    expected_outcome1 = ["denied"]
    observed_outcome1 = [registrant.status for registrant in registratants_report1.registrants if registrant.status == "denied"]
    assert observed_outcome1 == expected_outcome1
    
    
    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    expected_outcome2 = ["denied"]
    observed_outcome2 = [registrant.status for registrant in registratants_report2.registrants if registrant.status == "denied"]
    assert observed_outcome2 == expected_outcome2


def test_pending_registrants_are_correct(workshops):
    # GIVEN: a workshop
    # WHEN: asked for a list of registrants
    
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    registration_workflows = RegistrationWorkflows(registrants_repo)

    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    expected_outcome1 = ["pending"]
    observed_outcome1 = [registrant.status for registrant in registratants_report1.registrants if registrant.status == "pending"]
    assert observed_outcome1 == expected_outcome1
    
    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    expected_outcome2 = ["pending"]
    observed_outcome2 = [registrant.status for registrant in registratants_report2.registrants if registrant.status == "pending"]
    assert observed_outcome2 == expected_outcome2
