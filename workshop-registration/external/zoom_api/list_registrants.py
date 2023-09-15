from __future__ import annotations
from typing import Dict, List, Literal, NamedTuple

import requests


def list_registrants(
    access_token: str, meeting_id: str, status: Literal["approved", "pending", "denied"]
) -> List:
    response = requests.get(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}/registrants",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"status": status},
    )
    response.raise_for_status()
    data = response.json()
    registrants = []
    for registrant in data["registrants"]:
        registrant = ZoomRegistrant(
            first_name=registrant["first_name"],
            last_name=registrant["last_name"],
            email=registrant["email"],
            status=registrant["status"],
            registered_on=registrant["create_time"],
            custom_questions=registrant["custom_questions"]
        )
        registrants.append(registrant)

    return registrants


class ZoomRegistrant(NamedTuple):
    first_name: str
    last_name: str
    email: str
    status: Literal["approved", "pending", "denied"]
    registered_on: str
    custom_questions: List[Dict[str,str]]
