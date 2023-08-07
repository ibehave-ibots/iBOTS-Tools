from .core.attendance_workflows import AttendanceWorkflows



def test_number_of_attendees(attendance_repo):
    attendance_workflows = AttendanceWorkflows(attendance_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)
    assert attendance_report.total_attendees == 3


def test_number_of_candidates_who_got_attendance(attendance_repo) -> None:
    attendance_workflows = AttendanceWorkflows(attendance_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)
    assert len(attendance_report.list_successful_attendees) == 2


def test_number_of_attendees_not_getting_attendance(attendance_repo) -> None:
    attendance_workflows = AttendanceWorkflows(attendance_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)
    assert len(attendance_report.list_unsuccessful_attendees) == 1


def test_duration_of_attendee_with_only_one_appearance(attendance_repo):
    attendance_workflow = AttendanceWorkflows(attendance_repo)
    attendance_report = attendance_workflow.make_attendance_report(session_id=1234)
    assert attendance_report.report[0].total_duration == 3719.
    assert attendance_report.report[1].total_duration == 900.



def test_duration_not_added_multiple_devices(attendance_repo):
    attendance_workflows = AttendanceWorkflows(attendance_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)

    assert attendance_report.total_attendees == 3
    assert len(attendance_report.list_successful_attendees) == 2
    assert len(attendance_report.list_unsuccessful_attendees) == 1
    assert attendance_report.report[2].total_duration == 3300.


def test_zoom_same_participant_is_not_counted_more_than_once_if_they_leave_and_rejoin(attendance_repo):
    attendance_workflows = AttendanceWorkflows(attendance_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)    
    assert attendance_report.total_attendees == 3


def test_zoom_duration_not_added_multiple_devices(attendance_repo):
    attendance_workflows = AttendanceWorkflows(attendance_repo)
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)    
    assert attendance_report.total_attendees == 3
    assert len(attendance_report.list_successful_attendees) == 2
    assert len(attendance_report.list_unsuccessful_attendees) == 1
    assert attendance_report.report[2].total_duration == 3300.
