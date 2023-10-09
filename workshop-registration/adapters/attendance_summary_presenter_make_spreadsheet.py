import os
import io
from contextlib import redirect_stdout
from typing import List
from itertools import accumulate
from app import AttendancePresenter, AttendanceSummary

def _add_spaces(input_columns:List[str], col_width:int) -> List[str]:
        output_columns=['']*len(input_columns)
        for idx, c in enumerate(input_columns):
           c_spaced = c+ ' '* (col_width- len(c))

           output_columns[idx] = c_spaced
        output_columns = ', '.join(output_columns)
        return output_columns

class SpreadsheetAttendancePresenter(AttendancePresenter):

    def show(self, attendance_summaries: List[AttendanceSummary]) -> None:
        column_width=40
        
        all_sessions=[]
        for a in attendance_summaries: all_sessions.extend(list(a.hours_per_session.keys()))
        all_sessions = sorted(set(all_sessions))

        header_cols = ["Name", "email"] + all_sessions
        header = _add_spaces(header_cols, column_width)
        print(header)

        for attendance_summary in attendance_summaries:
            line_cols = [attendance_summary.name, attendance_summary.email]
            line_cols.extend(list([f"{attendance_summary.hours_per_session[x]:.2f}" for x in all_sessions]))
            line= _add_spaces(line_cols, column_width)
            print(line)

        
    def show_update(self, attendance_summary: AttendanceSummary) -> None:
        ...

    def write_csv(self, attendance_summaries: List[AttendanceSummary], output_filename: str) -> None:
        
        string_IO = io.StringIO()
        with redirect_stdout(string_IO): self.show(attendance_summaries)
        out = string_IO.getvalue()

        with open(output_filename, 'w') as f: f.write(out)
