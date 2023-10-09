from typing import List

import pandas as pd
from app import AttendancePresenter, AttendanceSummary


class PandasAttendancePresenter(AttendancePresenter):
    @staticmethod
    def create_pandas_dataframe_from_attendance_summary(attendance_summaries: List[AttendanceSummary]) -> pd.DataFrame:
        unique_sessions = []
        for registrant in attendance_summaries:
            sessions = list(registrant.hours_per_session.keys())
            unique_sessions.extend(sessions)
        unique_sessions = list(set(unique_sessions))
        df = pd.DataFrame(columns=["Name", "Email"] + unique_sessions)
        for registrant in attendance_summaries:
            row = {"Name": registrant.name, "Email": registrant.email}
            for unique_session in unique_sessions:
                hours_per_session = registrant.hours_per_session.get(unique_session, 0.)
                row[unique_session] = f"{hours_per_session:.2f}"
            df.loc[len(df)] = row
        return df
    
    def show(self, attendance_summaries: List[AttendanceSummary]) -> None:
        df = self.create_pandas_dataframe_from_attendance_summary(attendance_summaries)
        print(df.to_string())

    def write_csv(self, attendance_summaries: List[AttendanceSummary], output_filename: str) -> None:
        df = self.create_pandas_dataframe_from_attendance_summary(attendance_summaries)
        df.to_csv(f"{output_filename}.csv")
