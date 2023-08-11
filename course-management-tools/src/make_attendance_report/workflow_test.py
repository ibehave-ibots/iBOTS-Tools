from unittest.mock import Mock
from .core.attendance_workflows import AttendanceWorkflows



def test_number_of_attendees(attendance_repo):
    attendance_workflow = AttendanceWorkflows(attendance_repo)
    presenter = Mock()
    attendance_workflow.make_attendance_report(session_id=1234, presenter=presenter)
    attendance_report = presenter.show.call_args[0][0]
    assert attendance_report.total_attendees == 3


def test_number_of_candidates_who_got_attendance(attendance_repo) -> None:
    attendance_workflow = AttendanceWorkflows(attendance_repo)
    presenter = Mock()
    attendance_workflow.make_attendance_report(session_id=1234, presenter=presenter)
    attendance_report = presenter.show.call_args[0][0]
    assert len(attendance_report.list_successful_attendees) == 2


def test_number_of_attendees_not_getting_attendance(attendance_repo) -> None:
    attendance_workflow = AttendanceWorkflows(attendance_repo)
    presenter = Mock()
    attendance_workflow.make_attendance_report(session_id=1234, presenter=presenter)
    attendance_report = presenter.show.call_args[0][0]
    assert len(attendance_report.list_unsuccessful_attendees) == 1


def test_duration_of_attendee_with_only_one_appearance(attendance_repo):
    attendance_workflow = AttendanceWorkflows(attendance_repo)
    presenter = Mock()
    attendance_workflow.make_attendance_report(session_id=1234, presenter=presenter)
    attendance_report = presenter.show.call_args[0][0]
    assert attendance_report.attendees[0].total_duration == 3719.
    assert attendance_report.attendees[1].total_duration == 900.
    assert attendance_report.attendees[2].total_duration == 3300.


def test_attendance_report_is_displayed_when_given_a_session_id(attendance_repo):
    attendance_workflow = AttendanceWorkflows(attendance_repo)
    presenter = Mock()
    attendance_workflow.make_attendance_report(session_id=1234, presenter=presenter)
    attendance_report = presenter.show.call_args[0][0]
    for attendee in attendance_report.attendees:
        assert hasattr(attendee, 'name')
        assert hasattr(attendee, 'email')
        assert hasattr(attendee, 'attendance')