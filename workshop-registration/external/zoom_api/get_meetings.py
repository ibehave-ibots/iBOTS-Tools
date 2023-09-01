from __future__ import annotations
from typing import List, NamedTuple, Union
import requests

def get_meetings(access_token: str, user_id: int) -> List[MeetingSummary]:
        response = requests.get(
            url=f"https://api.zoom.us/v2/users/{user_id}/meetings",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data = response.json()
        meeting_summaries = []
        for meeting in data["meetings"]:
            if meeting["type"] == 2:
                meeting_summary = ScheduledMeetingSummary(
                    id=meeting["id"],
                    topic=meeting["topic"],
                    start_time=meeting["start_time"],
                )
            elif meeting["type"] == 8:
                meeting_summary = RecurringMeetingSummary(
                    id=meeting["id"],
                    topic=meeting["topic"],
                    agenda=meeting["agenda"],
                    start_time=meeting["start_time"],
                )
            meeting_summaries.append(meeting_summary)
        return meeting_summaries

class ScheduledMeetingSummary(NamedTuple):
    id: int
    topic: str
    start_time: str
    
class RecurringMeetingSummary(NamedTuple):
    id: int
    topic: str
    agenda: str
    start_time: str

MeetingSummary = Union[ScheduledMeetingSummary, RecurringMeetingSummary]