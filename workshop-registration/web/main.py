import sys
sys.path.append('..')

from unittest.mock import Mock

from app.registrant_workflows import RegistrantWorkflows
from app.registrationrepo import RegistrationRecord

from adapters import StreamlitRegistrantPresenter, InMemoryRegistrationRepo
from app import App

repo = InMemoryRegistrationRepo(
    registrations=[
        RegistrationRecord(
            id="54321",
            workshop_id="12345",
            name="eve",
            email="e@e.com",
            registered_on="25092023",
            custom_questions=[{'value': 'Prof. Sangee'}],
            status='approved',
        ),
        RegistrationRecord(
            id="11111",
            workshop_id="12345",
            name="adam",
            email="a@a.com",
            registered_on="26092023",
            custom_questions=[{'value': 'Prof. Bee'}],
            status='waitlisted',
        ),
    ],
)



app = App(
    workshop_workflow=Mock(),
    registrant_workflows=RegistrantWorkflows(
        registration_repo=repo,
        presenter=StreamlitRegistrantPresenter(),
    )
)

app.list_registrants(workshop_id="12345")
