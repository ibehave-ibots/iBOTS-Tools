from abc import ABC, abstractmethod
from dataclasses import replace
from typing import List, Literal, NamedTuple, Optional
from app.registrationrepo import RegistrationRecord, RegistrationRepo
from .list_registrant_presenter import ListRegistrantPresenter, RegistrantSummary

class RegistrantWorkflows(NamedTuple):
    registration_repo: RegistrationRepo
    presenter: ListRegistrantPresenter

    def list_registrants(self, workshop_id: str, status: Optional[Literal['approved', 'waitlisted', 'rejected']] = None) -> None:
        registration_records = self.registration_repo.get_registrations(workshop_id=workshop_id)
        summaries = []
        for record in registration_records:
            if status and record.status != status:
                continue
            
            summary = self._make_summary(record=record)
            summaries.append(summary)
        
        sorted_summaries = list(sorted(summaries, key=lambda s: s.registered_on))
        self.presenter.show(registrants=sorted_summaries)

    def update_registrant_status(
            self,
            workshop_id: str, 
            registration_id: str,
            to_status: Literal['approved', 'rejected'],
        )  -> None:
        registrations = self.registration_repo.get_registrations(workshop_id=workshop_id)
        for idx, registration in enumerate(registrations):
            if registration.id == registration_id:
                updated_registration = replace(registration, status=to_status)
                self.registration_repo.registrations[workshop_id][idx] = updated_registration
                summary = self._make_summary(updated_registration)
                self.presenter.show_update(registrant=summary)
                break

    def _make_summary(self, record: RegistrationRecord):
        summary = RegistrantSummary(
                    workshop_id=record.workshop_id,
                    id=record.id,
                    name=record.name,
                    email=record.email,
                    status=record.status,
                    registered_on=record.registered_on,
                    group_name=record.custom_questions[0]['value']
                )
        
        return summary
            