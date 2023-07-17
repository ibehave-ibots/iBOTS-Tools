import urllib.parse
import numpy as np


def get_attendance(meeting_report):
    """
    Extract attendance data from a meeting report.

    This function takes a meeting report dictionary obtained from the Zoom API and extracts attendance data,
    including participant names and their corresponding durations.

    :param meeting_report: The meeting report dictionary obtained from the Zoom API.
    :type meeting_report: dict
    :raises TypeError: If the meeting_report parameter is not a dictionary.
    :raises KeyError: If the meeting_report dictionary does not contain the 'participants' key.
    :return: A dictionary containing participant names and their corresponding durations.
    :rtype: dict
    """
    if not isinstance(meeting_report, dict):
        raise TypeError("The meeting_report parameter must be a dictionary.")

    if 'participants' not in meeting_report:
        raise KeyError(
            "The meeting_report dictionary must contain the 'participants' key.")

    participants = meeting_report['participants']
    names = []
    duration = []
    emails = []
    for participant in participants:
        if participant['status'] == 'in_meeting':
            names.append(participant['name'])
            duration.append(np.round(
                participant['duration']/60., 0))
            emails.append(participant['user_email'])
    attendance = {
        'name': names,
        'duration_min': duration,
        'email': emails
    }
    return attendance


def get_meeting_ids(meeting_report):
    meeting_ids = []
    meetings = meeting_report['meetings']
    for meeting in meetings:
        meeting_ids.append(meeting['id'])
    return meeting_ids


def get_registrant_details(report):
    registrants = report['registrants']
    names = []
    emails = []
    for registrant in registrants:
        names.append(registrant['first_name'] +
                     '' + registrant['last_name'])
        emails.append(registrant['email'])
    registrant_details = {
        'name': names,
        'email': emails
    }
    return registrant_details


def get_uuids(report):
    past_meetings = report['meetings']
    uuids = []
    for past_meeting in past_meetings:
        uuids.append(past_meeting['uuid'])
    return uuids


def double_encoder(uuid):
    uuid_single_encode = urllib.parse.quote_plus(uuid)
    return (urllib.parse.quote_plus(uuid_single_encode))
