from __future__ import annotations
from typing import List, Literal, NamedTuple

import requests


def list_registrants(access_token: str, meeting_id: str, status: Literal['approved','pending','denied']) -> List:
    response = requests.get(
            url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}/registrants",
            headers={"Authorization": f"Bearer {access_token}"},
            params={'status': status}
        )
    response.raise_for_status()
    data = response.json()
    registrants=[]
    for registrant in data["registrants"]:
        registrant=Registrant()
        registrants.append(registrant)

    return registrants


class Registrant(NamedTuple):
    pass
