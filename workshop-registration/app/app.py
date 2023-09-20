
from typing import NamedTuple, Optional
from typing_extensions import Literal
from .registrant_workflows import RegistrantWorkflows
from .list_workshops_workflow import ListWorkshopsWorkflow


class App(NamedTuple):
    workshop_workflow: ListWorkshopsWorkflow
    registrant_workflows: RegistrantWorkflows

    def list_upcoming_workshops(self) -> None:
        self.workshop_workflow.check_upcoming_workshops()

    def list_registrants(self, workshop_id: str, status: Optional[Literal['approved', 'waitlisted', 'rejected']] = None) -> None:
        
        if status and status not in ['approved', 'waitlisted', 'rejected']:
            raise ValueError("given status invalid")
        self.registrant_workflows.list_registrants(workshop_id=workshop_id, status = status)

    def update_registration_status(
        self, 
        workshop_id: str, 
        registration_id: str,
        to_status: Literal['approved','rejected'],
    ) -> None:
        
        self.registrant_workflows.update_registrant_status(
            workshop_id=workshop_id, 
            registration_id=registration_id,
            to_status=to_status,
        )
                                   

