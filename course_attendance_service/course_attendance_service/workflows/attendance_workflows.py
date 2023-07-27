# AttendanceWorkflows class
# contains methods calling an abstract AttendeeRepo interface
# which has ZoomAttendeeRepo implementation


from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple, Union
import numpy as np
import requests
from unittest.mock import patch



# InMemory testing
def test_length_attendees():
    attendees = [Attendee(name='abc',email='abc@ibehave.com',certificate=True),Attendee(name='def',email='def@gmail.com',certificate=True),Attendee(name='ghi',email='ghi@xyz.com',certificate=False)]
    workshop = {'wid':attendees}

    repo = InMemoryAttandeeRepo(workshop=workshop)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id='wid')
    assert attendance_report.total_attendees == len(attendees)

def test_number_of_certificates_awarded_is_right() -> None:
    attendees = [Attendee(name='abc',email='abc@ibehave.com',certificate=True),Attendee(name='def',email='def@gmail.com',certificate=True),Attendee(name='ghi',email='ghi@xyz.com',certificate=False)]
    workshop = {'wid':attendees}
    repo = InMemoryAttandeeRepo(workshop=workshop)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id='wid')

    assert len(attendance_report.list_successful_attendees) == 2


def test_number_of_attendees_not_completed_course() -> None:
    attendees = [Attendee(name='abc',email='abc@ibehave.com',certificate=True),Attendee(name='def',email='def@gmail.com',certificate=True),Attendee(name='ghi',email='ghi@xyz.com',certificate=False)]
    workshop = {'wid':attendees}
    repo = InMemoryAttandeeRepo(workshop=workshop)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id='wid')

    assert len(attendance_report.list_unsuccessful_attendees) == 1

# ZoomRepo testing
# def test_length_attendees():
#     attendees = [Attendee(name='abc',email='abc@ibehave.com',certificate=True),Attendee(name='def',email='def@gmail.com',certificate=True),Attendee(name='ghi',email='ghi@xyz.com',certificate=False)]
#     part_report = {'participants': [
#             {'status': 'in_meeting', 'name': 'abc',
#                 'duration': 120, 'user_email': 'abc@ibehave.com'},
#             {'status': 'in_meeting', 'name': 'def',
#                 'duration': 100, 'user_email': 'def@gmail.com'},
#             {'status': 'in_meeting', 'name': 'ghi',
#                 'duration': 10, 'user_email': 'ghi@gmail.com'}                
#         ]}

#     repo = ZoomAttendeeRepo()
#     attendance_workflows = AttendanceWorkflows(repo)

#     with patch('ZoomAttendeeRepo.get_zoom_participant_report', part_report):
#         attendance_report = attendance_workflows.list_all_attendees(token='1231414', meeting_id='1231')

#     assert attendance_report.total_attendees == len(attendees)


##################
class Attendee(NamedTuple):
    name: str
    email: str
    certificate: bool

class AttendanceReport(NamedTuple):
    attendees: List[Attendee]

    @property
    def total_attendees(self) -> int:
        return len(self.attendees)
    
    @property
    def list_successful_attendees(self) -> List[Attendee]:
        return [attendee for attendee in self.attendees if attendee.certificate]
        

    @property
    def list_unsuccessful_attendees(self) -> List[Attendee]:
        return [attendee for attendee in self.attendees if not attendee.certificate]


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
class InMemoryAttandeeRepo(AttendanceRepo):
    def __init__(self, workshop: Dict[str,List[Attendee]]) -> None:
        self.workshop = workshop

    def list_all_attendees(self,workshop_id:str) -> List[str]:
        return self.workshop[workshop_id]

# class ZoomAttendeeRepo(AttendanceRepo):

#     def get_zoom_participant_report(self, access_token:str, workshop_id: str):
#         url = f"https://api.zoom.us/v2/report/meetings/{workshop_id}/participants"
#         report = get_json_from_zoom_request(url=url, access_token=access_token)
#         return report


#     def list_all_attendees(self, access_token:str,workshop_id: str) -> List[Attendee]:
#         participants = self.get_zoom_participant_report(access_token=access_token,workshop_id=workshop_id)['participants']

#         names = []
#         durations = []
#         emails = []
        
#         max_duration = np.max([participant['duration']/60. for participant in participants])

#         attendees = []
#         for participant in participants:
#             attendee = Attendee()
#             if participant['status'] == 'in_meeting':
#                 attendee.name = participant['name']
#                 attendee.email = participant['user_email']
#                 if participant['duration']/60. >= 0.75*max_duration:
#                     attendee.certificate = True
#                 else:
#                     attendee.certificate = False
#             attendees.append(attendee)
#         return attendees


#         return output
    

# ######################
# def get_json_from_zoom_request(url: str, access_token: str, params: Dict = None) -> Union[List, Dict]:
#     header = {
#         'Authorization': f"Bearer {access_token}"
#     }

#     response = requests.get(url, headers=header, params=params)
#     response.raise_for_status()
#     return response.json()    
