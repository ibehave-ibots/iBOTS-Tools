from __future__ import annotations
from typing import List, NamedTuple
import requests

def get_meeting(access_token: str, meeting_id: str) -> Meeting:
        response = requests.get(
            url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data = response.json()
        meeting = Meeting(
            topic=data['topic'], 
            registration_url=data['registration_url'], 
            occurrences=[Occurrence(start_time=occ["start_time"]) for occ in data["occurrences"]],
            agenda=data["agenda"],
            id=data["id"],
        )
        return meeting

class Meeting(NamedTuple):
    topic: str
    registration_url: str
    occurrences: List[Occurrence]
    agenda: str
    id: int

class Occurrence(NamedTuple):
    start_time: str