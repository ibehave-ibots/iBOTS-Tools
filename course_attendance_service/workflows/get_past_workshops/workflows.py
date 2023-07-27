from __future__ import annotations
from abc import ABC, abstractmethod
from typing import NamedTuple, NewType

WorkshopID = NewType("WorkshopID", str)

class PastWorkshop(NamedTuple):
    id: WorkshopID
    name: str
    

class GetPastWorkshopWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    def get_workshop_details(self, workshop_id: WorkshopID) -> PastWorkshop:
        workshop = self.workshop_repo.get_workshop(workshop_id=workshop_id)
        return PastWorkshop(
            id=WorkshopID(workshop.id),
            name=workshop.name,
        )
        
        
class WorkshopDTO(NamedTuple):
    id: str
    name: str
        
        
class WorkshopRepo(ABC):
    
    @abstractmethod
    def get_workshop(self, workshop_id: str) -> WorkshopDTO:
        ...
        
        
class InMemoryWorkshopRepo(WorkshopRepo):
    
    def __init__(self, workshops):
        self.workshops = {w['id']: w for w in workshops}
    
    def get_workshop(self, workshop_id: str) -> WorkshopDTO:
        workshop = self.workshops[workshop_id]
        return WorkshopDTO(
            id=workshop['id'],
            name=workshop['name'],
        )