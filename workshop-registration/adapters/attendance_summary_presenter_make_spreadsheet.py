import os
import io
from contextlib import redirect_stdout
from typing import List
from itertools import accumulate
from app import AttendancePresenter, AttendanceSummary
#from app.attendance_presenter import AttendancePresenter, AttendanceSummary

class SpreadsheetAttendancePresenter(AttendancePresenter):

    def show(self, attendance_summaries: List[AttendanceSummary]) -> None:

        all_sessions=[]
        for a in attendance_summaries: all_sessions.extend(list(a.hours_per_session.keys()))
        all_sessions = sorted(set(all_sessions))

        header="Name, email,"
        for session in all_sessions: header += session + ', '
        print(header)


        for attendance_summary in attendance_summaries:
            line = f"{attendance_summary.name}, {attendance_summary.email}, "
            attendance_values=''.join(map( lambda x: str(attendance_summary.hours_per_session[x]) + ', ', all_sessions))
            print(line+ attendance_values)

        
    def show_update(self, attendance_summary: AttendanceSummary) -> None:
        ...

    def write_csv(self, attendance_summaries: List[AttendanceSummary], output_filename: str) -> None:
        
        string_IO = io.StringIO()
        with redirect_stdout(string_IO): self.show(attendance_summaries)
        out = string_IO.getvalue()

        with open(output_filename, 'w') as f: f.write(out)
