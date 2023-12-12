from behave import given, when, then
from datetime import datetime
from app import AttendanceRecord
from external.zoom_api import ZoomAttendee

@given(u'participants attended workshop 1 with the following events')
def step_impl(context):
    zoom_attendees = []
    for row in context.table:
        zoom_attendee = ZoomAttendee(
                name=row["Name"],
                user_email=row["Email"],
                session=row["Session"],#.split("Day")[-1],
                join_time=f"2023-10-01T{row['Arrived']}:00Z",
                leave_time=f"2023-10-01T{row['Departed']}:00Z",
            )
        zoom_attendees.append(zoom_attendee)
    context.attendance_repo.get_attendees.return_value = zoom_attendees

@when(u'the attendance table is built for workshop 1')
def step_impl(context):
    context.app.create_attendance_summary(workshop_id="12345")

@then(u'the user sees')
def step_impl(context):
    attendance_summaries = context.attendance_presenter.show.call_args[1]['attendance_summaries']
    for observed, expected in zip(attendance_summaries, context.table):
        assert observed.name == expected['Name'], f"{observed} {expected}"
        assert observed.email == expected['Email'], f"{observed} {expected}"
        assert str(observed.hours_per_session['Day1']) == expected['Day1'], f"assertion3 {expected}"
        assert str(observed.hours_per_session['Day2']) == expected['Day2'], f"assertion4 {expected}"
