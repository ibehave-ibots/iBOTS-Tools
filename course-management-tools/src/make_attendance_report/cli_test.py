

from unittest.mock import Mock

from .core.attendance_workflows import AttendanceWorkflows


def test_attendance_report_is_displayed_when_given_a_session_id(inmemory_repo):
    # GIVEN: a session id
    session_id = 'some number'
    workflow = AttendanceWorkflows(inmemory_repo)
    presenter = Mock()
    
    # WHEN: asked for the attendance report
    workflow.make_attendance_report(session_id=session_id, presenter=presenter)
    
    # THEN: something is displayed
    presenter.show.assert_called()
    
    # THEN: names, emails, and attendance for each attendee is displayed
    args, kwargs = presenter.show.call_args
    for attendee in args[0]:
        assert hasattr(attendee, 'name')
        assert hasattr(attendee, 'email')
        assert hasattr(attendee, 'attendance')