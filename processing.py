import urllib.parse
import numpy as np


def get_attendance(meeting_report):
    """
    Retrieves the attendance details from a Zoom meeting report.

    Args:
        meeting_report (dict): Zoom meeting report obtained from `zoom_integration.get_participant_report()`.

    Returns:
        dict: A dictionary containing the names and durations of participants who were in the meeting.

    Raises:
        TypeError: If the meeting_report parameter is not a dictionary.
        KeyError: If the 'participants' key is missing in the meeting_report dictionary.

    Example:
        meeting_report = {
            'participants': [
                {
                    'name': 'John Doe',
                    'status': 'in_meeting',
                    'duration': 1800
                },
                {
                    'name': 'Jane Smith',
                    'status': 'in_meeting',
                    'duration': 2400
                },
                {
                    'name': 'Alice Johnson',
                    'status': 'not_in_meeting',
                    'duration': 0
                }
            ]
        }
        attendance = get_attendance(meeting_report)
        print(attendance)

    """
    if not isinstance(meeting_report, dict):
        raise TypeError("The meeting_report parameter must be a dictionary.")

    if 'participants' not in meeting_report:
        raise KeyError(
            "The meeting_report dictionary must contain the 'participants' key.")

    participants = meeting_report['participants']
    names = []
    duration = []
    for participant in participants:
        if participant['status'] == 'in_meeting':
            names.append(participant['name'])
            duration.append(np.round(
                participant['duration']/60., 0))
    attendance = {
        'name': names,
        'duration_min': duration
    }
    return attendance


def get_participant_details(meeting_report):
    participants = meeting_report['participants']
    names = []
    emails = []
    for participant in participants:
        if participant['status'] == 'in_meeting':
            names.append(participant['name'])
            emails.append(participant['user_email'])
    participant_details = {
        'name': names,
        'email': emails
    }
    return participant_details


def double_encoder(uuid):
    uuid_single_encode = urllib.parse.quote_plus(uuid)
    return (urllib.parse.quote_plus(uuid_single_encode))
