from datetime import datetime
from .attendance_workflows import Attendee

attendee1 = Attendee(
    name='abc',
    email='abc@ibehave.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=1, minute=1, second=59, microsecond=0, tzinfo=None))

attendee2 = Attendee(
    name='def',
    email='def@gmail.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=0, minute=15, second=0, microsecond=0, tzinfo=None))

attendee3 = Attendee(
    name='ghi',
    email='ghi@xyz.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    join_end = datetime(2023, 7, 7, hour=0, minute=20, second=0, microsecond=0, tzinfo=None))

attendee4 = Attendee(
    name='ghi',
    email='ghi@xyz.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=25, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=1, minute=0, second=0, microsecond=0, tzinfo=None))

attendee5 = Attendee(
    name='jkl',
    email='ghi@xyz.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=0, minute=20, second=0, microsecond=0, tzinfo=None))

attendee6 = Attendee(
    name='jkl',
    email='ghi@xyz.com',
    join_start=datetime(2023, 7, 7, hour=0, minute=25, second=0, microsecond=0, tzinfo=None),
    join_end=datetime(2023, 7, 7, hour=0, minute=30, second=0, microsecond=0, tzinfo=None))
