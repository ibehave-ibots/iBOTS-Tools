from collections import defaultdict
from typing import Dict, List, Sequence
from app import AttendanceRecord, AttendanceRepo

class InMemoryAttendanceRepo(AttendanceRepo):
    def __init__(self, attendance_records: Sequence[AttendanceRecord] = ()) -> None:
        self.attendance_records: Dict[str, List[AttendanceRecord]] = defaultdict(list)
        for ar in attendance_records:
            self.attendance_records[ar.workshop_id].append(ar)
    
    def get_attendance_records(self, workshop_id: str) -> List[AttendanceRecord]:
        return self.attendance_records[workshop_id]
    
    def add_attendance_record(self, attendance_record: AttendanceRecord) -> None:
        self.attendance_records[ attendance_record.workshop_id].append(attendance_record)
        
        