# AttendanceWorkflows class
# contains methods calling an abstract AttendeeRepo interface
# which has ZoomAttendeeRepo implementation


from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple, Union
import numpy as np
import requests
from unittest.mock import Mock

class Attendee(NamedTuple):
    name: str
    email: str
    attendance: bool

class AttendanceReport(NamedTuple):
    attendees: List[Attendee]

    @property
    def total_attendees(self) -> int:
        return len(self.attendees)
    
    @property
    def list_successful_attendees(self) -> List[Attendee]:
        return [attendee for attendee in self.attendees if attendee.attendance]
        

    @property
    def list_unsuccessful_attendees(self) -> List[Attendee]:
        return [attendee for attendee in self.attendees if not attendee.attendance]


# INTERFACE (CONTRACT)
class AttendanceRepo(ABC):
    @abstractmethod
    def list_all_attendees(self, workshop_id: str) -> List[Attendee]:
        ...

# OWNER
class AttendanceWorkflows(NamedTuple):
    attendee_repo: AttendanceRepo

    def list_all_attendees(self, workshop_id: str) -> List[Attendee]:
        attendees = self.attendee_repo.list_all_attendees(workshop_id=workshop_id)
        return AttendanceReport(attendees=attendees)
    