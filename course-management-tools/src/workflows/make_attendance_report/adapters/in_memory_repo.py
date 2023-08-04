from datetime import datetime
from typing import Dict, List
from ..core.attendance_workflows import Attendee, AttendanceRepo, Session

# Implementation of AttendanceRepo for integration testing
# RESPONSIBLE fot the implementation of AttendanceRepo

class InMemoryAttendeeRepo(AttendanceRepo):
    def __init__(self, start_time: datetime, end_time: datetime, attendees: List[Attendee]):
        self.start_time = start_time
        self.end_time = end_time
        self.attendees = attendees

    def get_session_details(self,session_id: str)-> Session:
        return Session(
            session_id=session_id,
            start_time=self.start_time,
            end_time=self.end_time,
            attendees=self.attendees
        )
