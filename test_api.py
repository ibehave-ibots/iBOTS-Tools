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

    # WHEN we ask for the attendance report
    report = api.get_attendance_report(token=token_data, meeting_id=meeting_id)

    # THEN the result should match our expected output
    expected = [
        {'name': 'Sangeetha Nandakumar', 'duration_min': 191.0},
        {'name': 'Nicholas Del Grosso', 'duration_min': 182.0},
        {'name': 'Oliver Barnstedt', 'duration_min': 156.0},
    ]
    observed = report
    assert expected == observed


def test_number_of_participants_is_three(token_data):
    # GIVEN
    meeting_id = 87870712552

    # WHEN
    report = api.get_attendance_report(token=token_data, meeting_id=meeting_id)

    # THEN
    assert len(report) == 3
