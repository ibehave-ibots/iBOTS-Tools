from pprint import pprint

from app.list_workshops_app import ListWorkshopsPresenter, WorkshopRegistrationSummary


class PPrintListWorkshopPresenter(ListWorkshopsPresenter):

    def show(self, upcoming_workshops: list[WorkshopRegistrationSummary]) -> None:
        for workshop in upcoming_workshops:
            pprint(workshop)