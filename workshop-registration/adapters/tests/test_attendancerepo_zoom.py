from datetime import datetime
from unittest.mock import Mock
from external.zoom_api import ZoomAttendee, OAuthGetToken
from adapters import ZoomAttendanceRepo

def test_zoom_attendance_repo_returns_correct_attendance_records_for_a_given_workshop():
    get_attendees = lambda access_token, meeting_id: [
        ZoomAttendee(
            name="first_A last_A",
            user_email="a@a.com",
            session="1",
            join_time="2023-10-05T07:40:14Z",
            leave_time="2023-10-05T10:01:19Z",
        ),
        
        ZoomAttendee(
            name="first_B last_B",
            user_email="b@b.com",
            session="1",
            join_time="2023-10-05T07:45:14Z",
            leave_time="2023-10-05T09:59:19Z",
        ),
    ]
    
    oauth = Mock(OAuthGetToken)
    oauth.create_access_token.return_value = {'access_token': "OPEN-SESAME"}
    repo = ZoomAttendanceRepo(oauth_get_token=oauth, get_attendees=get_attendees)
    workshop_id = "12345"
    attendance_records = repo.get_attendance_records(workshop_id=workshop_id)
    
    assert len(attendance_records) == 2
    assert attendance_records[0].workshop_id == workshop_id
    assert attendance_records[0].name == "first_A last_A"
    assert attendance_records[0].email == "a@a.com"
    assert attendance_records[0].session
    assert attendance_records[0].arrived == datetime.strptime("2023-10-05T07:40:14Z", "%Y-%m-%dT%H:%M:%S%z")
    assert attendance_records[0].departed == datetime.strptime("2023-10-05T10:01:19Z", "%Y-%m-%dT%H:%M:%S%z")