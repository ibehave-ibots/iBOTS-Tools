from typing import NamedTuple
from ..external.cli import CLI
from ..core.contact_info_controller import ContactInfoController
from .registrants_repo_inmemory import InMemoryRegistrantsRepo
from .contact_info_formatter_repo_gmail import GmailContactInfoFormatterRepo
from .contact_info_repo_print import PrintContactInfoRepo
from ..core.workflows import RegistrationWorkflows


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


class CLIController(ContactInfoController):
    def __init__(self, cli: CLI, registration_workflows: RegistrationWorkflows):
        self.cli = cli
        self.registration_workflows = registration_workflows

    def get_contact_info(self):
        workshop_id = self.cli.get_workshop_id_from_user()
        self.registration_workflows.display_approved_registrants_contact_info(
            workshop_id=workshop_id
        )


if __name__ == "__main__":
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    contact_info_formatter = GmailContactInfoFormatterRepo()
    contact_info_repo = PrintContactInfoRepo(formatter=contact_info_formatter)
    registration_workflows = RegistrationWorkflows(
        registrants_repo=registrants_repo, contact_info_repo=contact_info_repo
    )
    cli = CLI()
    user_interface = CLIController(
        cli=cli, registration_workflows=registration_workflows
    )
    user_interface.get_contact_info()
