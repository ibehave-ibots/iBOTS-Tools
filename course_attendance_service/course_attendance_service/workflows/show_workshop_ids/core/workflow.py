from __future__ import annotations

from typing import List, NamedTuple

from .workshop_repo import WorkshopRepo
from .entities import WorkshopID


class ListWorkshopsWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    def list_all_workshops(self) -> List[WorkshopID]:
        return self.workshop_repo.list_workshops()
    
    
    
    

