import random
from typing import Literal
import requests


def create_random_zoom_registrant(access_token: str, meeting_id: str, status: Literal["approved", "pending", "denied"]) -> str:
    random_number = random.randint(1, 1e5)
    fname = 'test'+str(random_number)
    params = {
    "first_name": fname,
    "last_name": 'last_name',
    "email": f'eve{random_number}@lname.com',
    "custom_questions": [{'title':'Research Group', 'value': 'AG Bashiri'}],
    "status": status
    }
    response = requests.post(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ','')}/registrants",
        headers={"Authorization": f"Bearer {access_token}"},
        json=params,
        )
    response.raise_for_status()
    return response.json()['registrant_id']
    

def delete_zoom_registrant(access_token: str, meeting_id: str, registrant_id: str) -> None:
    response = requests.delete(
            url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}/registrants/{registrant_id}",
            headers={"Authorization": f"Bearer {access_token}"},
            )
    response.raise_for_status()