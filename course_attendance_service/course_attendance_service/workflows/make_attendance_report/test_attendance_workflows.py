from unittest.mock import Mock

from .zoom_attendance_api import ZoomAttendanceApi, ZoomParticipantsResponseData

from .zoom_attendance_repo import ZoomAttendeeRepo
from .attendance_workflows import Attendee, AttendanceWorkflows
from .in_memory_repo import InMemoryAttandeeRepo

# InMemory testing
def test_length_attendees():
    attendees = [Attendee(name='abc',email='abc@ibehave.com',attendance=True),Attendee(name='def',email='def@gmail.com',attendance=True),Attendee(name='ghi',email='ghi@xyz.com',attendance=False)]
    workshop = {'wid':attendees}

    repo = InMemoryAttandeeRepo(workshop=workshop)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id='wid')
    assert attendance_report.total_attendees == len(attendees)

def test_number_of_candidates_who_got_attendance() -> None:
    attendees = [
        Attendee(name='abc',email='abc@ibehave.com',attendance=True),
        Attendee(name='def',email='def@gmail.com',attendance=True),
        Attendee(name='ghi',email='ghi@xyz.com',attendance=False)]
    workshop = {'wid':attendees}
    repo = InMemoryAttandeeRepo(workshop=workshop)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id='wid')

    assert len(attendance_report.list_successful_attendees) == 2


def test_number_of_attendees_not_getting_attendance() -> None:
    attendees = [Attendee(name='abc',email='abc@ibehave.com',attendance=True),Attendee(name='def',email='def@gmail.com',attendance=True),Attendee(name='ghi',email='ghi@xyz.com',attendance=False)]
    workshop = {'wid':attendees}
    repo = InMemoryAttandeeRepo(workshop=workshop)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.list_all_attendees(workshop_id='wid')

    assert len(attendance_report.list_unsuccessful_attendees) == 1

# Unit testing Zoom 
# Patching out API calls to reduce test time
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


def test_zoom_number_of_attendees_not_getting_attendance():
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


def test_same_participant_is_not_counted_more_than_once_if_they_leave_and_rejoin():
    part_report: ZoomParticipantsResponseData = {'participants': [
        {'status': 'in_meeting', 'name': 'Mo',       'user_email': 'mo@mo.com', 'duration': 10},
        {'status': 'in_meeting', 'name': 'Mohammad', 'user_email': 'mo@mo.com', 'duration': 20},
    ]}
    api = Mock(ZoomAttendanceApi)
    api.get_zoom_participant_report.return_value = part_report
    repo = ZoomAttendeeRepo(zoom_api=api)
    attendance_workflows = AttendanceWorkflows(repo)
    attendance_report = attendance_workflows.list_all_attendees(workshop_id=1234)
    
    assert attendance_report.total_attendees == 1
    assert len(attendance_report.attendees) == 1 

    