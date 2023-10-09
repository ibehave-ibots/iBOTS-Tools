from __future__ import annotations

import sys
sys.path.append('..')

from dataclasses import dataclass
import streamlit as st

from app.app import App
from web.presenters import ViewModel



@dataclass
class View:
    """
    The Streamlit View, responible for:
      - rendering the ViewModel in the web browser using Streamlit
      - sending any user interactions out of Streamlit for processing.
    """
    controller: App

    def render(self, model: ViewModel):
        st.button('Get Available Workshop IDs', on_click=self._get_workshops_button_clicked)
        workshop_id = st.selectbox(key='selectbox-workshop-id', label="Workshop IDs: ", options=model.workshop_ids)
        st.button(label=f"Get Waitlisted Registrants", on_click=self._get_button_clicked, disabled=not workshop_id)
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
                    options=['approved', 'rejected', 'waitlisted'],
                    required=True,
                    disabled=False,
                ),
                'state': st.column_config.TextColumn(label='Confirmed State', disabled=True),
            },
            column_order=["name", "email", "group_name", "registered_on", "status", "state", "id", "wokshop_id"]
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
                    print("Approving")
                    self.controller.update_registration_status(registration_id=reg_id, workshop_id=workshop_id, to_status='approved')
                case {"status": 'rejected'}:
                    print("Rejecting")
                    self.controller.update_registration_status(registration_id=reg_id, workshop_id=workshop_id, to_status='rejected')
                case {"status": 'waitlisted'}:
                    self.controller.update_registration_status(registration_id=reg_id, workshop_id=workshop_id, to_status='waitlisted')
        
    def _get_button_clicked(self):
        workshop_id = st.session_state['selectbox-workshop-id']
        if workshop_id:
            self.controller.list_registrants(workshop_id=workshop_id, status='waitlisted')

    def _get_workshops_button_clicked(self):
        self.controller.list_upcoming_workshops()

