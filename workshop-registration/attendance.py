

# %%
import os
from external.zoom_api.zoom_oauth import OAuthGetToken
from adapters.attendance_summary_presenter_make_spreadsheet import SpreadsheetAttendancePresenter
from adapters.attendancerepo_zoom import ZoomAttendanceRepo
from datetime import time, datetime
from dataclasses import asdict
import pandas as pd


# %%
meeting_id = "869 0642 6337"

# %%
oauth_get_token = OAuthGetToken(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    account_id=os.environ["ACCOUNT_ID"],
)
repo = ZoomAttendanceRepo(oauth_get_token=oauth_get_token)
attendance_records = repo.get_attendance_records(workshop_id=meeting_id)

# %%
data = [asdict(attendance_record) for attendance_record in attendance_records]
df = pd.DataFrame(data=data)

# %%
df['date'] = df.arrived.dt.date
df['workshop_start'] = df.apply(lambda x: datetime.combine(x.date, time(hour= 8, minute=00)), axis = 1)
df['workshop_end'] = df.apply(lambda x: datetime.combine(x.date, time(hour= 11, minute=30)), axis = 1)


# %%
df["arrival_time_corrected"] = df["arrived"].dt.tz_localize(None).clip(lower=df["workshop_start"], upper=df["workshop_end"])
df["departure_time_corrected"] = df["departed"].dt.tz_localize(None).clip(lower=df["workshop_start"], upper=df["workshop_end"])
df["time_spent_corrected"] = (df['departure_time_corrected'] - df['arrival_time_corrected']).dt.total_seconds()/3600
df.groupby(["email", "date"]).time_spent_corrected.sum().unstack().round(1).style.background_gradient()
# %%
df[(df.email == "liyi3387@gmail.com") & (df.session == 'Day7')]

