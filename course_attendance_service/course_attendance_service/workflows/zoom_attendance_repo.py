from typing import List

import numpy as np

from .attendance_workflows import Attendee
from .zoom_attendance_api import ZoomAttendanceApi
from .attendance_workflows import AttendanceRepo

# Implementation of AttendanceRepo
# RESPONSIBLE for AttendanceRepo contract
# For Zoom attendance
class ZoomAttendeeRepo(AttendanceRepo):
    def __init__(self, zoom_api: ZoomAttendanceApi) -> None:
        self.api = zoom_api
        self.access_token = 'ACCESS TOKEN'

    def list_all_attendees(self,workshop_id:str) -> List[str]:
        report = self.api.get_zoom_participant_report(access_token=self.access_token,meeting_id=workshop_id)
        participants = report['participants']
        attendees = []
        max_duration = np.nanmax([participant['duration'] for participant in participants if participant['status'] == 'in_meeting'])
        attendance = False
        for participant in participants:
            if participant['status'] == 'in_meeting':
                if participant['duration'] >= 0.75*max_duration:
                    attendance = True
                else:
                    attendance = False
            attendees.append(Attendee(name=participant['name'],email=participant['user_email'],attendance=attendance))
        return attendees

