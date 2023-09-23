from __future__ import annotations

import sys
from typing import List, Tuple
sys.path.append('..')

from app.app import App
from app.list_registrant_presenter import ListRegistrantPresenter, RegistrantSummary


from dataclasses import dataclass, field
import pandas as pd
import streamlit as st

@dataclass
class Presenter(ListRegistrantPresenter):
    model: Model

    def show(self, registrants: List[RegistrantSummary]) -> None:
        model = self.model
        regs = [r.to_dict() for r in registrants]            
        model.set_data(data=regs)

    def show_update(self, registrant: RegistrantSummary) -> None:
        model = self.model
        model.update_registrant_status(id=registrant.id, status=registrant.status)
        
        

@dataclass
class Model:
    view: View
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    columns: Tuple[str, ...] = ('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state')

    def set_data(self, data):
        self.table = pd.DataFrame(data, columns=self.columns)
        self.table.set_index('id', inplace=True)
        self.table.state = self.table.status
        self.view.render(model=self)

    def update_registrant_status(self, id, status):
        self.table.loc[id, 'status'] = status
        self.table.loc[id, 'state'] = status
        self.view.render(model=self)


class Signal:
    def __init__(self) -> None:
        self._fun = None

    def connect(self, fun) -> None:
        self._fun = fun

    def send(self, *args, **kwargs) -> None:
        self._fun(*args, **kwargs)








@dataclass
class View:
    on_status_update: Signal = Signal()

    def render(self, model: Model):
        st.data_editor(
            model.table, 
            key="data_editor", 
            on_change=self._data_editor_updated,
            column_config={
                'id': st.column_config.TextColumn(label='ID', disabled=True),
                'workshop_id': st.column_config.TextColumn(label='Workshop ID', disabled=True),
                'name': st.column_config.TextColumn(label='Name', disabled=True),
                'email': st.column_config.TextColumn(label='Email', disabled=True),
                'registered_on': st.column_config.TextColumn(label='Date', disabled=True),
                'group_name': st.column_config.TextColumn(label='Group', disabled=True),
                'status': st.column_config.SelectboxColumn(
                    label='Status', 
                    options=['accepted', 'rejected', 'waitlisted'],
                    required=True,
                    disabled=False,
                ),
                'state': st.column_config.TextColumn(label='Confirmed State', disabled=True),
            }
        )


    def _data_editor_updated(self):    
        updated_rows = st.session_state['data_editor']['edited_rows']
        assert len(updated_rows) == 1   
        for idx, changes in updated_rows.items():
            match idx, changes:
                case int(i), {"status": str(new_status)}:
                    self.on_status_update.send(row=i, status=new_status)
                case _:
                    st.write(updated_rows)
        


@dataclass
class Controller:
    model: Model
    app: App

    def update_status(self, row: int, status: str):
        reg = self.model.table.iloc[row]
        self.app.update_registration_status(registration_id=reg.name, workshop_id=reg['workshop_id'], to_status=status)


    


