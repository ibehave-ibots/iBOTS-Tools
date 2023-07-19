import streamlit as st
from course_attendance_service import api
from course_attendance_service import zoom_integration


def enter_meeting_id():
    return int(st.text_input(label="Enter meeting ID",value='Meeting id'))

def display_participant_details(access_token,meeting_id):
    # 87870712552
    details= api.get_attendance_report(token=token_data, meeting_id=meeting_id)
    participants = {
        'Name':details.names,
        'Duration (minute)':details.durations_min,
        'Email address':details.emails
    }
    st.dataframe(participants)

def display_meeting_details(token_data, meeting_id):
    details = api.get_meeting_details(token_data, meeting_id)

    meeting_details = {
    'title': details.title,
    'description': details.description,
    'date':details.date,
    'planned_start_time':details.planned_start_time,
    'planned_end_time':details.planned_end_time,
    'session_ids':details.session_ids}

    st.dataframe(meeting_details)


# Refactor to a module
token_data = zoom_integration.create_access_token()['access_token']

st.title(body=":blue[Zoom] Meetings Analytics")
st.caption(body="...for your zoom courses")

meeting_id = enter_meeting_id()
display_participant_details(token_data,meeting_id)
display_meeting_details(token_data, meeting_id)