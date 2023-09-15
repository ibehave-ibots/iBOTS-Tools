from typing import List
from app import WorkshopRepo, WorkshopRecord


class InMemoryWorkshopRepo(WorkshopRepo):
    def __init__(self) -> None:
        self.workshops: List[WorkshopRecord] = []

    def add_workshop(self, workshop: WorkshopRecord):
        self.workshops.append(workshop)

    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        return self.workshops
