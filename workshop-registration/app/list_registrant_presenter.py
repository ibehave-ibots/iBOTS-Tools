from abc import ABC, abstractmethod
from typing import List, Literal, NamedTuple, Dict, Any
from dataclasses import field
from uuid import uuid4

class RegistrantSummary(NamedTuple):
    name: str
    email: str
    status: Literal['approved','waitlisted','rejected']
    registered_on: str
    group_name: str
    workshop_id: str
    id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()


class ListRegistrantPresenter(ABC):

    @abstractmethod
    def show(self, registrants: List[RegistrantSummary]) -> None:
        ...
        
    def show_update(self, registrant: RegistrantSummary) -> None:
        ...