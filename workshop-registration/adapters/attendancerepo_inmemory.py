from typing import List, Sequence
from app import AttendanceRecord, AttendanceRepo

class InMemoryAttendanceRepo(AttendanceRepo):
    def __init__(self, workshop_id: str, attendance_records: Sequence[AttendanceRecord] = ()) -> None:
        self.workshop_id = workshop_id
        self.attendance_records: List[AttendanceRecord] = list()
        for ar in attendance_records:
            self.attendance_records.append(ar)
            
    def add_attendance_record(self, attendance_record: AttendanceRecord):
        self.attendance_records.append(attendance_record)
        
        