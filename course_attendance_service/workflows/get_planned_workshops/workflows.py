from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, NamedTuple, Set


class PlannedSession(NamedTuple):
    id: str
    start: datetime
    end: datetime
   
    
class PlannedWorkshop(NamedTuple):
    id: str
    name: str
    description: str
    planned_start: datetime
    planned_end: datetime
    sessions: List[PlannedSession]
    

class PlannedWorkshopWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    
    def list_all_planned_workshops(self) -> List[str]:
        return self.workshop_repo.list_workshops()
    
    def get_planned_workshop_details(self, workshop_id: str) -> PlannedWorkshop:
        workshop = self.workshop_repo.get_workshop(workshop_id=workshop_id)
        return workshop
    
    def get_planned_workshop_and_session_details(self, workshop_id: str) -> PlannedWorkshop:
        workshop = self.get_planned_workshop_details(workshop_id=workshop_id)
        sessions = []
        for session_id in workshop.session_ids:
            session_dto = self.workshop_repo.get_session(session_id=session_id)
            session = PlannedSession(**session_dto._asdict())
            sessions.append(session)
            
        workshop_full = PlannedWorkshop(
            id=workshop.id,
            name=workshop.name,
            description=workshop.description,
            planned_start=workshop.planned_start,
            planned_end=workshop.planned_end,
            sessions=sessions,
        )
        return workshop_full



# Repo Interfaces

class PlannedWorkshopDTO(NamedTuple):
    id: str
    name: str
    description: str
    planned_start: datetime
    planned_end: datetime
    session_ids: List[str]


class PlannedSessionDTO(NamedTuple):
    id: str
    start: datetime
    end: datetime


class WorkshopRepo(ABC):
    
    @abstractmethod
    def list_workshops(self) -> Set[str]: ...
    
    @abstractmethod
    def get_workshop(self, workshop_id: str) -> PlannedWorkshopDTO: ...

    @abstractmethod
    def get_session(self, session_id: str) -> PlannedSessionDTO: ...

