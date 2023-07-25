from __future__ import annotations
from abc import ABC, abstractmethod
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
            
        },
    ]
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    workflows = GetWorkshopWorkflows(workshop_repo=repo)
    
    workshop = workflows.get_workshop_details(workshop_id=given_workshops[0]['id'])
    assert workshop.name == given_workshops[0]['name']
    assert workshop.description == given_workshops[0]['description']
    
    
    
    
    
    
    
########## SRC    

WorkshopId = NewType('WorkshopId', str)

class Workshop(NamedTuple):
    id: WorkshopId
    name: str
    description: str


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
        workshop_ids = []
        for entry in self.workshops.values():
            workshop_id = WorkshopId(entry['id'])
            workshop_ids.append(workshop_id)
        return set(workshop_ids)
        
    def get_workshop_details(self, workshop_id: WorkshopId) -> Workshop:
        entry = self.workshops[workshop_id]
        return Workshop(id=entry['id'], name=entry['name'], description=entry['description'])
    