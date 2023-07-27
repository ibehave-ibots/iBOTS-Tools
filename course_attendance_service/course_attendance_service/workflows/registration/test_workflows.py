from .repo_inmemory import InMemoryRegistrantsRepo
from .workflows import RegistrationWorkflows, Registrant


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


def test_number_of_approved_registrants():
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


def test_number_of_denied_registrants():
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


def test_number_of_pending_registrants():
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
