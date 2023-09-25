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
        table = pd.DataFrame(
            regs, 
            columns=('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state'),
        )
        table.set_index('id', inplace=True)
        table.state = table.status
        self.model.update_table(table=table)
        
    def show_update(self, registrant: RegistrantSummary) -> None:
        self.model.update_registrant(id=registrant.id, status=registrant.status)


