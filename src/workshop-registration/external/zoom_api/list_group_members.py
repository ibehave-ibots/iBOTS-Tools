from typing import List, NamedTuple

import requests


class User(NamedTuple):
    id: str


def list_group_members(access_token: str, group_id: str) -> List[User]:
    response = requests.get(
            url=f"https://api.zoom.us/v2/groups/{group_id}/members",
            headers={"Authorization": f"Bearer {access_token}"},
        )
    response.raise_for_status()
    data = response.json()

    user_list = []
    for member in data['members']:
        user = User(id=member['id'])
        user_list.append(user)
    
    return user_list