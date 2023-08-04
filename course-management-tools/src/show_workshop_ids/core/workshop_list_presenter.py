from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple, List


class WorkshopListPresenter(ABC):

    @abstractmethod
    def show(self, workshops: List[WorkshopData]) -> None:
        ...
        
        
        
class WorkshopData(NamedTuple):
    id: str