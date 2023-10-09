from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List
from unittest.mock import Mock

from external.zoom_api import OAuthGetToken, get_attendees
from app import AttendanceRecord, AttendanceRepo

@dataclass(frozen=True)
class ZoomAttendanceRepo(AttendanceRepo):
    oauth_get_token: OAuthGetToken
    get_attendees: Callable = get_attendees
    
    def get_attendance_records(self, workshop_id: str) -> List[AttendanceRecord]:
        access_token = self.oauth_get_token.create_access_token()["access_token"]
        zoom_attendees = self.get_attendees(
                access_token=access_token, 
                meeting_id=workshop_id, 
            )
        attendance_records = []
        for zoom_attendee in zoom_attendees:
            attendance_record = AttendanceRecord(
                workshop_id=workshop_id,
                name=zoom_attendee.name,
                email=zoom_attendee.user_email,
                session=Mock(),
                arrived=datetime.strptime(zoom_attendee.join_time, "%Y-%m-%dT%H:%M:%S%z"),
                departed=datetime.strptime(zoom_attendee.leave_time, "%Y-%m-%dT%H:%M:%S%z"),
            )
            attendance_records.append(attendance_record)
        return attendance_records