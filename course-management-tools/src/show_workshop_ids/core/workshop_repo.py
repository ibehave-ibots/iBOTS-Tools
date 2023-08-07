from abc import ABC, abstractmethod
from typing import List


class WorkshopRepo(ABC):

    @abstractmethod
    def list_workshops(self) -> List[str]: ...