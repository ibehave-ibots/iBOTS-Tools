import zoom_integration
import processing


def get_attendance_report(token, meeting_id):
    report = zoom_integration.get_participant_report(
        access_token=token, meeting_id=meeting_id)
    result = processing.get_attendance(meeting_report=report)

    # [{'name': 'Nick', 'duration_min': 500}, {'name': 'Nick', 'duration_min': 500}]
    num_attendees = len(result['name'])
    attendance_report = [{'name': result['name'][i], 'duration_min':result['duration_min'][i]}
                         for i in range(num_attendees)]
    print(attendance_report)

    return attendance_report
