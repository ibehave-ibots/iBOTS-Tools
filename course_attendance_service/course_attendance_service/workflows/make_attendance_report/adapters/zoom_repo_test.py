from datetime import datetime
from unittest.mock import Mock

from ..external.zoom_api import ZoomAttendanceApi, ZoomParticipantsResponseData, ZoomMeetingData

from .example_attendees import *

from .zoom_attendance_repo import ZoomAttendeeRepo
from ..core.attendance_workflows import AttendanceWorkflows



# Unit testing Zoom 
# Patching out API calls to reduce test 

# example case
start_time = datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
end_time = datetime(2023, 7, 7, hour=1, minute=1, second=59, microsecond=0, tzinfo=None)

meeting_data: ZoomMeetingData = {'start_time':start_time,
                                'end_time':end_time}

part_report: ZoomParticipantsResponseData = {
    'participants': [{'status': 'in_meeting', 'name': attendee.name, 'user_email': attendee.email,
                      'join_time': attendee.join_start, 'leave_time': attendee.join_end}
                     for attendee in [attendee1, attendee2, attendee3, attendee4, attendee5, attendee6]
                    ]
}


def test_zoom_number_of_attendees():
    attendance_workflows = prep_zoom_repo()

    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)

    assert attendance_report.total_attendees == 3

def test_zoom_number_of_candidates_who_got_attendance() -> None:
    attendance_workflows = prep_zoom_repo()
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)
    assert len(attendance_report.list_successful_attendees) == 2


def test_zoom_number_of_attendees_not_getting_attendance():
    attendance_workflows = prep_zoom_repo()
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)
    assert len(attendance_report.list_unsuccessful_attendees) == 1


def test_zoom_same_participant_is_not_counted_more_than_once_if_they_leave_and_rejoin():
    attendance_workflows = prep_zoom_repo()
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)    
    assert attendance_report.total_attendees == 3

def test_zoom_duration_not_added_multiple_devices():
    attendance_workflows = prep_zoom_repo()
    attendance_report = attendance_workflows.make_attendance_report(session_id=1234)

    assert attendance_report.total_attendees == 3
    assert len(attendance_report.list_successful_attendees) == 2
    assert len(attendance_report.list_unsuccessful_attendees) == 1
    assert attendance_report.report[2].total_duration == 3300.

#######################################
def prep_zoom_repo():
    api = Mock(ZoomAttendanceApi)
    api.get_past_meeting_details.return_value = meeting_data
    api.get_zoom_participant_report.return_value = part_report
    repo = ZoomAttendeeRepo(zoom_api=api)
    attendance_workflows = AttendanceWorkflows(repo)
    return attendance_workflows

