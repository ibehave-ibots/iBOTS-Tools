from typing import Dict, List, Union
import requests

# API to get participant report from Zoom
class ZoomAttendanceApi:
    @staticmethod
    def get_zoom_participant_report(access_token:str, meeting_id: str, params:Dict = None):
        url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
        header = {
            'Authorization': f"Bearer {access_token}"
        }

        response = requests.get(url, headers=header, params=params)
        response.raise_for_status()
        return response.json()    