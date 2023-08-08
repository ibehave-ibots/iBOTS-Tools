from typing import NamedTuple
from unittest.mock import Mock
import pytest
from .adapters.registrants_repo_inmemory import InMemoryRegistrantsRepo
from .adapters.contact_info_presenter_print import PrintContactInfoPresenter
from .adapters.contact_info_formatter_gmail import GmailContactInfoFormatter
from .core.workflows import RegistrationWorkflows
from ..external.console import Console

# I went back to using MockRegistrant because "name" seems to be a keyword for Mock
class MockRegistrant(NamedTuple):
    name: str
    email: str
    status: str


@pytest.fixture
def workshops():
    return {
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

@pytest.fixture
def console():
    return Mock(Console)

@pytest.fixture
def presenter(console):
    contact_info_formatter = GmailContactInfoFormatter()
    presenter = PrintContactInfoPresenter(formatter=contact_info_formatter, console=console)
    return presenter

@pytest.fixture
def registration_workflows(workshops):
    registrants_repo = InMemoryRegistrantsRepo(workshops)
    registration_workflows = RegistrationWorkflows(registrants_repo=registrants_repo)
    return registration_workflows