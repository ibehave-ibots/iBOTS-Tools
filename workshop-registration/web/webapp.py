from __future__ import annotations

import sys
sys.path.append('..')

from dataclasses import dataclass, field
import pandas as pd
import streamlit as st

from app.app import App



@dataclass
class ViewModel:
    app: App                              
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    
    def request_list_of_registrants(self, workshop_id):
        self.app.list_registrants(workshop_id=workshop_id)

    def request_change_registrant_status(self, row: int, status: str):
        reg = self.table.iloc[row]
        self.app.update_registration_status(registration_id=reg.name, workshop_id=reg['workshop_id'], to_status=status)
    

@dataclass
class View:

    def render(self, model: ViewModel):
        st.button(label="Get Registrants for Workshop 12345", on_click=lambda: self._get_button_clicked(model))
        st.data_editor(
            model.table, 
            key="data_editor", 
            on_change=lambda: self._data_editor_updated(model),
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

    def _data_editor_updated(self, model: ViewModel):    
        updated_rows = st.session_state['data_editor']['edited_rows']
        assert len(updated_rows) == 1   
        for idx, changes in updated_rows.items():
            match idx, changes:
                case int(i), {"status": str(new_status)}:
                    print('detected update')
                    model.request_change_registrant_status(row=i, status=new_status)
                case _:
                    st.write(updated_rows)
        
    def _get_button_clicked(self, model: ViewModel):
        model.request_list_of_registrants(workshop_id='12345')


