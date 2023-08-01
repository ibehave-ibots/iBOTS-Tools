from __future__ import annotations
from typing import TypedDict, Union

import requests


class ZoomRestApi:
    
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
        
        
        
    
class ZoomListMeetingsResponseData(TypedDict):
    meetings: None