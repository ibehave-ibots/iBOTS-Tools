from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Literal
import uuid


class RegistrationRepo(ABC):
    @abstractmethod
    def get_registrations(self, workshop_id: str) -> List[RegistrationRecord]:
        ...


@dataclass(frozen=True)
class RegistrationRecord:
    workshop_id: str
    name: str
    registered_on: str
    custom_questions: List[Dict[str, str]]
    email: str
    status: Literal["approved", "rejected", "waitlisted"]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def update_status(self, status):
        self.updated_status = status