from abc import ABC, abstractmethod
from typing import NamedTuple, List, Any, Dict
from pytest import mark

#### TESTS

def test_attendance_report_gets_correct_number_of_attendees():
    # GIVEN
    workshops = {
        'abc': [Attendee(), Attendee()],
        'xyz': [Attendee(), Attendee(), Attendee()],
    }
    repo = InMemoryAttendeeRepo(workshops=workshops)
    attendance_workflows = AttendanceWorkflows(attendee_repo=repo)

    # WHEN
    workshop_id = 'abc'
    attendance_report = attendance_workflows.get_attendance_report(workshop_id=workshop_id)
    assert attendance_report.total_attendees == 2

    workshop_id = 'xyz'
    attendance_report = attendance_workflows.get_attendance_report(workshop_id=workshop_id)
    assert attendance_report.total_attendees == 3




### ENTITIES
class Attendee(NamedTuple):
    ...


### WORKFLOWS
class AttendanceReport(NamedTuple):
    attendees: List[Attendee]

    @property
    def total_attendees(self):
        return len(self.attendees)


class AttendeeRepo(ABC):
    @abstractmethod
    def get_list_of_attendees(self, workshop_id) -> List[Attendee]: ...

class AttendanceWorkflows(NamedTuple):
    attendee_repo: AttendeeRepo

    def get_attendance_report(self, workshop_id):
        attendees = self.attendee_repo.get_list_of_attendees(workshop_id)
        return AttendanceReport(attendees=attendees)



## REPOS

class InMemoryAttendeeRepo(AttendeeRepo):
    def __init__(self, workshops: Dict[str, List[Attendee]]):
        self.workshops = workshops

    def get_list_of_attendees(self, workshop_id) -> List[Attendee]:
        return self.workshops[workshop_id]

