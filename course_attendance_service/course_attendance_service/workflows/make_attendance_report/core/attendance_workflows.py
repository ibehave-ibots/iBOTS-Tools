# AttendanceWorkflows class
# contains methods calling an abstract AttendeeRepo interface

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, NamedTuple
from collections import defaultdict
from .entities import Attendee, AttendeeReport, Session
from .attendance_repo import AttendanceRepo


# entities

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