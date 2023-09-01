from __future__ import annotations
from typing import List, NamedTuple, TypedDict
import requests
from .zoom_oauth import create_access_token


class Meeting(NamedTuple):
    topic: str
    registration_url: str
    occurrences: List[Occurrence]
    agenda: str
    id: int

class Occurrence(NamedTuple):
    start_time: str


class ZoomAPI:

    def _get_access_token(self) -> str:
        access_data = create_access_token()
        access_token = access_data['access_token']
        return access_token
    

    def get_meeting(self, meeting_id) -> Meeting:
        access_token = self._get_access_token()
        
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