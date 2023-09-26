from __future__ import annotations

import sys
from typing import Literal
sys.path.append('..')

from dataclasses import dataclass
import streamlit as st

from app.app import App
from web.presenter import ViewModel



@dataclass
class View:
    controller: App

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
            reg = model.table.iloc[idx]
            reg_id = reg['id']
            workshop_id = reg['workshop_id']
            match changes:
                case {"status": 'approved'}:
                    self.controller.update_registration_status(registration_id=reg_id, workshop_id=workshop_id, to_status='approved')
                case {"status": 'rejected'}:
                    self.controller.update_registration_status(registration_id=reg_id, workshop_id=workshop_id, to_status='rejected')
        
    def _get_button_clicked(self, model: ViewModel):
        self.controller.list_registrants(workshop_id='12345')


