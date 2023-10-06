import os
from typing import List
import io
from contextlib import redirect_stdout
from app import AttendancePresenter, AttendanceSummary
#from app.attendance_presenter import AttendancePresenter, AttendanceSummary

class Spreadsheet_attendancepresenter(AttendancePresenter):

    def show(self, attendance_summaries: List[AttendanceSummary]) -> None:

        all_sessions=[]
        for a in attendance_summaries: all_sessions.extend(list(a.hours_per_session.keys()))
        all_sessions = sorted(set(all_sessions))

        header="Name, email,"
        for session in all_sessions: header += session + ', '
        print(header)

        for attendance_summary in attendance_summaries:
            line = f"{attendance_summary.name}, {attendance_summary.email},"
            for session in all_sessions:
                line += str(attendance_summary.hours_per_session[session]) + ', '
            print(line)

        
    def show_update(self, attendance_summary: AttendanceSummary) -> None:
        ...

    def write_csv(self, attendance_summaries: List[AttendanceSummary], output_filename: str) -> None:
         
        string_IO = io.StringIO()
        with redirect_stdout(string_IO):
            self.show(attendance_summaries)
        out = string_IO.getvalue()

        with open(output_filename, 'w') as f: f.write(out)
