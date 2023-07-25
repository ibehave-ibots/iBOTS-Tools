from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
import random
from typing import List, NamedTuple, NewType, Set
from unittest.mock import Mock

############# TESTS

def test_list_all_workshops_ids():
    random.seed(42)
    given_workshops = [
        {'id': random.choice('abcdefghijk')},
        {'id': random.choice('abcdefghijk')}
    ]
    
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    workflows = GetWorkshopWorkflows(workshop_repo=repo)
    
    workshop_ids = workflows.list_all_workshops()
    assert workshop_ids == {given_workshops[0]['id'], given_workshops[1]['id']}
    
    
    
def test_get_workshop_details():
    random.seed(42)
    given_workshops = [
        {
            'id': random.choice('abcdefghijk'), 
            'name': random.choice(['IntroPy', 'IntroR', 'IntroMat']),
            'description': ''.join(random.choices('ABCDEFGHIJK', k=3)),
            'planned_start': datetime(2023, 1, 18, 9, 30),
            'planned_end': datetime(2023, 1, 21, 17, 45)
            
        },
    ]
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    workflows = GetWorkshopWorkflows(workshop_repo=repo)
    
    workshop = workflows.get_workshop_details(workshop_id=given_workshops[0]['id'])
    assert workshop.name == given_workshops[0]['name']
    assert workshop.description == given_workshops[0]['description']
    assert workshop.planned_start == given_workshops[0]['planned_start']
    assert workshop.planned_end == given_workshops[0]['planned_end']
    
    
    
    
    
    
    
########## SRC    

WorkshopId = NewType('WorkshopId', str)

class Workshop(NamedTuple):
    id: WorkshopId
    name: str
    description: str
    planned_start: datetime
    planned_end: datetime
    

class WorkshopRepo(ABC):
    
    @abstractmethod
    def list_workshops(self) -> Set[WorkshopId]: ...
    
    @abstractmethod
    def get_workshop_details(self, workshop_id: WorkshopId) -> Workshop: ...


class GetWorkshopWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    
    def list_all_workshops(self) -> List[WorkshopId]:
        return self.workshop_repo.list_workshops()
    
    def get_workshop_details(self, workshop_id: str):
        workshop = self.workshop_repo.get_workshop_details(workshop_id=workshop_id)
        return workshop
    
    
    
class InMemoryWorkshopRepo(WorkshopRepo):
    
    def __init__(self, workshops) -> None:
        self.workshops = {workshop['id']: workshop for workshop in workshops}
        
    def list_workshops(self) -> Set[WorkshopId]:
        return set(WorkshopId(entry['id']) for entry in self.workshops.values())
        
    def get_workshop_details(self, workshop_id: WorkshopId) -> Workshop:
        entry = self.workshops[workshop_id]
        workshop = Workshop(
            id=entry['id'], 
            name=entry['name'], 
            description=entry['description'],
            planned_start=entry['planned_start'],
            planned_end=entry['planned_end'],
        )
        return workshop
    
    