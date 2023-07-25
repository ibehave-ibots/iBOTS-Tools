from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random
from typing import List, NamedTuple, NewType, Set
from string import ascii_letters

############# TESTS
rand_letters = lambda: ''.join(random.choices(ascii_letters, k=4))
rand_date = lambda: datetime(year=random.randint(1900, 2100), month=random.randint(1, 12), day=random.randint(1, 28))
    
                               
def test_list_all_workshops_ids():
    random.seed(42)
    given_workshops = [
        {'id': rand_letters()},
        {'id': rand_letters()}
    ]
    
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    workflows = PlannedWorkshopWorkflows(workshop_repo=repo)
    
    workshop_ids = workflows.list_all_planned_workshops()
    assert workshop_ids == {given_workshops[0]['id'], given_workshops[1]['id']}
    
    
def test_get_workshop_and_session_details():
    random.seed(42)
    
def test_get_workshop_details():
    random.seed(42)
    
    given_workshops = [
        {
            'id': rand_letters(), 
            'name': rand_letters(),
            'description': rand_letters(),
            'planned_start': (s := rand_date()),
            'planned_end': (s + timedelta(days=random.randint(1, 6))),
            'sessions': [
                {'id': (sid := rand_letters()), 
                 'planned_start': (s := rand_date()), 
                 'planned_end': s + timedelta(hours=random.randint(3, 10)),
                }],
            'session_ids': [sid],
        },
    ]
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    workflows = PlannedWorkshopWorkflows(workshop_repo=repo)
    
    workshop = workflows.get_planned_workshop_and_session_details(workshop_id=given_workshops[0]['id'])
    assert workshop.name == given_workshops[0]['name']
    assert workshop.description == given_workshops[0]['description']
    assert workshop.planned_start == given_workshops[0]['planned_start']
    assert workshop.planned_end == given_workshops[0]['planned_end']
    given_sessions = given_workshops[0]['sessions']
    session = workflows.get_planned_session_details(session_id=given_sessions[0]['id'])
    assert session.start == given_sessions[0]['planned_start']
    assert session.end == given_sessions[0]['planned_end']
    
    
def test_get_session_details():
    random.seed(42)
    given_workshops = [
        {
            'id': rand_letters(), 
            'sessions': [
                {'id': rand_letters(), 
                 'planned_start': (s := rand_date()), 
                 'planned_end': s + timedelta(hours=random.randint(3, 10)),
                 },
            ]
        },
    ]
    
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    workflows = PlannedWorkshopWorkflows(workshop_repo=repo)
    given_sessions = given_workshops[0]['sessions']
    session = workflows.get_planned_session_details(session_id=given_sessions[0]['id'])
    assert session.start == given_sessions[0]['planned_start']
    assert session.end == given_sessions[0]['planned_end']
    
    
    

########## SRC    

WorkshopId = NewType('WorkshopId', str)

class PlannedWorkshop(NamedTuple):
    id: WorkshopId
    name: str
    description: str
    planned_start: datetime
    planned_end: datetime
    session_ids: List[str]
    
    
SessionId = NewType('SessionId', str)

class PlannedSession(NamedTuple):
    id: SessionId
    start: datetime
    end: datetime
    
class PlannedWorkshopAndSessions(NamedTuple):
    id: WorkshopId
    name: str
    description: str
    planned_start: datetime
    planned_end: datetime
    sessions: List[PlannedSession]
    

class WorkshopRepo(ABC):
    
    @abstractmethod
    def list_workshops(self) -> Set[WorkshopId]: ...
    
    @abstractmethod
    def get_workshop_details(self, workshop_id: WorkshopId) -> PlannedWorkshop: ...
    
    @abstractmethod
    def get_session_details(self, session_id: SessionId) -> PlannedSession: ...


class PlannedWorkshopWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    
    def list_all_planned_workshops(self) -> List[WorkshopId]:
        return self.workshop_repo.list_workshops()
    
    def get_planned_workshop_details(self, workshop_id: str) -> PlannedWorkshop:
        workshop = self.workshop_repo.get_workshop_details(workshop_id=workshop_id)
        return workshop
    
    def get_planned_session_details(self, session_id: str) -> PlannedSession:
        session = self.workshop_repo.get_session_details(session_id=session_id)
        return session
    
    def get_planned_workshop_and_session_details(self, workshop_id: str) -> PlannedWorkshopAndSessions:
        workshop = self.get_planned_workshop_details(workshop_id=workshop_id)
        sessions = []
        for session_id in workshop.session_ids:
            session = self.get_planned_session_details(session_id=session_id)
            sessions.append(session)
        workshop_full = PlannedWorkshopAndSessions(
            id=workshop.id,
            name=workshop.name,
            description=workshop.description,
            planned_start=workshop.planned_start,
            planned_end=workshop.planned_end,
            sessions=sessions,
        )
        return workshop_full
    
class InMemoryWorkshopRepo(WorkshopRepo):
    
    def __init__(self, workshops) -> None:
        self.workshops = {workshop['id']: workshop for workshop in workshops}
        
    def list_workshops(self) -> Set[WorkshopId]:
        return set(WorkshopId(record['id']) for record in self.workshops.values())
        
    def get_workshop_details(self, workshop_id: WorkshopId) -> PlannedWorkshop:
        record = self.workshops[workshop_id]
        workshop = PlannedWorkshop(
            id=record['id'], 
            name=record['name'], 
            description=record['description'],
            planned_start=record['planned_start'],
            planned_end=record['planned_end'],
            session_ids=record['session_ids']
        )
        return workshop
    
    def get_session_details(self, session_id: SessionId) -> PlannedSession:
        session_record = self._find_session_record(workshop_entries=self.workshops, session_id=session_id)    
        return PlannedSession(
            id=SessionId('aa'), 
            start=session_record['planned_start'],
            end=session_record['planned_end'],
        )

    @staticmethod
    def _find_session_record(workshop_entries, session_id):
        for workshop in workshop_entries.values():
            for session in workshop['sessions']:
                if session['id'] == session_id:
                    return session
        else:
            raise ValueError(f"session_id not found: {session_id}")
        
    