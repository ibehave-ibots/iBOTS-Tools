from __future__ import annotations
from typing import Dict, List, NamedTuple, Sequence

import requests

def get_attendees(access_token: str, meeting_id: str) -> List[ZoomAttendee]:
    session_uuids = get_session_uuids(access_token=access_token, meeting_id=meeting_id)
    zoom_attendees = []
    for session_idx, session_uuid in enumerate(session_uuids):
        response = requests.get(
            url=f"https://api.zoom.us/v2/report/meetings/{session_uuid}/participants",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data = response.json()
        
        participants = list(filter(lambda x: x["status"] == "in_meeting", data["participants"]))
       
        for participant in participants:
            zoom_attendee = ZoomAttendee(
                name=participant["name"],
                user_email=participant["user_email"],
                session=f"Day{session_idx+1}",
                join_time=participant["join_time"],
                leave_time=participant["leave_time"]
            )
            zoom_attendees.append(zoom_attendee)
    return zoom_attendees
    
def get_session_uuids(access_token: str, meeting_id: str) -> Sequence[str]:
    response = requests.get(
        url=f"https://api.zoom.us/v2/past_meetings/{meeting_id.replace(' ', '')}/instances",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    data = response.json()
    sessions: List[Dict[str, str]] = list(sorted(data["meetings"], key=lambda x: x["start_time"]))
    session_uuids = tuple(s["uuid"] for s in sessions)
    return session_uuids

    
class ZoomAttendee(NamedTuple):
    name: str
    user_email: str
    session: str
    join_time: str
    leave_time: str
