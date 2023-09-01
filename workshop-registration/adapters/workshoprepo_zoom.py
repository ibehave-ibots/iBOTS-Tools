from dataclasses import dataclass
import yaml
from external.zoom_api import ZoomAPI, RecurringMeetingSummary
from app import WorkshopRepo, WorkshopRecord

@dataclass(frozen=True)
class ZoomWorkshopRepo(WorkshopRepo):
    zoom_api: ZoomAPI
    user_id: str

    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        meeting_summaries = self.zoom_api.get_meetings(user_id=self.user_id)
        workshop_records = []
        for meeting_summary in meeting_summaries:
            match meeting_summary:
                case RecurringMeetingSummary():
                    meeting = self.zoom_api.get_meeting(meeting_id=str(meeting_summary.id))
                    metadata = yaml.load(meeting.agenda.split("---")[1], Loader=yaml.Loader)
                    workshop_record = WorkshopRecord(
                        link=meeting.registration_url,
                        title=meeting_summary.topic,
                        date=meeting_summary.start_time[:10],
                        capacity=metadata["Capacity"],
                        id=str(meeting_summary.id),
                    )
                    workshop_records.append(workshop_record)
                case _:
                    continue
        return workshop_records