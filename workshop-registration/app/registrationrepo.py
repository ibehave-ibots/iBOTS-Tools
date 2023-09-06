from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Literal
import uuid

class RegistrationRepo(ABC):

    @abstractmethod
    def get_registrations(self, workshop_id: str) -> List[RegistrationRecord]: ...


@dataclass(frozen=True)
class RegistrationRecord:
    workshop_id: str
    name: str
    status: Literal['approved', 'rejected', 'waitlisted'] 
    id: str = field(default_factory= lambda: str(uuid.uuid4()))