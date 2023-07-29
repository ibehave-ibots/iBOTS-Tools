from __future__ import annotations
from typing import Set

from .workflows import WorkshopRepo, SessionRecord, WorkshopRecord


class InMemoryWorkshopRepo(WorkshopRepo):
    
    def __init__(self, workshops) -> None:
        self.workshops = {workshop['id']: workshop for workshop in workshops}
        
    def list_workshops(self) -> Set[str]:
        return set(str(record['id']) for record in self.workshops.values())
        
    def get_workshop(self, workshop_id: str) -> WorkshopRecord:
        record = self.workshops[workshop_id]
        workshop = WorkshopRecord(
            id=record['id'], 
            name=record['name'], 
            description=record['description'],
            topics=record['topics'],
            scheduled_start=record['scheduled_start'],
            scheduled_end=record['scheduled_end'],
            session_ids=[session['id'] for session in record['sessions']],
            organizer=record['organizer'],
        )
        return workshop
    
    def get_session(self, session_id: str) -> SessionRecord:
        session_record = self._find_session_record(workshop_entries=self.workshops, session_id=session_id)    
        return SessionRecord(
            id=str('aa'), 
            scheduled_start=session_record['scheduled_start'],
            scheduled_end=session_record['scheduled_end'],
        )

    @staticmethod
    def _find_session_record(workshop_entries, session_id):
        for workshop in workshop_entries.values():
            for session in workshop['sessions']:
                if session['id'] == session_id:
                    return session
        else:
            raise ValueError(f"session_id not found: {session_id}")
        
    