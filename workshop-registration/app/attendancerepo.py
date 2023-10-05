from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AttendanceRecord:
    name: str 
    email: str 
    session: str 
    arrived: datetime 
    departed: datetime
    
    
    
class AttendanceRepo(ABC):
    
    @abstractmethod
    def add_attendance_record(self, attendance_record: AttendanceRecord):
        ...