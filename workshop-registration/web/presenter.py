from __future__ import annotations
from dataclasses import dataclass, field

from typing import List, NamedTuple

import pandas as pd

from web.signal import Signal
from app import ListRegistrantPresenter, RegistrantSummary

class ViewModel(NamedTuple):
    table: pd.DataFrame

@dataclass
class Presenter(ListRegistrantPresenter):
    model: ViewModel = field(default_factory=lambda: ViewModel(table=pd.DataFrame()))
    update: Signal = field(default_factory=Signal)

    def show(self, registrants: List[RegistrantSummary]) -> None:
        regs = [r.to_dict() for r in registrants]            
        df = pd.DataFrame(
            regs, 
            columns=('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state'),
        )
        df.set_index('id', inplace=True)
        df.state = df.status
        self.model = ViewModel(table=df)
        self.update.send(self.model)
        
    def show_update(self, registrant: RegistrantSummary) -> None:
        id = registrant.id
        status=registrant.status
        self.model.table.loc[id, 'status'] = status
        self.model.table.loc[id, 'state'] = status
        self.update.send(self.model)


