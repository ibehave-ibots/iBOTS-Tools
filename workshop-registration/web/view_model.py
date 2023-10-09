from __future__ import annotations
from dataclasses import dataclass, field, replace

from typing import Any, Dict, List, Sequence, Tuple, TypedDict

import pandas as pd

@dataclass
class AppState:
    data: ViewModel
    

class WorkshopSummaryRecord(TypedDict):
    id: str


@dataclass(frozen=True)
class ViewModel:
    """
    The ViewModel, responsible for:
      - holding all the data that should be rendered for the user
      - handling any modifications to its data and verifying that it is correct.

    The ViewModel should be considered immutable by all other entities, so that fails don't result in partially-updated invalid ViewModels.
    """
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(
        columns=('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state'),
        dtype=str,
    ))
    workshop_ids: Tuple[str, ...] = ()
    workshop_summaries_table: pd.DataFrame = field(default_factory=pd.DataFrame)

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

    def set_workshop_ids(self, ids: Sequence[str]) -> ViewModel:
        return self._replace(workshop_ids=tuple(ids))

    def set_workshop_summary_table(self, summaries: List[Dict]) -> ViewModel:
        return self._replace(
            workshop_summaries_table=pd.DataFrame(summaries),
        )