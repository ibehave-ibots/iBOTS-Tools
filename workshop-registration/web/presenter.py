from __future__ import annotations
from dataclasses import dataclass

from typing import List

from app import ListRegistrantPresenter, RegistrantSummary
from web.model import AppState, AppModel


@dataclass
class Presenter(ListRegistrantPresenter):
    state: AppState

    def show(self, registrants: List[RegistrantSummary]) -> None:
        old_model: AppModel = self.state.model
        new_model = old_model.update_registrant_table(registrants=[r.to_dict() for r in registrants])
        self.state.model = new_model

    def show_update(self, registrant: RegistrantSummary) -> None:
        old_model: AppModel = self.state.model
        new_model = old_model.set_registration_status(id=registrant.id, status=registrant.status)
        self.state.model = new_model


