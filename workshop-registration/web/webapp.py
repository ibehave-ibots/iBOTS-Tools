from __future__ import annotations

import sys

from web.signal import Signal
sys.path.append('..')

from dataclasses import dataclass, field
import pandas as pd
import streamlit as st

from app.app import App



@dataclass
class ViewModel:
    app: App                              
    _table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    update: Signal = field(default_factory=Signal)

    # List of Registrants
    def request_list_of_registrants(self, workshop_id):
        self.app.list_registrants(workshop_id=workshop_id)

    def get_table(self) -> pd.DataFrame:
        return self._table
    
    def set_table(self, table: pd.DataFrame):
        self._table = table
        self.update.send(self)

    # Registrant Status
    def request_change_registrant_status(self, row: int, status: str):
        reg = self._table.iloc[row]
        self.app.update_registration_status(registration_id=reg.name, workshop_id=reg['workshop_id'], to_status=status)

    def get_registrant_status(self, id: int) -> str:
        return self._table.loc[id, 'status']

    def set_registrant_status(self, id: int, status: str):
        self._table.loc[id, 'status'] = status
        self._table.loc[id, 'state'] = status
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
            model._table, 
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
                    self.model.request_change_registrant_status(row=i, status=new_status)
                case _:
                    st.write(updated_rows)
        
    def _get_button_clicked(self):
        self.model.request_list_of_registrants(workshop_id='12345')


