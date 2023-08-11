from datetime import datetime
from typing import List, NamedTuple


class AttendeeInstance(NamedTuple):
    name: str
    email: str
    join_start: datetime
    join_end: datetime

    @property
    def duration(self):
        return (self.join_end - self.join_start).total_seconds()
    
# unique email and all different instances of same attendee in a session
class AttendeeReport(NamedTuple):
    email: str
    attendee_instances: List[AttendeeInstance]
    attendance: bool
    total_duration: float

# individual session of a workshop with a session id. List of all attendees (including duplicates) 
class Session(NamedTuple):
    session_id: str
    start_time: datetime
    end_time: datetime
    attendees: List[AttendeeInstance]

    @property
    def duration(self):
        return (self.end_time - self.start_time).total_seconds()
    