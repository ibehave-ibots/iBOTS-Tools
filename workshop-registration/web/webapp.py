from __future__ import annotations

import sys
from typing import List, Tuple
sys.path.append('..')


from app.list_registrant_presenter import ListRegistrantPresenter, RegistrantSummary
from web.wapp import App

from dataclasses import dataclass, field
import pandas as pd
import streamlit as st

class Signal:
    def __init__(self) -> None:
        self._fun = None

    def connect(self, fun) -> None:
        self._fun = fun

    def send(self, *args, **kwargs) -> None:
        self._fun(*args, **kwargs)


@dataclass
class ViewModel:
    app: App
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    columns: Tuple[str, ...] = ('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state')
    update: Signal = field(default_factory=Signal)

    def get_all(self, workshop_id):
        regs = self.app.list_registrants(workshop_id=workshop_id)
        regs = [r.to_dict() for r in regs]            
        self.table = pd.DataFrame(regs, columns=self.columns)
        self.table.set_index('id', inplace=True)
        self.table.state = self.table.status
        self.update.send(self)

    def update_status(self, row: int, status: str):
        reg = self.table.iloc[row]
        registrant = self.app.update_registration_status(registration_id=reg.name, workshop_id=reg['workshop_id'], to_status=status)
        self.table.loc[registrant.id, 'status'] = registrant.status
        self.table.loc[registrant.id, 'state'] = registrant.status
        self.update.send(self)

    

    

@dataclass
class View:
    model: ViewModel

    def __post_init__(self):
        self.model.update.connect(self.render)
        self.render(model=self.model)

    def render(self, model: ViewModel):
        st.button(label="Get Registrants for Workshop 12345", on_click=self._get_button_clicked)
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
                    print('detected update')
                    self.model.update_status(row=i, status=new_status)
                case _:
                    st.write(updated_rows)
        
    def _get_button_clicked(self):
        self.model.get_all(workshop_id='12345')


