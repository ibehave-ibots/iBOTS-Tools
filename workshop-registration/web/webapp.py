import sys
from typing import List, Tuple
sys.path.append('..')

from app.app import App
from app.list_registrant_presenter import ListRegistrantPresenter, RegistrantSummary


from dataclasses import dataclass, field
import pandas as pd
import streamlit as st


class Presenter(ListRegistrantPresenter):
    def show(self, registrants: List[RegistrantSummary]) -> None:
        model: Model = st.session_state['model']
        regs = []
        for registrant in registrants:
            reg = {
                'id': registrant.id,
                'workshop_id': registrant.workshop_id,
                'name': registrant.name,
                'email': registrant.email,
                'registered_on': registrant.registered_on,
                'group_name': registrant.group_name,
                'status': registrant.status,
                'state': registrant.status,
            }
            regs.append(reg)
        model.set_data(data=regs)

    def show_update(self, registrant: RegistrantSummary) -> None:
        model: Model = st.session_state['model']
        model.update_registrant_status(id=registrant.id, status=registrant.status)


@dataclass
class Model:
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    columns: Tuple[str, ...] = ('id', 'workshop_id', 'name', 'email', 'registered_on', 'group_name', 'status', 'state')

    def set_data(self, data):
        self.table = pd.DataFrame(data, columns=self.columns)
        self.table.set_index('id', inplace=True)

    def get_registrant(self, idx):
        return self.table.loc[idx].to_dict()

    def update_registrant_status(self, id, status):
        self.table.loc[id, 'status'] = status
        self.table.loc[id, 'state'] = status


    
class View:

    def __init__(self, app: App) -> None:
        self.app: App = app

        if not 'model' in st.session_state:
            model = Model()
            st.session_state['model'] = model
            st.session_state['app'] = app
            
            self.app.list_registrants(workshop_id="12345")

    def render(self):
        model: Model = st.session_state['model']
        st.data_editor(
            model.table, 
            key="data_editor", 
            on_change=self.update,
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


    def update(self):    
        model: Model = st.session_state['model']
        updated_rows = st.session_state['data_editor']['edited_rows']
        
        assert len(updated_rows) == 1
        for idx, changes in updated_rows.items():
            match idx, changes:
                case int(i), {"status": str(new_status)}:
                    reg = model.table.iloc[i]
                    reg_id = reg.name
                    self.app.update_registration_status(registration_id=reg_id, workshop_id=reg['workshop_id'], to_status=new_status)

                case _:
                    st.write(updated_rows)






