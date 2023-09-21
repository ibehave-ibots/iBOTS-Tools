from typing import List
from external.zoom_api.list_registrants import ZoomRegistrant

def add_registrants(access_token: str, user_id: str, meeting_id: str, registrants: List[ZoomRegistrant]) -> None:
    raise NotImplementedError