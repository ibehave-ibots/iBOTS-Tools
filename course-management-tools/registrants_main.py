
from typing import NamedTuple
from unittest.mock import Mock
from src.registration.core.workflows import RegistrationWorkflows
from src.registration.adapters.registrants_repo_inmemory import InMemoryRegistrantsRepo
from src.external.console import Console
from src.registration.adapters.contact_info_formatter_gmail import GmailContactInfoFormatter
from src.registration.adapters.contact_info_presenter_print import PrintContactInfoPresenter
from src.cli.registrants_cli_test import RegistrantsCLI

class MockRegistrant(NamedTuple):
    name: str
    email: str
    status: str

workshops = {
    "workshop1": [
        MockRegistrant(
            name="FirstName1 FamilyName1",
            status="denied",
            email="email1@gmail.com",
        ),
        MockRegistrant(
            name="FirstName2 FamilyName2",
            status="approved",
            email="email2@gmail.com",
        ),
        MockRegistrant(
            name="FirstName3 FamilyName3",
            status="pending",
            email="email3@gmail.com",
        ),
    ],
    "workshop2": [
        MockRegistrant(
            name="FirstName1 FamilyName1",
            status="approved",
            email="email1@gmail.com",
        ),
        MockRegistrant(
            name="FirstName2 FamilyName2",
            status="approved",
            email="email2@gmail.com",
        ),
        MockRegistrant(
            name="FirstName3 FamilyName3",
            status="pending",
            email="email3@gmail.com",
        ),
        MockRegistrant(
            name="FirstName4 FamilyName4",
            status="denied",
            email="email4@gmail.com",
        ),
    ],
}


cli = Mock()
cli.get_input.return_value = "workshop2"

interactor = RegistrantsCLI(
    cli=cli, 
    workflows=RegistrationWorkflows(
        registrants_repo=InMemoryRegistrantsRepo(workshops),
    ), 
    presenter=PrintContactInfoPresenter(
        formatter=GmailContactInfoFormatter(), 
        console=Console()
        )
)
interactor.run()
