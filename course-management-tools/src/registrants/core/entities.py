from typing import NamedTuple, Union, List


class Registrant(NamedTuple):
    user_id: str
    name: str
    affiliation: Union[str, List[str]]
    email: str
    status: str
