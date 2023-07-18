from functools import lru_cache
from course_attendance_service import zoom_integration
from course_attendance_service import api
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


def test_attendance_mark(token_data):
    uuid = "iJmk+imDQmugWQGtDIyRvg=="
    report = api.get_attendance_report(token=token_data, meeting_id=uuid)
    assert report.attendance_mark == [True, True, True]


def test_participant_details(token_data):
    uuid = "iJmk+imDQmugWQGtDIyRvg=="
    details = api.get_attendance_report(token=token_data, meeting_id=uuid)
    assert details.emails == [
        'sangeethanandakumar0694@gmail.com', 'delgrosso.nick@gmail.com', '']


def test_meeting_date(token_data):
    meeting_id = 87870712552
    meeting_details = api.get_meeting_details(
        token=token_data, meeting_id=meeting_id)
    assert meeting_details.date == '2023-07-03'


def test_meeting_title(token_data):
    meeting_id = 87870712552
    meeting_details = api.get_meeting_details(
        token=token_data, meeting_id=meeting_id)
    assert meeting_details.title == 'MouseFlow Refactoring'


def test_meeting_description(token_data):
    meeting_id = 87870712552
    meeting_details = api.get_meeting_details(
        token=token_data, meeting_id=meeting_id)
    assert meeting_details.description == ''


def test_meeting_id_over_period(token_data):
    meetings = api.list_meeting_ids(
        token_data, from_date='2023-07-18', to_date='2023-07-18')

    assert meetings.meeting_id == [82619942883]


def test_planned_start_and_end_times(token_data):
    meeting_id = 87870712552
    meeting_details = api.get_meeting_details(
        token=token_data, meeting_id=meeting_id)
    assert meeting_details.planned_start_time == '07:30:00'
    assert meeting_details.planned_end_time == '10:00:00'


def test_meeting_uuid_for_past_meeting(token_data):
    meeting_id = 87870712552
    meeting_details = api.get_meeting_details(
        token=token_data, meeting_id=meeting_id)
    assert meeting_details.session_ids == ['iJmk+imDQmugWQGtDIyRvg==']


def test_registrant_contact_details(token_data):
    meeting_id = 85887259531
    registrant_details = api.get_registrant_contact_details(
        token=token_data, meeting_id=meeting_id)
    assert registrant_details.names == [
        'Test Name 3', 'Test Name 2', 'Test Name 1']
    assert registrant_details.emails == [
        'an.sangeetha@gmail.com', 'sangeetha.nk94@gmail.com', 'astrophysics12@gmail.com']


def test_registrant_details(token_data):
    meeting_id = 84766483409
    registrant_details = api.get_registrant_details(
        token=token_data, meeting_id=meeting_id)
    assert registrant_details.names == [
        'TestName 5', 'TestName 4', 'TestName 3', 'TestName 2', 'TestName 1']
    assert registrant_details.emails == [
        'tn5@gmail.com', 'tn4@gmail.com', 'tn3@gmail.com', 'tn2@gmail.com', 'tn1@gmail.com']
    # assert registrant_details.affiliations == ['A', 'B', 'A', 'C', 'D']


def test_attendance_workshop(token_data):
    meeting_id = 87870712552
    report = api.get_workshop_attendance_report(
        token=token_data, meeting_id=meeting_id)
    assert report.workshop_attendees == ['Sangeetha Nandakumar',
                                         'Nicholas Del Grosso', 'Oliver Barnstedt']
    assert report.workshop_attendance == [True, True, True]
