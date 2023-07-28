from typing import Dict, List
from .attendance_workflows import Attendee, AttendanceRepo

# Implementation of AttendanceRepo for integration testing
# RESPONSIBLE fot the implementation of AttendanceRepo
class InMemoryAttandeeRepo(AttendanceRepo):
    def __init__(self, workshop: Dict[str,List[Attendee]]) -> None:
        self.workshop = workshop

    def list_all_attendees(self,workshop_id:str) -> List[str]:
        return self.workshop[workshop_id]
