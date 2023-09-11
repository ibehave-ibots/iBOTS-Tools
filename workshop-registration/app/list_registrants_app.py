from abc import ABC, abstractmethod
from typing import List, Literal, NamedTuple
from app.registrationrepo import RegistrationRepo



class RegistrantSummary(NamedTuple):
    name: str
    email: str
    status: Literal['approved','waitlisted','rejected']
    registered_on: str
    group_name: str

class Presenter(ABC):

    @abstractmethod
    def show(self, registrants: List[RegistrantSummary]) -> None:
        ...

class ConsolePresenter(Presenter):
    def show(self, registrants: List[RegistrantSummary]) -> None:
        print("Name, Registered_on, email, status, affiliation")
        for registrant in registrants:
            print('%s, %s, %s, %s, %s' %(
                registrant.name, 
                registrant.registered_on,
                registrant.email,
                registrant.status,
                registrant.group_name, 
                )
            )

class ListRegistrantsApp(NamedTuple):
    registration_repo: RegistrationRepo
    presenter: Presenter

    def list_registrants(self, workshop_id: str):
        registration_records = self.registration_repo.get_registrations(workshop_id=workshop_id)
        summaries = []
        for record in registration_records:
            summary = RegistrantSummary(
                name=record.name,
                email=record.email,
                status=record.status,
                registered_on=record.registered_on,
                group_name=record.custom_questions[0]['value']
            )
            summaries.append(summary)
        self.presenter.show(registrants=summaries)

