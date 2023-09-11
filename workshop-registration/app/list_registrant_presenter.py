from abc import ABC, abstractmethod
from typing import List, Literal, NamedTuple, Dict, Any


class RegistrantSummary(NamedTuple):
    name: str
    email: str
    status: Literal['approved','waitlisted','rejected']
    registered_on: str
    group_name: str

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()


class ListRegistrantPresenter(ABC):

    @abstractmethod
    def show(self, registrants: List[RegistrantSummary]) -> None:
        ...