from collections import defaultdict
from dataclasses import dataclass
import datetime
from typing import Any
from behave import given, when, then


class Repo:
    def __init__(self, sessions: dict[str, dict[str, Any]]) -> None:
        self.sessions = sessions

    def get_session(self, session_id: str) -> dict[str, Any]:
        return self.sessions[session_id]


@dataclass(frozen=True)
class AttendanceWorkflow:
    repo: Repo

    def get_attendance_report_for_session(self, session_id: str) -> dict[str, int]:
        session_record = self.repo.get_session(session_id)
        attendances = defaultdict(datetime.timedelta)
        for event in session_record['participant_events']:
            email = event['email']
            
            duration: datetime.timedelta = event['departure'] - event['arrival']
            attendances[email] += duration
        return attendances
        

        
@given(u'session ABCD, where Nick at dg@email.com arrived at 10h00 and left at 11h29')
def step_impl(context):
    sessions = {
        'ABCD': {
            'participant_events': [
                {'email': 'dg@email.com',
                'name': 'Nick',
                'arrival':   datetime.datetime(2023, 11, 10, 10, 00, 00),
                'departure': datetime.datetime(2023, 11, 10, 11, 29, 00)
                }
            ]
        }
    }
    repo = Repo(sessions=sessions)
    context.get_attendance_report_for_session = AttendanceWorkflow(repo=repo).get_attendance_report_for_session
    


@when(u'the teacher asks for the attendance report for session ABCD')
def step_impl(context):
    context.attendance = context.get_attendance_report_for_session('ABCD')

    

@then(u'they see that dg@email.com attended for 89 minutes')
def step_impl(context):
    assert context.attendance['dg@email.com'] == datetime.timedelta(minutes=89)
