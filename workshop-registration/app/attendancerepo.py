from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AttendanceRecord:
    workshop_id: str
    name: str 
    email: str 
    session: str 
    arrived: datetime 
    departed: datetime
    
    
    
class AttendanceRepo(ABC):
    
    @abstractmethod
    def get_attendance_records(self, workshop_id: str):
        ...
    
    @abstractmethod
    def add_attendance_record(self, attendance_record: AttendanceRecord):
        ...