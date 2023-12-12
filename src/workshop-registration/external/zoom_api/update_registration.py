
from typing import Literal
import json
import requests
from external.zoom_api.list_registrants import ZoomRegistrant


def zoom_call_update_registration(
        access_token: str,
        meeting_id: str,
        registrant: ZoomRegistrant) -> None:

    action_from_new_status = {
        "approved": "approve",
        "denied": "deny",
        }
    
    parameters = {
                "action": action_from_new_status[registrant.status],
                "registrants":[
                    {"email": registrant.email,
                     "id": registrant.id}
                ]
                  }
    response = requests.put(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}/registrants/status",
        headers={"Authorization": f"Bearer {access_token}"},
        json=parameters
    )
    response.raise_for_status()