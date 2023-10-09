
from typing import NamedTuple, Optional, Literal
from .registrant_workflows import RegistrantWorkflows
from .list_workshops_workflow import ListWorkshopsWorkflow
from .attendance_workflow import AttendanceWorkflow

class App(NamedTuple):
    workshop_workflow: ListWorkshopsWorkflow
    registrant_workflows: RegistrantWorkflows
    attendance_workflow: AttendanceWorkflow
    
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
        to_status: Literal['approved','rejected', 'waitlisted'],
    ) -> None:
        self.registrant_workflows.update_registrant_status(
            workshop_id=workshop_id, 
            registration_id=registration_id,
            to_status=to_status,
        )
                      
    def create_attendance_summary(self, workshop_id: str, output_filename: str = None) -> None:
        self.attendance_workflow.create_attendance_summary(workshop_id=workshop_id, output_filename=output_filename)
