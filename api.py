from typing import List, NamedTuple
from processing import double_encoder
import zoom_integration
import processing


class AttendanceReport(NamedTuple):
    names: List[str]
    durations_min: List[float]

    @property
    def n_participants(self) -> int:
        return len(self.names)

    @property
    def attendance_mark(self) -> List:
        attendance_mark = []
        max_duration = max(self.durations_min)
        for duration in self.durations_min:
            if duration/max_duration >= 0.8:
                attendance_mark.append(True)
            else:
                attendance_mark.append(False)
        return attendance_mark


class ParticipantsDetails(NamedTuple):
    names: List[str]
    emails: List[str]


def get_attendance_report(token, meeting_id) -> AttendanceReport:
    if isinstance(meeting_id, str):
        meeting_id = double_encoder(meeting_id)

    report = zoom_integration.get_participant_report(
        access_token=token, meeting_id=meeting_id)
    result = processing.get_attendance(meeting_report=report)
    return AttendanceReport(names=result['name'],
                            durations_min=result['duration_min'])


def get_participant_details(token, meeting_id) -> ParticipantsDetails:
    if isinstance(meeting_id, str):
        meeting_id = double_encoder(meeting_id)

    report = zoom_integration.get_participant_report(
        access_token=token, meeting_id=meeting_id)

    result = processing.get_participant_details(report)

    return ParticipantsDetails(names=result['name'], emails=result['email'])
