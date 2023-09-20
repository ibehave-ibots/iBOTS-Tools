
from typing import NamedTuple, Optional
from typing_extensions import Literal
from .list_registrants_workflow import ListRegistrantsWorkflow
from .list_workshops_workflow import ListWorkshopsWorkflow


class App(NamedTuple):
    workshop_workflow: ListWorkshopsWorkflow
    registrants_workflow: ListRegistrantsWorkflow

    def list_upcoming_workshops(self) -> None:
        self.workshop_workflow.check_upcoming_workshops()

    def list_registrants(self, workshop_id: str, status: Optional[Literal['approved', 'waitlisted', 'rejected']] = None) -> None:
        
        if status and status not in ['approved', 'waitlisted', 'rejected']:
            raise ValueError("given status invalid")
        self.registrants_workflow.list_registrants(workshop_id=workshop_id, status = status)

