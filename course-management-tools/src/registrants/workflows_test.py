def test_total_number_of_registrants(registration_workflows):
    # GIVEN: a workshop
    # WHEN: asked for the number registrants
    # THEN: correct number of registrants is returned

    registrants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    assert registrants_report1.total_number_of_registrants == 3

    registrants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    assert registrants_report2.total_number_of_registrants == 4


def test_number_of_approved_registrants(registration_workflows):
    # GIVEN: a workshop
    # WHEN: asked for the number of approved particpants
    # THEN: the correct number of participants is returned

    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    assert registratants_report1.number_of_approved_registrants == 1

    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    assert registratants_report2.number_of_approved_registrants == 2


def test_number_of_denied_registrants(registration_workflows):
    # GIVEN: a workshop
    # WHEN: asked for the number of denied particpants
    # THEN: the correct number of participants is returned

    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    assert registratants_report1.number_of_denied_registrants == 1

    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    assert registratants_report2.number_of_denied_registrants == 1


def test_number_of_pending_registrants(registration_workflows):
    # GIVEN: a workshop
    # WHEN: asked for the number of pending particpants
    # THEN: the correct number of participants is returned

    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    assert registratants_report1.number_of_pending_registrants == 1

    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    assert registratants_report2.number_of_pending_registrants == 1


def test_registrants_are_correct(registration_workflows):
    # GIVEN: a workshop
    # WHEN: asked for a list of registrants
    # THEN: correct registrants are returned

    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    expected_outcome1 = ["denied", "approved", "pending"]
    observed_outcome1 = [
        registrant.status for registrant in registratants_report1.registrants
    ]
    assert observed_outcome1 == expected_outcome1

    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    expected_outcome2 = ["approved", "approved", "pending", "denied"]
    observed_outcome2 = [
        registrant.status for registrant in registratants_report2.registrants
    ]
    assert observed_outcome2 == expected_outcome2


def test_approved_registrants_are_correct(registration_workflows):
    # GIVEN: a workshop
    # WHEN: asked for a list of approved registrants
    # THEN: correct registrants are returned

    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    expected_outcome1 = ["approved"]
    observed_outcome1 = [
        registrant.status
        for registrant in registratants_report1.registrants
        if registrant.status == "approved"
    ]
    assert observed_outcome1 == expected_outcome1

    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    expected_outcome2 = ["approved", "approved"]
    observed_outcome2 = [
        registrant.status
        for registrant in registratants_report2.registrants
        if registrant.status == "approved"
    ]
    assert observed_outcome2 == expected_outcome2


def test_denied_registrants_are_correct(registration_workflows):
    # GIVEN: a workshop
    # WHEN: asked for a list of denied registrants
    # THEN: correct registrants are returned

    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    expected_outcome1 = ["denied"]
    observed_outcome1 = [
        registrant.status
        for registrant in registratants_report1.registrants
        if registrant.status == "denied"
    ]
    assert observed_outcome1 == expected_outcome1

    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    expected_outcome2 = ["denied"]
    observed_outcome2 = [
        registrant.status
        for registrant in registratants_report2.registrants
        if registrant.status == "denied"
    ]
    assert observed_outcome2 == expected_outcome2


def test_pending_registrants_are_correct(registration_workflows):
    # GIVEN: a workshop
    # WHEN: asked for a list of pending registrants
    # THEN: correct registrants are returned

    registratants_report1 = registration_workflows.get_registrants_report(
        workshop_id="workshop1"
    )
    expected_outcome1 = ["pending"]
    observed_outcome1 = [
        registrant.status
        for registrant in registratants_report1.registrants
        if registrant.status == "pending"
    ]
    assert observed_outcome1 == expected_outcome1

    registratants_report2 = registration_workflows.get_registrants_report(
        workshop_id="workshop2"
    )
    expected_outcome2 = ["pending"]
    observed_outcome2 = [
        registrant.status
        for registrant in registratants_report2.registrants
        if registrant.status == "pending"
    ]
    assert observed_outcome2 == expected_outcome2


def test_approved_registrants_contact_info_display(
    console, presenter, registration_workflows
):
    # GIVEN: a workshop
    # WHEN: asked to display contact info of approved registrants
    # THEN: contact info is displayed in the correct format

    registration_workflows.display_approved_registrants_contact_info(
        workshop_id="workshop1",
        presenter=presenter,
    )
    expected_outcome1 = "email2@gmail.com,\n"
    observed_outcome1 = console.print.call_args[0][0]
    assert observed_outcome1 == expected_outcome1

    registration_workflows.display_approved_registrants_contact_info(
        workshop_id="workshop2",
        presenter=presenter,
    )
    expected_outcome2 = "email1@gmail.com,\nemail2@gmail.com,\n"
    observed_outcome2 = console.print.call_args[0][0]
    assert observed_outcome2 == expected_outcome2
