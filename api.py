import zoom_integration
import processing
import urllib.parse

# Might be refactored to utils module


def double_encoder(uuid):
    uuid_single_encode = urllib.parse.quote_plus(uuid)
    return (urllib.parse.quote_plus(uuid_single_encode))


def get_attendance_report(token, meeting_id):
    if isinstance(meeting_id, str):
        meeting_id = double_encoder(meeting_id)

    report = zoom_integration.get_participant_report(
        access_token=token, meeting_id=meeting_id)
    result = processing.get_attendance(meeting_report=report)

    # [{'name': 'Nick', 'duration_min': 500}, {'name': 'Nick', 'duration_min': 500}]
    num_attendees = len(result['name'])
    attendance_report = [{'name': result['name'][i], 'duration_min':result['duration_min'][i]}
                         for i in range(num_attendees)]

    return attendance_report
