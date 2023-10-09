import os
import io
from contextlib import redirect_stdout
from typing import List
from itertools import accumulate
from app import AttendancePresenter, AttendanceSummary
#from app.attendance_presenter import AttendancePresenter, AttendanceSummary

class SpreadsheetAttendancePresenter(AttendancePresenter):

    def show(self, attendance_summaries: List[AttendanceSummary]) -> None:
        table_width=35
        
        all_sessions=[]
        for a in attendance_summaries: all_sessions.extend(list(a.hours_per_session.keys()))
        all_sessions = sorted(set(all_sessions))

        #header = "Name, email, "
        #header += ', '.join(all_sessions)
        #for c in header.split(','): 
        #    c+= ' '* (table_width- len(c))
        #header = ','.join(c)
        #print(header)
        header_cols = ["Name", "email"] + all_sessions
        for idx, c in enumerate(header_cols):
           c_spaced = c+ ' '* (table_width- len(c))

           header_cols[idx] = c_spaced
        header = ','.join(header_cols)
        print(header)

        for attendance_summary in attendance_summaries:
            #line = f"{attendance_summary.name}, {attendance_summary.email}, "
            #attendance_values = ', '.join(map( lambda x: f"{attendance_summary.hours_per_session[x]:.2f}", all_sessions))
            #line_cols = line+ attendance_values
            line_cols = [attendance_summary.name, attendance_summary.email]
            line_cols.extend(list([f"{attendance_summary.hours_per_session[x]:.2f}" for x in all_sessions]))
            for idx, c in enumerate(line_cols):
                c_spaced = c+ ' '* (table_width- len(c))
                line_cols[idx] = c_spaced
                line_spaced = ','.join(line_cols)
            print(line_spaced)

        
    def show_update(self, attendance_summary: AttendanceSummary) -> None:
        ...

    def write_csv(self, attendance_summaries: List[AttendanceSummary], output_filename: str) -> None:
        
        string_IO = io.StringIO()
        with redirect_stdout(string_IO): self.show(attendance_summaries)
        out = string_IO.getvalue()

        with open(output_filename, 'w') as f: f.write(out)
