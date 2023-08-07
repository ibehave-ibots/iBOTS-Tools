# %%
import os
import requests
from course_attendance_service.course_attendance_service import api, zoom_integration
from course_attendance_service.course_attendance_service.zoom_integration import (
    create_access_token,
    get_meetings_of_member,
)

# %%
response = create_access_token()
access_token = response["access_token"]
os.environ["access_token"] = response["access_token"]

# %% get groups
url = "https://api.zoom.us/v2/groups"
header = {"Authorization": f"Bearer {access_token}"}
response = requests.get(url, headers=header)
groups = response.json()
groups
# %%
os.environ["GROUP_ID"] = "RRj_xud1S-yImYnUcbV6fg"

# %% get group members
url = f"https://api.zoom.us/v2/groups/{os.environ['GROUP_ID']}/members"
header = {"Authorization": f"Bearer {access_token}"}
response = requests.get(url, headers=header)
members = response.json()
members
# %% set the user ID
os.environ["USER_ID"] = "lo1pQlI_T5a72HyMCzFGpA"

# %% get a list of all meetings
meetings_report = get_meetings_of_member(access_token)

# %% get a list of all meeting ids for a specific user (optional: within a time range)
api.list_meeting_ids(access_token) #, from_date='2023-07-18', to_date='2023-07-18')

# %% Find a meeting that I attended
meetings = meetings_report["meetings"]
for meeting in meetings:
    host_id = meeting["host_id"]
    if host_id == os.environ["USER_ID"]:
        print(meeting)

# %%
api.list_meeting_ids(access_token, from_date='2023-07-11', to_date='2023-07-11')
# %%


# %% Get a list of registrants for a specific meeting
meeting_id = 83847307377
url = f"https://api.zoom.us/v2/meetings/{meeting_id}/registrants"
header = {"Authorization": f"Bearer {access_token}"}
params = {
    "status": "pending", # "pending", "approved", "denied"
    "page_size": 100,
    }
response = requests.get(url, params=params, headers=header)
registrants = response.json()
registrants
# %%
meeting_id = "83847307377"
registrants_report = zoom_integration.get_registrants(access_token, meeting_id, status=["approved", "denied"]) #"["approved", "denied"])
registrants_report

# %%
meeting_id = "83847307377"
registrants_count = registrants_count = zoom_integration.get_registrants_count_all_statuses(access_token, meeting_id)
registrants_count

# %%
