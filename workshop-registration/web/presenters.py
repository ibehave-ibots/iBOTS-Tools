from __future__ import annotations
from dataclasses import dataclass

from typing import List

from app import ListRegistrantPresenter, RegistrantSummary, ListWorkshopsPresenter, WorkshopRegistrationSummary
from web.view_model import AppState, ViewModel


@dataclass
class RegistrantPresenter(ListRegistrantPresenter):
    """
    Updates the state of the application with an updated ViewModel.
    """
    state: AppState

    def show(self, registrants: List[RegistrantSummary]) -> None:
        old_model: ViewModel = self.state.data
        new_model = old_model.update_registrant_table(registrants=[r.to_dict() for r in registrants])
        self.state.data = new_model

    def show_update(self, registrant: RegistrantSummary) -> None:
        old_model: ViewModel = self.state.data
        new_model = old_model.set_registration_status(id=registrant.id, status=registrant.status)
        self.state.data = new_model


@dataclass
class WorkshopPresenter(ListWorkshopsPresenter):
    state: AppState

    def show(self, upcoming_workshops: list[WorkshopRegistrationSummary]) -> None:
        old_model = self.state.data
        new_model = old_model.set_workshop_ids(ids=[w.id for w in upcoming_workshops])
        self.state.data = new_model

        