from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, NamedTuple, Sequence, Set

from .entities import Workshop, WorkshopID, Session


class WorkshopCertificatePresenter(ABC):
    ...
    # def present(self, workshop: Workshop) -> None:
    #     ...
        

class PlannedWorkshopWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    
    def list_all_workshops(self) -> List[WorkshopID]:
        return self.workshop_repo.list_workshops()
    
    def make_workshop_certificate(self, workshop_id: WorkshopID, presenter: WorkshopCertificatePresenter) -> None:
        workshop_record = self.workshop_repo.get_workshop(workshop_id=workshop_id)
        session_records = [self.workshop_repo.get_session(session_id=session_id) for session_id in workshop_record.session_ids]
        workshop = self._build_workshop_from_records(workshop_record, session_records)
        presenter.present(
            workshop_name=workshop.name, 
            workshop_description=workshop.description,
            start=workshop.scheduled_start,
            end=workshop.scheduled_end,
            workshop_topics=workshop.topics,
        )
        

    @staticmethod
    def _build_workshop_from_records(workshop_record: WorkshopRecord, session_records: Sequence[SessionRecord]) -> Workshop:
        sessions = []
        for session_record in session_records:
            session = Session(
                id=session_record.id,
                scheduled_start=session_record.scheduled_start,
                scheduled_end=session_record.scheduled_end,
            )
            sessions.append(session)
            
        workshop = Workshop(
            id=WorkshopID(workshop_record.id),
            name=workshop_record.name,
            description=workshop_record.description,
            topics=workshop_record.topics,
            scheduled_start=workshop_record.scheduled_start,
            scheduled_end=workshop_record.scheduled_end,
            sessions=session_records,
        )
        return workshop
        
        


# Repo Interfaces

class WorkshopRecord(NamedTuple):
    id: str
    name: str
    description: str
    topics: List[str]
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

