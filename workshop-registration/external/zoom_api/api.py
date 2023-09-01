from typing import NamedTuple
import requests
from .zoom_oauth import create_access_token


class Meeting(NamedTuple):
    topic: str

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
        
        return Meeting(topic=data['topic'])