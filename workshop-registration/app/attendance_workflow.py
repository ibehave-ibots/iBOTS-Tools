from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from .attendancerepo import AttendanceRepo
from .attendance_presenter import AttendancePresenter, AttendanceSummary


@dataclass(frozen=False)
class AttendanceWorkflow:
    attendance_repo: AttendanceRepo
    presenter: AttendancePresenter
    
    def create_attendance_summary(self, workshop_id: str) -> None:
        attendance_records = self.attendance_repo.get_attendance_records(workshop_id=workshop_id)
        unique_emails, idx = np.unique([a.email for a in attendance_records], return_index=True)
        emails = unique_emails[np.argsort(idx)]
        attendance_summaries: List[AttendanceSummary] = [] 
        for email in emails:
            attendance_records_one_person = list(filter(lambda x: x.email == email, attendance_records))
            attendance_records_one_person = list(sorted(attendance_records_one_person, key=lambda x: x.session))
            hours_per_session: Dict[str, float] = defaultdict(float)
            for attendance_record in attendance_records_one_person:
                attendance_time = (attendance_record.departed - attendance_record.arrived).seconds/3600.
                hours_per_session[attendance_record.session] = attendance_time    
            attendance_summary = AttendanceSummary(
                name=attendance_record.name,
                email=attendance_record.email,
                hours_per_session=hours_per_session,
            )
            attendance_summaries.append(attendance_summary)
        self.presenter.show(attendance_summaries=attendance_summaries)