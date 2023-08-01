from abc import ABC, abstractmethod
from typing import Set


class WorkshopRepo(ABC):

    @abstractmethod
    def list_workshops(self) -> Set[str]: ...