from dataclasses import dataclass
from .attendancerepo import AttendanceRepo
from .attendance_presenter import AttendancePresenter



@dataclass(frozen=False)
class AttendanceWorkflow:
    attendance_repo: AttendanceRepo
    presenter: AttendancePresenter
    
    def create_attendance_summary(self):
        # goal: create a list of AttendanceSummary
        attendance_records = self.attendance_repo.attendance_records
        emails = set([a.email for a in attendance_records])
        sessions = set([a.session for a in attendance_records])
        # initialize attendance summary object
        for attendance_record in attendance_records:
            attendance_time = (attendance_record.departed - attendance_record.arrived).to_hours()
            # update appropriate attendance summary object
            
            
                
        
        