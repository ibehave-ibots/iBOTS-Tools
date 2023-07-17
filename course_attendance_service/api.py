from typing import List, NamedTuple, Union
from processing import double_encoder
import zoom_integration
import processing
from datetime import datetime, timedelta
from collections import defaultdict


class AttendanceReport(NamedTuple):
    """
    Contains session attendance report 

    _extended_summary_

    :param NamedTuple: _description_
    :type NamedTuple: _type_
    :return: _description_
    :rtype: _type_
    """
    names: Union[List[str], List[List[str]]]
    durations_min: List[float]
    emails: List[str]

    @property
    def n_participants(self) -> int:
        return len(self.names)

    @property
    def attendance_mark(self) -> List:
        attendance_mark = []
        max_duration = max(self.durations_min)
        for duration in self.durations_min:
            if duration/max_duration >= 0.75:
                attendance_mark.append(True)
            else:
                attendance_mark.append(False)
        return attendance_mark


class RegistrantDetails(NamedTuple):
    """
    Details of all participants registered for a Zoom meeting

    _extended_summary_

    :param NamedTuple: _description_
    :type NamedTuple: _type_
    """
    names: List[str]
    emails: List[str]


class MeetingDetails(NamedTuple):
    """
    Deatils of a Zoom meeting 

    _extended_summary_

    :param NamedTuple: _description_
    :type NamedTuple: _type_
    """
    title: str
    description: str
    date: str
    planned_start_time: str
    planned_end_time: str
    session_ids: List[str]


class ListMeetings(NamedTuple):
    meeting_id: List[int]


class WorkshopAttendanceReport(NamedTuple):
    """
    Final workshop attendance report

    _extended_summary_

    :param NamedTuple: _description_
    :type NamedTuple: _type_
    """
    workshop_attendees: List[str]
    workshop_attendance: List[str]


def get_attendance_report(token, meeting_id) -> AttendanceReport:
    """
    _summary_

    _extended_summary_

    :param token: _description_
    :type token: _type_
    :param meeting_id: _description_
    :type meeting_id: _type_
    :return: _description_
    :rtype: AttendanceReport
    """
    if isinstance(meeting_id, str):
        meeting_id = double_encoder(meeting_id)

    report = zoom_integration.get_participant_report(
        access_token=token, meeting_id=meeting_id)
    result = processing.get_attendance(meeting_report=report)
    
    participants = {}
    for name, duration, email in zip(result['name'], result['duration_min'], result['email']):
        if email not in participants:
            participants[email] = {'name': [name], 'duration': duration}
        else:
            participants[email]['name'].append(name)
            participants[email]['duration'] += duration
        
    results_new = {
        'name': [entry['name'] if len(entry['name']) > 1 else entry['name'][0] for entry in participants.values()],
        'duration_min': [entry['duration'] for entry in participants.values()],
        'email': list(participants.keys()),
    }
    result = results_new.copy()
    

    return AttendanceReport(names=result['name'],
                            durations_min=result['duration_min'], emails=result['email'])


def get_workshop_attendance_report(token, meeting_id) -> WorkshopAttendanceReport:
    # uuids of all sessions of past meeting
    past_meeting_report = zoom_integration.get_past_meeting_details(
        access_token=token, meeting_id=meeting_id)

    uuids = processing.get_uuids(past_meeting_report)

    # getting attendance report of each session
    # assumes all names are unique and names of each attendee remains consistent through all sessions
    names = []
    attendances = []
    for uuid in uuids:
        session_report = get_attendance_report(token, uuid)
        names.append(session_report.names)
        attendances.append(session_report.attendance_mark)
    workshop = get_workshop_attendance(
        names, attendances)
    return (WorkshopAttendanceReport(workshop_attendees=list(workshop.keys()), workshop_attendance=list(workshop.values())))


def get_workshop_attendance(names_lists, attendance_lists):
    workshop_attendance = defaultdict(int)
    total_sessions = len(attendance_lists)

    # for names, attendance in zip(names_lists, attendance_lists):
    #     for name, is_present in zip(names, attendance):
    #         if name not in workshop_attendance:
    #             workshop_attendance[name] = is_present
    #         else:
    #             workshop_attendance[name] &= is_present

    for names, attendance in zip(names_lists, attendance_lists):
        for name, is_present in zip(names, attendance):
            workshop_attendance[name] += int(is_present)

    min_sessions_attended = total_sessions * 0.8

    final_attendance = {
        name: attendance >= min_sessions_attended
        for name, attendance in workshop_attendance.items()
    }

    return final_attendance


def get_meeting_details(token, meeting_id):
    if isinstance(meeting_id, str):
        meeting_id = double_encoder(meeting_id)

    report = zoom_integration.get_meeting(
        access_token=token, meeting_id=meeting_id)

    # date of meeting
    datetime_obj = datetime.strptime(
        report['start_time'], '%Y-%m-%dT%H:%M:%SZ')
    meeting_date = datetime_obj.date().strftime('%Y-%m-%d')

    # start and end time of meeting
    start_time = datetime_obj.time().strftime('%H:%M:%S')
    end_time = datetime_obj + timedelta(minutes=report['duration'])
    end_time = end_time.strftime('%H:%M:%S')

    # uuids of all sessions of past meeting
    past_meeting_report = zoom_integration.get_past_meeting_details(
        access_token=token, meeting_id=meeting_id)

    uuids = processing.get_uuids(past_meeting_report)

    return MeetingDetails(title=report['topic'], description=report['agenda'], date=meeting_date, planned_start_time=start_time, planned_end_time=end_time, session_ids=uuids)


def get_registrant_details(token, meeting_id) -> RegistrantDetails:
    report = zoom_integration.get_registrants(
        access_token=token, meeting_id=meeting_id)
    result = processing.get_registrant_details(report)
    return RegistrantDetails(names=result['name'], emails=result['email'])


def list_meeting_ids(token_data, from_date=None, to_date=None):
    report = zoom_integration.get_meetings_of_member(
        token_data, from_date=from_date, to_date=to_date)
    meeting_ids = processing.get_meeting_ids(report)
    return ListMeetings(meeting_id=meeting_ids)
