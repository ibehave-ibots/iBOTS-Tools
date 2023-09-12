from dataclasses import dataclass
from typing import Callable
import yaml
from warnings import warn
from external.zoom_api import RecurringMeetingSummary, OAuthGetToken, get_meeting, get_meetings
from app import WorkshopRepo, WorkshopRecord

@dataclass(frozen=True)
class ZoomWorkshopRepo(WorkshopRepo):
    user_id: str
    get_meeting: get_meeting
    get_meetings: get_meetings
    oauth_get_token: OAuthGetToken

    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        access_token = self.oauth_get_token.create_access_token()['access_token']
        meeting_summaries = self.get_meetings(access_token=access_token, user_id=self.user_id)
        workshop_records = []
        for meeting_summary in meeting_summaries:
            match meeting_summary:
                case RecurringMeetingSummary():
                    meeting = self.get_meeting(access_token=access_token, meeting_id=str(meeting_summary.id))
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