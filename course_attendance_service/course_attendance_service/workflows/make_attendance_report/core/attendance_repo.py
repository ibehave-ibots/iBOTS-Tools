# INTERFACE (CONTRACT)
from abc import abstractmethod, ABC
from .entities import Session


class AttendanceRepo(ABC):
    @abstractmethod
    def get_session_details(self, session_id: str) -> Session:
        ...
