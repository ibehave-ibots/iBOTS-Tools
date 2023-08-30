from dataclasses import dataclass, field
from typing import NamedTuple
import uuid

@dataclass(frozen=True)
class WorkshopRecord:
    link: str
    title: str
    date: str
    id: str = field(default_factory= lambda: str(uuid.uuid4()))


@dataclass
class AppModel:
    upcoming_workshops: list[WorkshopRecord] = field(default_factory=list)

class WorkshopRepo:
    def __init__(self) -> None:
        self.workshops = []

    def add_workshop(self, workshop: WorkshopRecord):
        self.workshops.append(workshop)

    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        return self.workshops
    

class App(NamedTuple):
    workshop_repo: WorkshopRepo
    model: AppModel

    def check_upcoming_workshops(self):
        upcoming_workshops = self.workshop_repo.get_upcoming_workshops()
        self.model.upcoming_workshops = upcoming_workshops