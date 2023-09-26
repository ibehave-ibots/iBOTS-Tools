from __future__ import annotations
from dataclasses import dataclass, field, replace

from typing import Any, Dict, List

import pandas as pd

from web.signal import Signal

@dataclass(frozen=True)
class AppModel:
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(
        columns=('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state'),
        dtype=str,
    ))

    def _replace(self, **kwargs) -> AppModel:
        return replace(self, **kwargs)

    def update_registrant_table(self, registrants: List[Dict[str, Any]]) -> AppModel:
        df = pd.DataFrame(
            registrants, 
            columns=self.table.columns,
            # dtype=self._model.table.dtypes,
        )
        df['state'] = df.status
        assert tuple(df.columns) == tuple(self.table.columns)
        new_model = self._replace(table=df)
        return new_model

    def set_registration_status(self, id: str, status: str) -> AppModel:
        df = self.table
        df.loc[df['id'] == id, 'status'] = status
        df.loc[df['id'] == id, 'state'] = status
        assert tuple(df.columns) == tuple(self.table.columns)
        return self._replace(table=df)

class AppState:
    updated: Signal

    def __init__(self, model: AppModel = None):
        self._model: AppModel = AppModel() if not model else model
        self.updated: Signal = Signal()

    def send_all(self) -> None:
        self.updated.send(self._model)

    @property
    def model(self) -> AppModel:
        return self._model
    
    @model.setter
    def model(self, value: AppModel) -> None:
        self._model = value
        self.updated.send(self._model)
