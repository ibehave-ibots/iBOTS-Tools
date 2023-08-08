from argparse import ArgumentParser
from typing import NamedTuple, Union
from ..adapters.registrants_repo_inmemory import InMemoryRegistrantsRepo
from ..adapters.contact_info_formatter_repo_gmail import GmailContactInfoFormatterRepo
from ..adapters.contact_info_presenter_repo_print import PrintContactInfoPresenterRepo
from ..core.workflows import RegistrationWorkflows


class MockRegistrant(NamedTuple):
    name: str
    email: str
    status: str


workshops = {
    1: [
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
    2: [
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

if __name__ == "__main__":
    # initialize the CLI
    parser = ArgumentParser()
    parser.add_argument(
        "workshop_id", type=int, help="Unique id of a specific workshop."
    )

    # get inputs from the user interface
    args = parser.parse_args()

    # standardize the input
    workshop_id = args.workshop_id

    # create a workflow onject (this must be independet of the cli)
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    contact_info_formatter = GmailContactInfoFormatterRepo()
    contact_info_repo = PrintContactInfoPresenterRepo(formatter=contact_info_formatter)
    registration_workflows = RegistrationWorkflows(
        registrants_repo=registrants_repo, contact_info_repo=contact_info_repo
    )

    # pass the input to the workflow object
    registration_workflows.display_approved_registrants_contact_info(
        workshop_id=workshop_id
    )
