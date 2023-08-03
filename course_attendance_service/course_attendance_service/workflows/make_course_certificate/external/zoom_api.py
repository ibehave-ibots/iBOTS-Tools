from __future__ import annotations
from typing import List, TypedDict, Union

import requests


class ZoomRestApi:
    
    @staticmethod
    def get_meeting(access_token, meeting_id) -> ZoomGetMeetingResponseData:
        response = requests.get(
            url = f"https://api.zoom.us/v2/meetings/{meeting_id}", 
            headers = {'Authorization': f"Bearer {access_token}"}
        )
        response.raise_for_status()
        data: ZoomGetMeetingResponseData = response.json()
        return data
    
        
class ZoomGetMeetingResponseData(TypedDict):
    id: Union[int, str]
    topic: str
    start_time: str # planned start: '%Y-%m-%dT%H:%M:%SZ'
    duration: int # minutes
    agenda: str
    occurrences: List[ZoomOccurance]
    
    
class ZoomOccurance(TypedDict):
    duration: int
    occurance_id: str
    start_time: str  # date-time
    status: str  # Occurence status