import zoom_integration
import processing


def get_attendance_report(token, meeting_id):
    report = zoom_integration.get_participant_report(
        access_token=token, meeting_id=meeting_id)
    result = processing.get_attendance(meeting_report=report)
    return result
