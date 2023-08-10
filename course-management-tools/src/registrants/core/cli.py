from abc import ABC, abstractmethod


class CLI(ABC):
    @abstractmethod
    def get_input(self):
        ...
