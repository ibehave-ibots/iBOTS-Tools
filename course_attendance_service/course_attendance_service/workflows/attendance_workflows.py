# AttendanceWorkflows class
# contains methods calling an abstract AttendeeRepo interface
# which has ZoomAttendeeRepo implementation


from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple, Union
import numpy as np
import requests
from unittest.mock import Mock

class Attendee:
    def __init__(self, name:str, email:str, attendance: bool = None, duration: float = None):
        self.name = name
        self.email = email
        self.attendance = attendance
        self.duration = duration

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
        non_none_durations = [attendee.duration for attendee in attendees if attendee.duration is not None]
        
        if non_none_durations:
            max_duration = np.nanmax(non_none_durations)
            for attendee in attendees:
                if attendee.attendance is None and attendee.duration is not None:
                    if attendee.duration >= 0.75 * max_duration:
                        attendee.attendance = True
                    else:
                        attendee.attendance = False                      
        return AttendanceReport(attendees=attendees)
    