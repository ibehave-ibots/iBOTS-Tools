from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, NamedTuple, Set

from .entities import WorkshopID




class PlannedWorkshopWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    def list_all_workshops(self) -> List[WorkshopID]:
        return self.workshop_repo.list_workshops()
    
    
    
    
class WorkshopRepo(ABC):
    
    @abstractmethod
    def list_workshops(self) -> Set[str]: ...

