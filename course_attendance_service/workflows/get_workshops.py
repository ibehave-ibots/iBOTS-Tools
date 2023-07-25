from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from random import randint, choices, seed
from typing import List, NamedTuple, Set
from string import ascii_letters

############# TESTS
rand_letters = lambda: ''.join(choices(ascii_letters, k=4))
rand_date = lambda: datetime(year=randint(1900, 2100), month=randint(1, 12), day=randint(1, 28))
    
                               
def test_list_all_workshops_ids():
    seed(42)
    
    for _ in range(10):
        given_workshops = [{'id': rand_letters()} for _ in range(randint(0, 10))]
        
        repo = InMemoryWorkshopRepo(workshops=given_workshops)
        workflows = PlannedWorkshopWorkflows(workshop_repo=repo)
        
        workshop_ids = workflows.list_all_planned_workshops()
        assert workshop_ids == {workshop['id'] for workshop in given_workshops}

    
def test_get_workshop_details():
    seed(42)
    
    for _ in range(3):
        given_workshops = [
            {
                'id': rand_letters(), 
                'name': rand_letters(),
                'description': rand_letters(),
                'planned_start': (s := rand_date()),
                'planned_end': (s + timedelta(days=randint(1, 6))),
                'sessions': [
                    {'id': (sid := rand_letters()), 
                    'planned_start': (s := rand_date()), 
                    'planned_end': s + timedelta(hours=randint(3, 10)),
                    }],
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
        
        session = workshop.sessions[0]
        assert session.start == given_sessions[0]['planned_start']
        assert session.end == given_sessions[0]['planned_end']
    

########## SRC    


### Workflows
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
            session = self.workshop_repo.get_session(session_id=session_id)
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


### Repo Interfaces
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



### Repo Implementations    
class InMemoryWorkshopRepo(WorkshopRepo):
    
    def __init__(self, workshops) -> None:
        self.workshops = {workshop['id']: workshop for workshop in workshops}
        
    def list_workshops(self) -> Set[str]:
        return set(str(record['id']) for record in self.workshops.values())
        
    def get_workshop(self, workshop_id: str) -> PlannedWorkshopDTO:
        record = self.workshops[workshop_id]
        workshop = PlannedWorkshopDTO(
            id=record['id'], 
            name=record['name'], 
            description=record['description'],
            planned_start=record['planned_start'],
            planned_end=record['planned_end'],
            session_ids=[session['id'] for session in record['sessions']],
        )
        return workshop
    
    def get_session(self, session_id: str) -> PlannedSession:
        session_record = self._find_session_record(workshop_entries=self.workshops, session_id=session_id)    
        return PlannedSession(
            id=str('aa'), 
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
        
    