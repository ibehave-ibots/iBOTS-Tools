from __future__ import annotations
from typing import Set

from .workflow import WorkshopRepo
from .zoom_api import ZoomRestApi


class ZoomWorkshopRepo(WorkshopRepo):
    
    def __init__(self, zoom_api: ZoomRestApi) -> None:
            self.zoom_api = zoom_api
            self.access_token = 'TOP-SECRET'
            self.group_id = 'TOP-SECRET'
            
    def list_workshops(self) -> Set[str]:
        
        all_meeting_ids: Set[str] = set()
        user_ids = self.zoom_api.list_users_in_group(group_id=self.group_id)
        for user_id in user_ids:
            data = self.zoom_api.list_scheduled_meetings_of_user(access_token=self.access_token, user_id=user_id)
            meeting_ids = set(data['meetings'])
            all_meeting_ids.update(meeting_ids)
        return all_meeting_ids
    