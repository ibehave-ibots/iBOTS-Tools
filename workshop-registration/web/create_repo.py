from adapters import InMemoryRegistrationRepo
from app.registrationrepo import RegistrationRecord
from app.registrationrepo import RegistrationRepo




def create_repo() -> RegistrationRepo:
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

    return repo