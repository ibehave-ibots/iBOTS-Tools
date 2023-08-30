from collections import defaultdict
from dataclasses import dataclass, field
from typing import Literal, NamedTuple
import uuid


@dataclass(frozen=True)
class WorkshopRecord:
    link: str
    title: str
    date: str
    capacity: int
    id: str = field(default_factory= lambda: str(uuid.uuid4()))


@dataclass(frozen=True)
class RegistrationRecord:
    workshop_id: str
    name: str
    status: Literal['approved', 'rejected', 'waitlisted'] 
    id: str = field(default_factory= lambda: str(uuid.uuid4()))


@dataclass(frozen=True)
class WorkshopRegistrationSummary:
    link: str
    title: str
    date: str
    capacity: int
    id: str
    num_approved: int
    num_waitlisted: int
    num_rejected: int
    num_free_spots: int


@dataclass
class AppModel:
    upcoming_workshops: list[WorkshopRegistrationSummary] = field(default_factory=list)

class WorkshopRepo:
    def __init__(self) -> None:
        self.workshops = []
        self.registrations = defaultdict(list)

    def add_workshop(self, workshop: WorkshopRecord):
        self.workshops.append(workshop)

    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        return self.workshops
    
    def add_registration(self, registration: RegistrationRecord):
        self.registrations[registration.workshop_id].append(registration)

    def get_registrations(self, workshop_id: str):
        return self.registrations[workshop_id]

    

class App(NamedTuple):
    workshop_repo: WorkshopRepo
    model: AppModel

    def check_upcoming_workshops(self):
        upcoming_workshop_records = self.workshop_repo.get_upcoming_workshops()
        workshop_summaries = []
        for workshop in upcoming_workshop_records:
            registration_records = self.workshop_repo.get_registrations(workshop.id)
            num_approved = sum(reg.status == 'approved' for reg in registration_records)
            num_waitlisted = sum(reg.status == 'waitlisted' for reg in registration_records)
            num_rejected = sum(reg.status == 'rejected' for reg in registration_records)
            num_free_spots = workshop.capacity - num_approved


            workshop_summary = WorkshopRegistrationSummary(
                link = workshop.link,
                title = workshop.title,
                date = workshop.date,
                capacity = workshop.capacity,
                id = workshop.id,
                num_approved=num_approved,
                num_waitlisted=num_waitlisted,
                num_rejected=num_rejected,
                num_free_spots=num_free_spots,
            )
            workshop_summaries.append(workshop_summary)
        self.model.upcoming_workshops = workshop_summaries

