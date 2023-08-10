from abc import ABC, abstractmethod
from typing import List
from .entities import Registrant


class ContactInfoFormatter(ABC):
    @abstractmethod
    def format_contact_info(self, registrants: List[Registrant]) -> str:
        ...
