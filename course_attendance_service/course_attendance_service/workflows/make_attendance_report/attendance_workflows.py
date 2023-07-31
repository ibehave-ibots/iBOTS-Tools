# AttendanceWorkflows class
# contains methods calling an abstract AttendeeRepo interface

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, NamedTuple, Optional, Union
from collections import defaultdict
import numpy as np
import requests
from unittest.mock import Mock

# change immutable class attributes 
@dataclass
class Attendee:
    name: str
    email: str
    attendance: Optional[bool] = None
    duration: Optional[float] = None

class AttendanceReport(NamedTuple):
    attendees: List[Attendee]

    @property
    def total_attendees(self) -> int:
        unique_attendees = {attendee.email for attendee in self.attendees}
        return len(unique_attendees)
    
    @property
    def list_successful_attendees(self) -> List[Attendee]:
        return [attendee for attendee in self.attendees if attendee.attendance]
        

    @property
    def list_unsuccessful_attendees(self) -> List[Attendee]: # better not to call them 'unsuccessful'
        return [attendee for attendee in self.attendees if not attendee.attendance]


# INTERFACE (CONTRACT)
class AttendanceRepo(ABC):
    @abstractmethod
    def list_all_attendees(self, workshop_id: str) -> List[Attendee]:
        ...

# OWNER
class AttendanceWorkflows(NamedTuple):
    attendee_repo: AttendanceRepo

    def list_all_attendees(self, workshop_id: str) -> AttendanceReport:
        attendees = self.attendee_repo.list_all_attendees(workshop_id=workshop_id)
        unique_attendees = defaultdict(list)
        for attendee in attendees:
            unique_attendees[attendee.email].append(attendee) 

        # refactor
        final_attendees = []
        for unique_attendee_group in unique_attendees.values():
            first_attendee = unique_attendee_group[0]
            total_duration = sum(attendee.duration for attendee in unique_attendee_group if attendee.duration is not None)
            total_duration = None if total_duration == 0. else total_duration 
            final_attendee = Attendee(
                name = first_attendee.name,
                email = first_attendee.email,
                attendance = first_attendee.attendance,
                duration = total_duration,
            )
            final_attendees.append(final_attendee)

        attendees = final_attendees
        non_none_durations = [attendee.duration for attendee in attendees if attendee.duration is not None]

        # refactor    
        if non_none_durations:
            max_duration = np.nanmax(non_none_durations)
            for attendee in attendees:
                if attendee.attendance is None and attendee.duration is not None:
                    if attendee.duration >= 0.75 * max_duration:
                        attendee.attendance = True
                    else:
                        attendee.attendance = False                      
        return AttendanceReport(attendees=attendees)
    