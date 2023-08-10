from typing import NamedTuple
from src.registrants.core.workflows import RegistrantsWorkflows
from src.registrants.adapters.registrants_repo_inmemory import InMemoryRegistrantsRepo
from src.external.console import Console
from src.registrants.adapters.contact_info_formatter_gmail import (
    GmailContactInfoFormatter,
)
from src.registrants.adapters.contact_info_presenter_print import (
    PrintContactInfoPresenter,
)
from src.registrants.interactors.cli import RegistrantsCLIInteractor
from src.registrants.adapters.cli_argparse import ArgparseCLI


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

interactor = RegistrantsCLIInteractor(
    cli=ArgparseCLI(),
    workflows=RegistrantsWorkflows(
        registrants_repo=InMemoryRegistrantsRepo(workshops),
    ),
    presenter=PrintContactInfoPresenter(
        formatter=GmailContactInfoFormatter(), console=Console()
    ),
)
interactor.display_approved_registrants_contact_info()
