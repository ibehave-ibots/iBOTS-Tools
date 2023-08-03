from abc import ABC, abstractmethod
from typing import Any, List
from .entities import Registrant


class RegistrantsRepo(ABC):
    @abstractmethod
    def get_list_of_registrants(self, workshop_id: Any) -> List[Registrant]:
        ...
