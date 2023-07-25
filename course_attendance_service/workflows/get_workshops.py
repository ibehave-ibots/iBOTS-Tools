from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
import random
from typing import List, NamedTuple, NewType, Set
from string import ascii_letters

############# TESTS

def test_list_all_workshops_ids():
    random.seed(42)
    given_workshops = [
        {'id': random.choice(ascii_letters)},
        {'id': random.choice(ascii_letters)}
    ]
    
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    workflows = GetWorkshopWorkflows(workshop_repo=repo)
    
    workshop_ids = workflows.list_all_workshops()
    assert workshop_ids == {given_workshops[0]['id'], given_workshops[1]['id']}
    
    
    
def test_get_workshop_details():
    random.seed(42)
    given_workshops = [
        {
            'id': random.choice(ascii_letters), 
            'name': random.choice(['IntroPy', 'IntroR', 'IntroMat']),
            'description': ''.join(random.choices(ascii_letters, k=3)),
            'planned_start': datetime(2023, 1, 18, 9, 30),
            'planned_end': datetime(2023, 1, 21, 17, 45),
            'session_ids': ['aa', 'bb', 'cc'],
            
        },
    ]
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    workflows = GetWorkshopWorkflows(workshop_repo=repo)
    
    workshop = workflows.get_workshop_details(workshop_id=given_workshops[0]['id'])
    assert workshop.name == given_workshops[0]['name']
    assert workshop.description == given_workshops[0]['description']
    assert workshop.planned_start == given_workshops[0]['planned_start']
    assert workshop.planned_end == given_workshops[0]['planned_end']
    assert workshop.session_ids == given_workshops[0]['session_ids']
    
    
def test_get_session_details():
    random.seed(42)
    given_workshops = [
        {
            'id': random.choice(ascii_letters), 
            'sessions': [
                {'id': random.choice(ascii_letters), 'planned_start': datetime(2023, 1, 19, 9, 30)},
            ]
        },
    ]
    
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    workflows = GetWorkshopWorkflows(workshop_repo=repo)
    given_sessions = given_workshops[0]['sessions']
    session = workflows.get_session_details(session_id=given_sessions[0]['id'])
    assert session.planned_start == given_sessions[0]['planned_start']
    
    
    

########## SRC    

WorkshopId = NewType('WorkshopId', str)

class Workshop(NamedTuple):
    id: WorkshopId
    name: str
    description: str
    planned_start: datetime
    planned_end: datetime
    session_ids: List[str]
    
    
SessionId = NewType('SessionId', str)

class Session(NamedTuple):
    id: SessionId
    planned_start: datetime

class WorkshopRepo(ABC):
    
    @abstractmethod
    def list_workshops(self) -> Set[WorkshopId]: ...
    
    @abstractmethod
    def get_workshop_details(self, workshop_id: WorkshopId) -> Workshop: ...
    
    @abstractmethod
    def get_session_details(self, session_id: SessionId) -> Session: ...


class GetWorkshopWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    
    def list_all_workshops(self) -> List[WorkshopId]:
        return self.workshop_repo.list_workshops()
    
    def get_workshop_details(self, workshop_id: str):
        workshop = self.workshop_repo.get_workshop_details(workshop_id=workshop_id)
        return workshop
    
    def get_session_details(self, session_id: str):
        session = self.workshop_repo.get_session_details(session_id=session_id)
        return session
    
    
    
class InMemoryWorkshopRepo(WorkshopRepo):
    
    def __init__(self, workshops) -> None:
        self.workshops = {workshop['id']: workshop for workshop in workshops}
        
    def list_workshops(self) -> Set[WorkshopId]:
        return set(WorkshopId(record['id']) for record in self.workshops.values())
        
    def get_workshop_details(self, workshop_id: WorkshopId) -> Workshop:
        record = self.workshops[workshop_id]
        workshop = Workshop(
            id=record['id'], 
            name=record['name'], 
            description=record['description'],
            planned_start=record['planned_start'],
            planned_end=record['planned_end'],
            session_ids=['aa', 'bb', 'cc']
        )
        return workshop
    
    def get_session_details(self, session_id: SessionId) -> Session:
        session_record = self._find_session_record(workshop_entries=self.workshops, session_id=session_id)    
        return Session(id=SessionId('aa'), planned_start=session_record['planned_start'])

    @staticmethod
    def _find_session_record(workshop_entries, session_id):
        for workshop in workshop_entries.values():
            for session in workshop['sessions']:
                if session['id'] == session_id:
                    return session
        else:
            raise ValueError(f"session_id not found: {session_id}")
        
    