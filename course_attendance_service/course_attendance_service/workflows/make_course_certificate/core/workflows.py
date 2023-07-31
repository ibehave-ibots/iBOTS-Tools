from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Literal, NamedTuple, Sequence, Set, Union

from .entities import Workshop, WorkshopID, Session



class WritableData(NamedTuple):
    data: Union[bytes, str]
    recommended_extension: str
    
    @property
    def data_type(self) -> Literal['bytes', 'str']:
        return 'bytes' if isinstance(self.data, bytes)  else 'str'
    
    

class WorkshopCertificateBuilder(ABC):
    
    @abstractmethod
    def create_certificate_file(self,
        workshop_name: str, 
        workshop_description: str,
        start: date,
        end: date,
        workshop_topics: List[str],
        organizer: str,
    ) -> WritableData:
        ...                
        
        
class CertificateRepo(ABC):
    
    @abstractmethod
    def save_certificate(self, workshop_id: str, certificate_file: WritableData): ...

class PlannedWorkshopWorkflow(NamedTuple):
    workshop_repo: WorkshopRepo
    certificate_builder: WorkshopCertificateBuilder
    certificate_repo: CertificateRepo
    
    
    def make_workshop_certificate(self, workshop_id: WorkshopID) -> None:
        workshop_record = self.workshop_repo.get_workshop(workshop_id=workshop_id)
        session_records = [self.workshop_repo.get_session(session_id=session_id) for session_id in workshop_record.session_ids]
        workshop = self._build_workshop_from_records(workshop_record, session_records)
        certificate_file = self.certificate_builder.create_certificate_file(
            workshop_name=workshop.name, 
            workshop_description=workshop.description,
            start=workshop.scheduled_start,
            end=workshop.scheduled_end,
            workshop_topics=workshop.topics,
            organizer=workshop.organizer,
        )
        self.certificate_repo.save_certificate(
            workshop_id=workshop_id,
            certificate_file=certificate_file,
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
            organizer=workshop_record.organizer,
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

