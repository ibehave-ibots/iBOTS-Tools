from abc import ABC, abstractmethod
from typing import List, Literal, NamedTuple
from app.registrationrepo import RegistrationRepo
from .list_registrant_presenter import ListRegistrantPresenter, RegistrantSummary

class ListRegistrantsApp(NamedTuple):
    registration_repo: RegistrationRepo
    presenter: ListRegistrantPresenter

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

