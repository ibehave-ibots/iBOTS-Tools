from datetime import datetime

import pytest
from .core.attendance_workflows import AttendanceWorkflows
from .adapters.in_memory_repo import InMemoryAttendeeRepo
from .adapters.example_attendees import *
from .external.zoom_api import ZoomAttendanceApi, ZoomParticipantsResponseData, ZoomMeetingData
from .adapters.zoom_attendance_repo import ZoomAttendeeRepo
from unittest.mock import Mock

start_time = datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
end_time = datetime(2023, 7, 7, hour=1, minute=1, second=59, microsecond=0, tzinfo=None)




@pytest.fixture()
def inmemory_repo() -> InMemoryAttendeeRepo:
    attendees = [attendee1, attendee2, attendee3, attendee4, attendee5, attendee6]
    inmemory_repo = InMemoryAttendeeRepo(start_time=start_time,end_time=end_time,attendees=attendees)
    return inmemory_repo

@pytest.fixture()
def zoom_repo():
    meeting_data: ZoomMeetingData = {'start_time':start_time,
                                    'end_time':end_time}
    part_report: ZoomParticipantsResponseData = {
        'participants': [{'status': 'in_meeting', 'name': attendee.name, 'user_email': attendee.email,
                        'join_time': attendee.join_start, 'leave_time': attendee.join_end}
                        for attendee in [attendee1, attendee2, attendee3, attendee4, attendee5, attendee6]
                        ]
    }
    api = Mock(ZoomAttendanceApi)
    api.get_past_meeting_details.return_value = meeting_data
    api.get_zoom_participant_report.return_value = part_report
    zoom_repo = ZoomAttendeeRepo(zoom_api=api)
    return zoom_repo




####
def test_number_of_attendees(inmemory_repo):
    attendance_workflows = AttendanceWorkflows(inmemory_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id='session_123')
    assert attendance_report.total_attendees == 3


def test_zoom_number_of_attendees(zoom_repo):
    attendance_workflows = AttendanceWorkflows(zoom_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)
    assert attendance_report.total_attendees == 3



###
def test_number_of_candidates_who_got_attendance(inmemory_repo) -> None:
    attendance_workflows = AttendanceWorkflows(inmemory_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id='session_123')
    assert len(attendance_report.list_successful_attendees) == 2

def test_zoom_number_of_candidates_who_got_attendance(zoom_repo) -> None:
    attendance_workflows = AttendanceWorkflows(zoom_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)
    assert len(attendance_report.list_successful_attendees) == 2



####
def test_number_of_attendees_not_getting_attendance(inmemory_repo) -> None:
    attendance_workflows = AttendanceWorkflows(inmemory_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id='session_123')
    assert len(attendance_report.list_unsuccessful_attendees) == 1

def test_zoom_number_of_attendees_not_getting_attendance(zoom_repo):
    attendance_workflows = AttendanceWorkflows(zoom_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)
    assert len(attendance_report.list_unsuccessful_attendees) == 1




####
def test_duration_of_attendee_with_only_one_appearance(inmemory_repo):
    attendance_workflow = AttendanceWorkflows(inmemory_repo)
    attendance_report = attendance_workflow.make_attendance_report(session_id='session_xyz')
    assert attendance_report.report[0].total_duration == 3719.
    assert attendance_report.report[1].total_duration == 900.



####
def test_duration_not_added_multiple_devices():
    attendees = [attendee3, attendee4, attendee5, attendee6]

    repo = InMemoryAttendeeRepo(start_time=start_time,end_time=end_time,attendees=attendees)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.make_attendance_report(session_id='session_123')

    assert attendance_report.total_attendees == 1
    assert len(attendance_report.list_successful_attendees) == 1
    assert len(attendance_report.list_unsuccessful_attendees) == 0
    assert attendance_report.report[0].total_duration == 3300.


####
def test_zoom_same_participant_is_not_counted_more_than_once_if_they_leave_and_rejoin(zoom_repo):
    attendance_workflows = AttendanceWorkflows(zoom_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)    
    assert attendance_report.total_attendees == 3


def test_zoom_duration_not_added_multiple_devices(zoom_repo):
    attendance_workflows = AttendanceWorkflows(zoom_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)
    
    assert attendance_report.total_attendees == 3
    assert len(attendance_report.list_successful_attendees) == 2
    assert len(attendance_report.list_unsuccessful_attendees) == 1
    assert attendance_report.report[2].total_duration == 3300.
