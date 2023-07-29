from __future__ import annotations

from datetime import date, datetime
from typing import List, NamedTuple, NewType, Sequence



class Session(NamedTuple):
    id: str
    scheduled_start: datetime
    scheduled_end: datetime
   
   
    
WorkshopID = NewType("WorkshopID", str)
    
class Workshop(NamedTuple):
    id: WorkshopID
    name: str
    description: str
    scheduled_start: date
    scheduled_end: date
    sessions: List[Session]
    topics: Sequence[str]