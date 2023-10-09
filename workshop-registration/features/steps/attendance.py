from behave import given, when, then
from datetime import datetime
from app import AttendanceRecord

@given(u'participants attended workshop 1 with the following events')
def step_impl(context):
    for row in context.table:
        attendance_record = AttendanceRecord(
            workshop_id="12345",
            name=row["Name"],
            email=row["Email"],
            session=row["Session"],
            arrived=datetime.strptime(row["Arrived"], "%H:%M"),
            departed=datetime.strptime(row["Departed"], "%H:%M"),
        )
        context.attendance_repo.add_attendance_record(attendance_record)


@when(u'the attendance table is built for workshop 1')
def step_impl(context):
    context.app.create_attendance_summary(workshop_id="12345")

@then(u'the user sees')
def step_impl(context):
    attendance_summaries = context.attendance_presenter.show.call_args[1]['attendance_summaries']
    for observed, expected in zip(attendance_summaries, context.table):
        assert observed.name == expected['Name'], f"{observed} {expected}"
        assert observed.email == expected['Email'], f"{observed} {expected}"
        assert str(observed.hours_per_session["Day1"]) == expected['Day1'], f"assertion3 {expected}"
        assert str(observed.hours_per_session["Day2"]) == expected['Day2'], f"assertion4 {expected}"
