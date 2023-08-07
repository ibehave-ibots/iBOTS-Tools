from abc import ABC, abstractmethod
from typing import List
from .entities import Registrant


class ContactInfoController(ABC):
    @abstractmethod
    def get_contact_info(self, registrants: List[Registrant]):
        ...
