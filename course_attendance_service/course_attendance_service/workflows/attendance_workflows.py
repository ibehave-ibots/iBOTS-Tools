# AttendanceWorkflows class
# contains methods calling an abstract AttendeeRepo interface
# which has ZoomAttendeeRepo implementation


from abc import ABC, abstractmethod
from typing import Dict, List, NamedTuple


def test_length_attendees():
    attendees = [Attendee(name='abc',email='abc@ibehave.com',certificate=True),Attendee(name='def',email='def@gmail.com',certificate=True),Attendee(name='ghi',email='ghi@xyz.com',certificate=False)]
    workshop = {'wid':attendees}

    repo = InMemoryAttandanceRepo(workshop=workshop)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id='wid')
    assert attendance_report.total_attendees == len(attendees)

def test_number_of_certificates_awarded_is_right() -> None:
    attendees = [Attendee(name='abc',email='abc@ibehave.com',certificate=True),Attendee(name='def',email='def@gmail.com',certificate=True),Attendee(name='ghi',email='ghi@xyz.com',certificate=False)]
    workshop = {'wid':attendees}
    repo = InMemoryAttandanceRepo(workshop=workshop)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id='wid')

    assert len(attendance_report.list_successful_attendees) == 2


def test_number_of_attendees_not_completed_course() -> None:
    attendees = [Attendee(name='abc',email='abc@ibehave.com',certificate=True),Attendee(name='def',email='def@gmail.com',certificate=True),Attendee(name='ghi',email='ghi@xyz.com',certificate=False)]
    workshop = {'wid':attendees}
    repo = InMemoryAttandanceRepo(workshop=workshop)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id='wid')

    assert len(attendance_report.list_unsuccessful_attendees) == 1


##################
class Attendee(NamedTuple):
    name: str
    email: str
    certificate: bool

class AttendanceReport(NamedTuple):
    attendees: List[Attendee]

    @property
    def total_attendees(self) -> int:
        return len(self.attendees)
    
    @property
    def list_successful_attendees(self) -> List[Attendee]:
        return [attendee for attendee in self.attendees if attendee.certificate]
        

    @property
    def list_unsuccessful_attendees(self) -> List[Attendee]:
        return [attendee for attendee in self.attendees if not attendee.certificate]


# interface
class AttendanceRepo(ABC):
    @abstractmethod
    def list_all_attendees(self, workshop_id: str) -> List[Attendee]:
        ...

# handler
class AttendanceWorkflows(NamedTuple):
    attendee_repo: AttendanceRepo

    # Step 1: get list of attendees from workshop id
    def list_all_attendees(self, workshop_id: str) -> List[Attendee]:
        attendees = self.attendee_repo.list_all_attendees(workshop_id=workshop_id)
        return AttendanceReport(attendees=attendees)
    
    # Step 2: if attendee has attended at least 75% of the 

        ...
    

# Implementations
class InMemoryAttandanceRepo(AttendanceRepo):
    def __init__(self, workshop: Dict[str,List[Attendee]]) -> None:
        self.workshop = workshop

    def list_all_attendees(self,workshop_id:str) -> List[str]:
        return self.workshop[workshop_id]
