from __future__ import annotations

from typing import List

import pandas as pd

from app import ListRegistrantPresenter, RegistrantSummary
from web.webapp import ViewModel

class ToViewModelListRegistrantPresenter(ListRegistrantPresenter):
    model: ViewModel

    def register(self, model: ViewModel):
        self.model = model

    def show(self, registrants: List[RegistrantSummary]) -> None:
        regs = [r.to_dict() for r in registrants]            
        df = pd.DataFrame(
            regs, 
            columns=('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state'),
        )
        df.set_index('id', inplace=True)
        df.state = df.status
        self.model.set_table(table=df)
        
    def show_update(self, registrant: RegistrantSummary) -> None:
        self.model.set_registrant_status(id=registrant.id, status=registrant.status)


