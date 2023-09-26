from __future__ import annotations
from dataclasses import dataclass, field, replace

from typing import Any, Dict, List

import pandas as pd


@dataclass(frozen=True)
class ViewModel:
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(
        columns=('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state'),
        dtype=str,
    ))

    def _replace(self, **kwargs) -> ViewModel:
        return replace(self, **kwargs)

    def update_registrant_table(self, registrants: List[Dict[str, Any]]) -> ViewModel:
        df = pd.DataFrame(
            registrants, 
            columns=self.table.columns,
            # dtype=self._model.table.dtypes,
        )
        df['state'] = df.status
        assert tuple(df.columns) == tuple(self.table.columns)
        new_model = self._replace(table=df)
        return new_model

    def set_registration_status(self, id: str, status: str) -> ViewModel:
        df = self.table.copy()
        df.loc[df['id'] == id, 'status'] = status
        df.loc[df['id'] == id, 'state'] = status
        assert tuple(df.columns) == tuple(self.table.columns)
        return self._replace(table=df)


