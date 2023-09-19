from typing import Literal, NamedTuple, Optional
from app.registrationrepo import RegistrationRepo
from .list_registrant_presenter import ListRegistrantPresenter, RegistrantSummary

class ListRegistrantsWorkflow(NamedTuple):
    registration_repo: RegistrationRepo
    presenter: ListRegistrantPresenter

    def list_registrants(self, workshop_id: str, status: Optional[Literal['approved', 'waitlisted', 'rejected']] = None) -> None:
        registration_records = self.registration_repo.get_registrations(workshop_id=workshop_id)
        summaries = []
        for record in registration_records:
            if status and record.status != status:
                continue
            
            summary = RegistrantSummary(
                name=record.name,
                email=record.email,
                status=record.status,
                registered_on=record.registered_on,
                group_name=record.custom_questions[0]['value']
            )
            summaries.append(summary)
        
        sorted_summaries = list(sorted(summaries, key=lambda s: s.registered_on))
        self.presenter.show(registrants=sorted_summaries)

