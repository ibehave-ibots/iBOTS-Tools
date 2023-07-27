# AttendanceWorkflows class
# contains methods calling an abstract AttendeeRepo interface
# which has ZoomAttendeeRepo implementation


from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple, Union
import numpy as np
import requests
from unittest.mock import Mock


# ZoomRepo testing
def test_zoom_length_attendees():
    attendees = [Attendee(name='abc',email='abc@ibehave.com',attendance=True),Attendee(name='def',email='def@gmail.com',attendance=True),Attendee(name='ghi',email='ghi@xyz.com',attendance=False)]
    part_report = {'participants': [
            {'status': 'in_meeting', 'name': 'abc',
                'duration': 120, 'user_email': 'abc@ibehave.com'},
            {'status': 'in_meeting', 'name': 'def',
                'duration': 100, 'user_email': 'def@gmail.com'},
            {'status': 'in_meeting', 'name': 'ghi',
                'duration': 10, 'user_email': 'ghi@gmail.com'}                
        ]}

    api = Mock(ZoomAttendanceApi)
    api.get_zoom_participant_report.return_value = part_report
    repo = ZoomAttendeeRepo(zoom_api=api)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id=1234)

    assert attendance_report.total_attendees == len(attendees)

def test_zoom_number_of_candidates_who_got_attendance() -> None:
    attendees = [Attendee(name='abc',email='abc@ibehave.com',attendance=True),Attendee(name='def',email='def@gmail.com',attendance=True),Attendee(name='ghi',email='ghi@xyz.com',attendance=False)]
    part_report = {'participants': [
            {'status': 'in_meeting', 'name': 'abc',
                'duration': 120, 'user_email': 'abc@ibehave.com'},
            {'status': 'in_meeting', 'name': 'def',
                'duration': 100, 'user_email': 'def@gmail.com'},
            {'status': 'in_meeting', 'name': 'ghi',
                'duration': 10, 'user_email': 'ghi@gmail.com'}                
        ]}

    api = Mock(ZoomAttendanceApi)
    api.get_zoom_participant_report.return_value = part_report
    repo = ZoomAttendeeRepo(zoom_api=api)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id=1234)
    assert len(attendance_report.list_successful_attendees) == 2


def test_zoom_number_of_attendees_not_completed_course() -> None:
    attendees = [Attendee(name='abc',email='abc@ibehave.com',attendance=True),Attendee(name='def',email='def@gmail.com',attendance=True),Attendee(name='ghi',email='ghi@xyz.com',attendance=False)]
    part_report = {'participants': [
            {'status': 'in_meeting', 'name': 'abc',
                'duration': 120, 'user_email': 'abc@ibehave.com'},
            {'status': 'in_meeting', 'name': 'def',
                'duration': 100, 'user_email': 'def@gmail.com'},
            {'status': 'in_meeting', 'name': 'ghi',
                'duration': 10, 'user_email': 'ghi@gmail.com'}                
        ]}

    api = Mock(ZoomAttendanceApi)
    api.get_zoom_participant_report.return_value = part_report
    repo = ZoomAttendeeRepo(zoom_api=api)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id=1234)
    assert len(attendance_report.list_unsuccessful_attendees) == 1


##################
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


# interface
class AttendanceRepo(ABC):
    @abstractmethod
    def list_all_attendees(self, workshop_id: str) -> List[Attendee]:
        ...

# handler
class AttendanceWorkflows(NamedTuple):
    attendee_repo: AttendanceRepo

    def list_all_attendees(self, workshop_id: str) -> List[Attendee]:
        attendees = self.attendee_repo.list_all_attendees(workshop_id=workshop_id)
        return AttendanceReport(attendees=attendees)
    

# Implementations
class ZoomAttendanceApi:
    @staticmethod
    def get_zoom_participant_report(access_token:str, meeting_id: str, params:Dict = None):
        url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
        header = {
            'Authorization': f"Bearer {access_token}"
        }

        response = requests.get(url, headers=header, params=params)
        response.raise_for_status()
        return response.json()    

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

