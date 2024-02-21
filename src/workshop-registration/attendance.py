import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from datetime import time, datetime
from dataclasses import asdict
from external.zoom_api.zoom_oauth import OAuthGetToken
from adapters.attendancerepo_zoom import ZoomAttendanceRepo
from merge_timerange import merge_timeranges



def calculate_attendance(meeting_id):
    load_dotenv()
    oauth_get_token = OAuthGetToken(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        account_id=os.environ["ACCOUNT_ID"],
    )
    repo = ZoomAttendanceRepo(oauth_get_token=oauth_get_token)
    attendance_records = repo.get_attendance_records(workshop_id=meeting_id)

    data = [asdict(attendance_record) for attendance_record in attendance_records]
    df = pd.DataFrame(data=data)

    df['date'] = df.arrived.dt.date
    df['workshop_start'] = df.apply(lambda x: datetime.combine(x.date, time(hour= 9, minute=30)), axis = 1)
    df['workshop_end'] = df.apply(lambda x: datetime.combine(x.date, time(hour=18, minute=00)), axis = 1)

    df["arrival_time_corrected"] = df["arrived"].dt.tz_localize(None).clip(lower=df["workshop_start"], upper=df["workshop_end"])
    df["departure_time_corrected"] = df["departed"].dt.tz_localize(None).clip(lower=df["workshop_start"], upper=df["workshop_end"])

    res_list = []
    for n, df_n in df.groupby(["email", "date"]):
        email = n[0]
        workshop_day = n[1]
        time_ranges_input = [(a,b) for a,b in zip(df_n["arrival_time_corrected"].values, df_n["departure_time_corrected"].values)]
        merged_timeranges = merge_timeranges(time_ranges_input)
        total_time_hrs = sum( [ ((mt[1]-mt[0]).astype(np.int64)*1e-9/3600) for mt in merged_timeranges ])
        name = df_n['name'].unique()[0]
        res_list.append({'name':name, 'email':email,'day':workshop_day, 'time_hrs':total_time_hrs })


    df_res = pd.DataFrame(res_list)
    df_res = df_res.set_index(['email','name'])
    df_wide = df_res.pivot( columns='day', values='time_hrs').fillna(0.0).round(1).reset_index()

    days = sorted(df_res.day.unique())
    df_wide.rename(columns={ x: "Day%s"%(i+1) for x,i in zip(days, range(len(days)))})

    cols = df_wide.columns.tolist()
    return df_wide[['name','email']+ cols[2:]]



if __name__ == "__main__":    
    meeting_id = "833 3035 7443"
    #meeting_id = input("Type meeting id: ")

    print("Calculating attendance for meeting id %s"%meeting_id)
    df = calculate_attendance(meeting_id)
    file_name = "attendance_report-%s.csv"%meeting_id.replace(" ","")
    print('Saving to %s'%file_name)
    df.to_csv(file_name , index=False, )