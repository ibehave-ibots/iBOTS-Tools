
from typing import NamedTuple
from .list_registrants_app import ListRegistrantsWorkflow
from .list_workshops_app import ListWorkshopsWorkflow


class App(NamedTuple):
    workshop_workflow: ListWorkshopsWorkflow
    registrants_workflow: ListRegistrantsWorkflow

    def list_upcoming_workshops(self) -> None:
        self.workshop_workflow.check_upcoming_workshops()

    def list_registrants(self, workshop_id: str) -> None:
        self.registrants_workflow.list_registrants(workshop_id=workshop_id)

