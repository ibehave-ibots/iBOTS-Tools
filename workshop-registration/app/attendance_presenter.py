from abc import ABC, abstractmethod
from typing import Dict, List, NamedTuple

class AttendanceSummary(NamedTuple):
    name: str
    email: str
    hours_per_session: Dict[str, float]


class AttendancePresenter(ABC):
    
    @abstractmethod
    def show(self, attendance_summaries: List[AttendanceSummary]) -> None:
        ...

