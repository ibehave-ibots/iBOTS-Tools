from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, NamedTuple, NewType, Set


class Session(NamedTuple):
    id: str
    scheduled_start: datetime
    scheduled_end: datetime
   
    
WorkshopID = NewType("WorkshopID", str)
    
class Workshop(NamedTuple):
    id: WorkshopID
    name: str
    description: str
    scheduled_start: date
    scheduled_end: date
    sessions: List[Session]
    
    


class PlannedWorkshopWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    
    def list_all_workshops(self) -> List[WorkshopID]:
        return self.workshop_repo.list_workshops()
    
    def show_workshop_plan(self, workshop_id: WorkshopID) -> Workshop:
        workshop = self.workshop_repo.get_workshop(workshop_id=workshop_id)
        sessions = []
        for session_id in workshop.session_ids:
            session_entry = self.workshop_repo.get_session(session_id=session_id)
            session = Session(
                id=session_entry.id,
                scheduled_start=session_entry.scheduled_start,
                scheduled_end=session_entry.scheduled_end,
            )
            sessions.append(session)
            
        workshop_full = Workshop(
            id=WorkshopID(workshop.id),
            name=workshop.name,
            description=workshop.description,
            scheduled_start=workshop.scheduled_start,
            scheduled_end=workshop.scheduled_end,
            sessions=sessions,
        )
        return workshop_full



# Repo Interfaces

class WorkshopRecord(NamedTuple):
    id: str
    name: str
    description: str
    scheduled_start: date
    scheduled_end: date
    session_ids: List[str]


class SessionRecord(NamedTuple):
    id: str
    scheduled_start: datetime
    scheduled_end: datetime


class WorkshopRepo(ABC):
    
    @abstractmethod
    def list_workshops(self) -> Set[str]: ...
    
    @abstractmethod
    def get_workshop(self, workshop_id: str) -> WorkshopRecord: ...

    @abstractmethod
    def get_session(self, session_id: str) -> SessionRecord: ...

