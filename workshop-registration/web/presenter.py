from __future__ import annotations
from dataclasses import dataclass, field, replace

from typing import Any, Dict, List, NamedTuple

import pandas as pd

from web.signal import Signal
from app import ListRegistrantPresenter, RegistrantSummary

@dataclass(frozen=True)
class AppModel:
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(
        columns=('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state'),
        dtype=str,
    ))

    def replace(self, **kwargs) -> AppModel:
        return replace(self, **kwargs)



class Controller:
    updated: Signal

    def __init__(self, model: AppModel = None):
        self._model: AppModel = AppModel() if not model else model
        self.updated: Signal = Signal()
    
    def send_update(self) -> None:
        self.updated.send(self._model)
        
    def update_registrant_table(self, registrants: List[Dict[str, Any]]) -> None:
        df = pd.DataFrame(
            registrants, 
            columns=self._model.table.columns,
            # dtype=self._model.table.dtypes,
        )
        df['state'] = df.status
        assert tuple(df.columns) == tuple(self._model.table.columns)
        self._model = self._model.replace(table=df)
        self.updated.send(self._model)

    def set_registration_status(self, id: str, status: str) -> None:
        df = self._model.table
        df.loc[df['id'] == id, 'status'] = status
        df.loc[df['id'] == id, 'state'] = status
        self.registrant_table = df
        assert tuple(df.columns) == tuple(self._model.table.columns)
        self._model = self._model.replace(table=df)
        self.updated.send(self._model)


@dataclass
class Presenter(ListRegistrantPresenter):
    controller: Controller

    def show(self, registrants: List[RegistrantSummary]) -> None:
        self.controller.update_registrant_table(registrants=[r.to_dict() for r in registrants])

    def show_update(self, registrant: RegistrantSummary) -> None:
        self.controller.set_registration_status(id=registrant.id, status=registrant.status)


