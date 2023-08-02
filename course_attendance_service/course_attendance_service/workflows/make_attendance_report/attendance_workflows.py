# AttendanceWorkflows class
# contains methods calling an abstract AttendeeRepo interface

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, NamedTuple, Optional, Union
from collections import defaultdict
import numpy as np
import requests
from unittest.mock import Mock


# entities
class Attendee(NamedTuple):
    name: str
    email: str
    join_start: datetime
    join_end: datetime

    @property
    def duration(self):
        return (self.join_end - self.join_start).total_seconds()
        # return sum([(end-self.join_start[i]).total_seconds() for i,end in enumerate(self.join_end)])
    

class AttendeeReport(NamedTuple):
    email: str
    attendees: List[Attendee]
    attendance: bool

class Session(NamedTuple):
    session_id: str
    start_time: datetime
    end_time: datetime
    attendees: List[Attendee]

    @property
    def duration(self):
        return (self.end_time - self.start_time).total_seconds()
    
class SessionAttendanceReport(NamedTuple):
    report: List[AttendeeReport]

    @property
    def total_attendees(self) -> int:
        return len(self.report)
    
    @property
    def list_successful_attendees(self) -> List[Attendee]:
        return [attendee_report for attendee_report in self.report if attendee_report.attendance]
        
    @property
    def list_unsuccessful_attendees(self) -> List[Attendee]: 
        return [attendee_report for attendee_report in self.report if not attendee_report.attendance]


# INTERFACE (CONTRACT)
class AttendanceRepo(ABC):
    @abstractmethod
    def get_session_details(self, session_id: str) -> Session:
        ...

# OWNER
class AttendanceWorkflows(NamedTuple):
    attendee_repo: AttendanceRepo

    def make_attendance_report(self, session_id: str) -> SessionAttendanceReport:
        session = self.attendee_repo.get_session_details(session_id=session_id)
        all_attendees = session.attendees

        unique_attendees = defaultdict(list)
        for attendee in all_attendees:
            unique_attendees[attendee.email].append(attendee)

        report = self._get_report(session, unique_attendees)
                

        return SessionAttendanceReport(report=report)

    def _get_report(self, session, unique_attendees):
        report = []        
        max_duration = session.duration
        for email,attendees in unique_attendees.items():
            if len(attendees) == 1:            
                attendee = attendees[0]
                duration = attendee.duration
            else:
                duration = sum([attendee.duration for attendee in attendees])
            
            if duration >= 0.75 * max_duration:
                attendance=True
            else:
                attendance=False
                
            report.append(AttendeeReport(email=email,attendees=attendees,attendance=attendance))
        return report
    