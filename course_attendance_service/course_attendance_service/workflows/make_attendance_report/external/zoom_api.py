from datetime import datetime
from typing import Dict, List, Literal, TypedDict
import requests

# API to get participant report from Zoom

class ZoomParticipantsReportData(TypedDict):
    status: Literal['in_meeting','in_waiting_room']
    name: str
    user_email: str
    join_time: datetime
    leave_time: datetime

class ZoomMeetingData(TypedDict):
    start_time: datetime
    end_time: datetime
    
class ZoomParticipantsResponseData(TypedDict):
    participants: List[ZoomParticipantsReportData]

class ZoomAttendanceApi:
    @staticmethod
    def get_past_meeting_details(access_token:str, meeting_id:str, params:Dict=None) -> ZoomMeetingData:
        url = f"https://api.zoom.us/v2/report/past_meetings/{meeting_id}"
        header = {
            'Authorization': f"Bearer {access_token}"
        }

        response = requests.get(url, headers=header, params=params)
        response.raise_for_status()
        return response.json()            


    @staticmethod
    def get_zoom_participant_report(access_token:str, meeting_id: str, params:Dict = None) -> ZoomParticipantsResponseData:
        url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
        header = {
            'Authorization': f"Bearer {access_token}"
        }

        response = requests.get(url, headers=header, params=params)
        response.raise_for_status()
        return response.json() 
    
       