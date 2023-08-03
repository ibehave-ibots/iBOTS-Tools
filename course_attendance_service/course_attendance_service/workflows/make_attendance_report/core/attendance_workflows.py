# AttendanceWorkflows class
# contains methods calling an abstract AttendeeRepo interface

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, NamedTuple
from collections import defaultdict


# entities
class Attendee(NamedTuple):
    name: str
    email: str
    join_start: datetime
    join_end: datetime

    @property
    def duration(self):
        return (self.join_end - self.join_start).total_seconds()
    
# unique email and all different instances of same attendee in a session
class AttendeeReport(NamedTuple):
    email: str
    attendees: List[Attendee]
    attendance: bool
    total_duration: float

# individual session of a workshop with a session id. List of all attendees (including duplicates) 
class Session(NamedTuple):
    session_id: str
    start_time: datetime
    end_time: datetime
    attendees: List[Attendee]

    @property
    def duration(self):
        return (self.end_time - self.start_time).total_seconds()
    
# attendance report of each unique attendee
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
            duration = self.calculate_duration(attendees=attendees)          
            attendance = duration >= 0.75 * max_duration             
            report.append(AttendeeReport(email=email,attendees=attendees,attendance=attendance,total_duration=duration))
        return report
    
    @staticmethod
    # for multiple instances of same attendee, calculate overall duration considering overlap time 
    def calculate_duration(attendees: List['Attendee']):
        overlapping_time_duration = 0.
        duration = sum([attendee.duration for attendee in attendees])
        for i, attendee_prev in enumerate(attendees):
            for attendee_next in attendees[i + 1:]:
                if attendee_next.join_start < attendee_prev.join_end:
                    overlap_start_time = max(attendee_prev.join_start, attendee_next.join_start)
                    overlap_end_time = min(attendee_prev.join_end, attendee_next.join_end)
                    overlapping_time_duration += max((overlap_end_time - overlap_start_time).total_seconds(), 0)
        duration = duration - overlapping_time_duration
        return duration