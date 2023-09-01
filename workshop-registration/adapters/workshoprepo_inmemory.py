from app import WorkshopRepo, WorkshopRecord


class InMemoryWorkshopRepo(WorkshopRepo):
    def __init__(self) -> None:
        self.workshops = []

    def add_workshop(self, workshop: WorkshopRecord):
        self.workshops.append(workshop)

    def get_upcoming_workshops(self) -> list[WorkshopRecord]:
        return self.workshops
