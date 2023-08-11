from datetime import datetime

import pytest

from .adapters.in_memory_repo import InMemoryAttendeeRepo
from ..external.zoom_api import ZoomRestApi, ZoomParticipantsResponseData, ZoomMeetingData
from .adapters.zoom_attendance_repo import ZoomAttendeeRepo
from .core.entities import AttendeeInstance
from unittest.mock import Mock


start_time = datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
end_time = datetime(2023, 7, 7, hour=1, minute=1, second=59, microsecond=0, tzinfo=None)

attendee1 = AttendeeInstance(
    name='abc',
    email='abc@ibehave.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=1, minute=1, second=59, microsecond=0, tzinfo=None))

attendee2 = AttendeeInstance(
    name='def',
    email='def@gmail.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=0, minute=15, second=0, microsecond=0, tzinfo=None))

attendee3 = AttendeeInstance(
    name='ghi',
    email='ghi@xyz.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    join_end = datetime(2023, 7, 7, hour=0, minute=20, second=0, microsecond=0, tzinfo=None))

attendee4 = AttendeeInstance(
    name='ghi',
    email='ghi@xyz.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=25, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=1, minute=0, second=0, microsecond=0, tzinfo=None))

attendee5 = AttendeeInstance(
    name='jkl',
    email='ghi@xyz.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=0, minute=20, second=0, microsecond=0, tzinfo=None))

attendee6 = AttendeeInstance(
    name='jkl',
    email='ghi@xyz.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=25, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=0, minute=30, second=0, microsecond=0, tzinfo=None))


##############################


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
    api = Mock(ZoomRestApi)
    api.get_past_meeting_details.return_value = meeting_data
    api.get_zoom_participant_report.return_value = part_report
    zoom_repo = ZoomAttendeeRepo(zoom_api=api)
    return zoom_repo


@pytest.fixture(params=['inmemory_repo', 'zoom_repo'])
def attendance_repo(request,inmemory_repo,zoom_repo):
    if request.param == 'inmemory_repo':
        return inmemory_repo
    if (request.param) == 'zoom_repo':
        return zoom_repo    

