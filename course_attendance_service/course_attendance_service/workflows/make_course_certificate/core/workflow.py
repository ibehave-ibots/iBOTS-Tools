from __future__ import annotations

from typing import NamedTuple, Sequence

from .entities import Workshop, WorkshopID, Session
from .certificate_repo import CertificateRepo
from .certificate_builder import CertificateBuilder
from .workshop_repo import WorkshopRepo, WorkshopRecord, SessionRecord
        

class PlannedWorkshopWorkflow(NamedTuple):
    workshop_repo: WorkshopRepo
    certificate_builder: CertificateBuilder
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
        
        

