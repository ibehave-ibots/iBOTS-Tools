from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, NamedTuple



class WorkshopRecord(NamedTuple):
    id: str
    name: str
    description: str
    topics: List[str]
    scheduled_start: date
    scheduled_end: date
    session_ids: List[str]
    organizer: str


class SessionRecord(NamedTuple):
    id: str
    scheduled_start: datetime
    scheduled_end: datetime


class WorkshopRepo(ABC):
    
    @abstractmethod
    def get_workshop(self, workshop_id: str) -> WorkshopRecord: ...

    @abstractmethod
    def get_session(self, session_id: str) -> SessionRecord: ...

