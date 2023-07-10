import zoom_integration
import api

# GIVEN, WHEN, THEN


def test_program_gets_attendance_given_meeting_id():
    # GIVEN the account credentials and meeting id
    token_data = zoom_integration.create_access_token()['access_token']
    meeting_id = 87870712552

    # WHEN we ask for the attendance report
    report = api.get_attendance_report(token=token_data, meeting_id=meeting_id)

    # THEN the result should match our expected output
    expected = {'name': ['Sangeetha Nandakumar', 'Nicholas Del Grosso',
                         'Oliver Barnstedt'], 'duration_min': [191.0, 182.0, 156.0]}
    observed = report
    assert expected == observed
