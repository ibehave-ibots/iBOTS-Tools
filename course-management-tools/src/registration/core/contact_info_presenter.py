from abc import ABC, abstractmethod
from typing import List
from .entities import Registrant


class ContactInfoPresenter(ABC):
    @abstractmethod
    def display_contact_info(self, registrants: List[Registrant]) -> None:
        ...
