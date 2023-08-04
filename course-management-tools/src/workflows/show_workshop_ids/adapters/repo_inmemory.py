from __future__ import annotations
from typing import List, Set

from ..core.workshop_repo import WorkshopRepo


class InMemoryWorkshopRepo(WorkshopRepo):
    
    def __init__(self, workshops) -> None:
        self.workshops = {workshop['id']: workshop for workshop in workshops}
        
    def list_workshops(self) -> List[str]:
        return [str(record['id']) for record in self.workshops.values()]