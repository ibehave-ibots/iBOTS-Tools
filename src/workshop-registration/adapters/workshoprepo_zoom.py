from dataclasses import dataclass
from typing import Callable, Optional
import yaml
from warnings import warn
from external.zoom_api import RecurringMeetingSummary, OAuthGetToken, get_meeting, get_meetings
from external.zoom_api import list_group_members
from app import WorkshopRepo, WorkshopRecord

@dataclass(frozen=True)
class ZoomWorkshopRepo(WorkshopRepo):
    oauth_get_token: OAuthGetToken
    get_meetings: Callable = get_meetings
    get_meeting: Callable = get_meeting
    list_group_members: Callable = list_group_members
    group_id: Optional[str] = None
    user_id: Optional[str] = None

    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        access_token = self.oauth_get_token.create_access_token()['access_token']


        match self.group_id , self.user_id :
            case None, None: 
                raise ValueError("C'mon, I some info to work with!")
            case None, str(user_id): 
                user_ids = [user_id]
            case str(group_id), None:
                group_members = list_group_members(access_token=access_token,group_id=group_id)
                user_ids = [member.id for member in group_members]
            case _:
                raise ValueError('Pick one: user_id or group_id')


        meeting_summaries = []
        for user_id in user_ids:
            data = self.get_meetings(access_token=access_token, user_id=user_id)
            meeting_summaries.extend(data)

        workshop_records = []
        for meeting_summary in meeting_summaries:
            match meeting_summary:
                case RecurringMeetingSummary():
                    meeting = self.get_meeting(access_token=access_token, meeting_id=str(meeting_summary.id))
                    if meeting.agenda == "" or len(meeting.agenda.split('---'))!=2:
                        continue

                    metadata = yaml.load(meeting.agenda.split("---")[1], Loader=yaml.Loader)
                    
                    if not meeting.occurrences:
                        warn(f"No occurrances found in Zoom for meeting ID {meeting_summary.id}. Look at meeting on website")
                    workshop_record = WorkshopRecord(
                        link=meeting.registration_url,
                        title=meeting_summary.topic,
                        date=meeting.occurrences[0].start_time[:10] if meeting.occurrences else "",
                        capacity=metadata["Capacity"],
                        id=str(meeting_summary.id),
                    )
                    workshop_records.append(workshop_record)
                case _:
                    continue
        return workshop_records