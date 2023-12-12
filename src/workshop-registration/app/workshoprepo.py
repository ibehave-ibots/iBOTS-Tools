from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import uuid

class WorkshopRepo(ABC):

    @abstractmethod
    def get_upcoming_workshops(self) -> list[WorkshopRecord]: ...


@dataclass(frozen=True)
class WorkshopRecord:
    link: str
    title: str
    date: str
    capacity: int
    id: str = field(default_factory= lambda: str(uuid.uuid4()))
