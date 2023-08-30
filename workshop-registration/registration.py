from dataclasses import dataclass, field
from typing import NamedTuple


class Workshop(NamedTuple):
    id: str


@dataclass
class AppModel:
    upcoming_workshops: list[Workshop] = field(default_factory=list)

class WorkshopRepo:
    def __init__(self) -> None:
        self.workshops = []

    def add_workshop(self, workshop_id: str):
        self.workshops.append(Workshop(id=workshop_id))

    def get_upcoming_workshops(self) -> list[Workshop]:
        return self.workshops
    

class App(NamedTuple):
    workshop_repo: WorkshopRepo
    model: AppModel

    def check_upcoming_workshops(self):
        upcoming_workshops = self.workshop_repo.get_upcoming_workshops()
        self.model.upcoming_workshops = upcoming_workshops