from functools import lru_cache
import zoom_integration
import api
from pytest import fixture


# GIVEN, WHEN, THEN

@fixture(scope='session')
def token_data():
    token_data = zoom_integration.create_access_token()['access_token']
    return token_data


def test_program_gets_attendance_given_meeting_id(token_data):
    # GIVEN the account credentials and meeting id
    meeting_id = 87870712552
    report = api.get_attendance_report(token=token_data, meeting_id=meeting_id)
    assert report.names == ['Sangeetha Nandakumar',
                            'Nicholas Del Grosso', 'Oliver Barnstedt']
    assert report.durations_min == [191.0, 182.0, 156.0]


def test_number_of_participants_is_three(token_data):
    meeting_id = 87870712552
    report = api.get_attendance_report(token=token_data, meeting_id=meeting_id)
    assert report.n_participants == 3


def test_uuid_working_instead_of_meetingid(token_data):
    uuid = "iJmk+imDQmugWQGtDIyRvg=="
    report = api.get_attendance_report(token=token_data, meeting_id=uuid)
    assert report.names == ['Sangeetha Nandakumar',
                            'Nicholas Del Grosso', 'Oliver Barnstedt']
    assert report.durations_min == [191.0, 182.0, 156.0]


def test_number_of_participants_is_three_from_uuid(token_data):
    uuid = "iJmk+imDQmugWQGtDIyRvg=="
    report = api.get_attendance_report(token=token_data, meeting_id=uuid)
    assert report.n_participants == 3
