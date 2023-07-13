from unittest.mock import patch

from api import get_attendance_report

def test_users_changing_display_name_doesnt_affect_attendance_duration():
    # Given the ID for a zoom meeting with where Nick <dg@gmail.com> was present for 10 minutes, 
    # # then left, and NickDG <dg@gmail.com> was present for 20 minutes afterwards
    def part_report(access_token, meeting_id):
        return {'participants': [
            {'status': 'in_meeting', 'name': 'Nick', 'duration': 10, 'user_email': 'dg@gmail.com'}, 
            {'status': 'in_meeting', 'name': 'NickDG', 'duration': 20, 'user_email': 'dg@gmail.com'}, 
        ]}
    
    # When you ask for the attendance report
    with patch('api.zoom_integration.get_participant_report', part_report):
        report = get_attendance_report(token='1231414', meeting_id='1231')
    
    # Then you see that someone named both Nick and NickDG <dg@gmail.com> was present for 30 minutes
    assert report.names == [['Nick', 'NickDG']]
    
    # And the number of participants was 1
    assert report.n_participants == 1
    
    
    