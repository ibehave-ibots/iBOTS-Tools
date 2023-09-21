import json
from external.zoom_api.get_meeting import Meeting
import requests


def create_meeting(access_token: str, user_id: str, meeting: Meeting) -> None:
    parameters = {
                "topic": meeting.topic
                  }
    response = requests.post(
        url=f"https://api.zoom.us/v2/users/{user_id}/meetings",
        headers={"Authorization": f"Bearer {access_token}"},
        data=json.dumps(parameters)
    )
    response.raise_for_status()
    raise NotImplementedError("check that response is OK")
