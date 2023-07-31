from __future__ import annotations
from typing import Set

from ..core.workflow import WorkshopRepo


class InMemoryWorkshopRepo(WorkshopRepo):
    
    def __init__(self, workshops) -> None:
        self.workshops = {workshop['id']: workshop for workshop in workshops}
        
    def list_workshops(self) -> Set[str]:
        return set(str(record['id']) for record in self.workshops.values())