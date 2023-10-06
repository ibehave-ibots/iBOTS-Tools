from __future__ import annotations
from typing import Dict, List, Literal, NamedTuple

import requests

def get_attendees(access_token: str, meeting_id: str) -> List[ZoomAttendee]:
    response = requests.get(
        url=f"https://api.zoom.us/v2/report/meetings/{meeting_id.replace(' ', '')}/participants",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    data = response.json()
    participants = list(filter(lambda x: x["status"] == "in_meeting", data["participants"]))
    return participants
    
    
class ZoomAttendee(NamedTuple):
    name: str
    user_email: str
    session: str
    join_time: str
    leave_time: str