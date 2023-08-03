from datetime import datetime
from .attendance_workflows import Attendee, AttendanceWorkflows, Session
from .in_memory_repo import InMemoryAttendeeRepo
from .example_attendees import *



def attendees_details():
    attendees = [attendee1, attendee2, attendee3, attendee4, attendee5, attendee6]
    return attendees


start_time=datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
end_time=datetime(2023, 7, 7, hour=1, minute=1, second=59, microsecond=0, tzinfo=None)

# InMemory testing
def test_number_of_attendees():
    attendees = attendees_details()

    repo = InMemoryAttendeeRepo(start_time=start_time,end_time=end_time,attendees=attendees)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.make_attendance_report(session_id='session_123')
    assert attendance_report.total_attendees == 3

def test_number_of_candidates_who_got_attendance() -> None:
    attendees = attendees_details()

    repo = InMemoryAttendeeRepo(start_time=start_time,end_time=end_time,attendees=attendees)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.make_attendance_report(session_id='session_123')

    assert len(attendance_report.list_successful_attendees) == 2


def test_number_of_attendees_not_getting_attendance() -> None:
    attendees = attendees_details()

    repo = InMemoryAttendeeRepo(start_time=start_time,end_time=end_time,attendees=attendees)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.make_attendance_report(session_id='session_123')

    assert len(attendance_report.list_unsuccessful_attendees) == 1

def test_duration_of_attendee_with_only_one_appearance():
    attendees = attendees_details()
    repo = InMemoryAttendeeRepo(start_time=start_time,end_time=end_time,attendees=attendees)
    attendance_workflow = AttendanceWorkflows(repo)
    attendance_report = attendance_workflow.make_attendance_report(session_id='session_xyz')

    attendance_report.report[0].total_duration == 3719.
    attendance_report.report[1].total_duration == 900.

def test_duration_not_added_multiple_devices():
    attendees = [attendee3, attendee4, attendee5, attendee6]

    repo = InMemoryAttendeeRepo(start_time=start_time,end_time=end_time,attendees=attendees)
    attendance_workflows = AttendanceWorkflows(repo)

    attendance_report = attendance_workflows.make_attendance_report(session_id='session_123')

    assert attendance_report.total_attendees == 1
    assert len(attendance_report.list_successful_attendees) == 1
    assert len(attendance_report.list_unsuccessful_attendees) == 0
    assert attendance_report.report[0].total_duration == 3300.
