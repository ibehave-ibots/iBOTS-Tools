from __future__ import annotations
from typing import TypedDict, Union

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
    
    @staticmethod
    def list_scheduled_meetings_of_user(access_token, user_id) -> ZoomListMeetingsResponseData:
        response = requests.get(
            url=f"https://api.zoom.us/v2/users/{user_id}/meetings",
            params={'type': 'scheduled'},  #, 'from': from_date, 'to': to_date}
            headers = {'Authorization': f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data: ZoomListMeetingsResponseData = response.json()
        return data
        
        
    @staticmethod
    def list_users_in_group(access_token, group_id):
        response = requests.get(
            url = f"https://api.zoom.us/v2/groups/{group_id}/members",
            headers = {'Authorization': f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data: ZoomListMeetingsResponseData = response.json()
        return data
        
        
        
class ZoomGetMeetingResponseData(TypedDict):
    id: Union[int, str]
    topic: str
    start_time: str # planned start: '%Y-%m-%dT%H:%M:%SZ'
    duration: int # minutes
    agenda: str
    
class ZoomListMeetingsResponseData(TypedDict):
            meetings: None