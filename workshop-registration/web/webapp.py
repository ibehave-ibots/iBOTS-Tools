from __future__ import annotations
from abc import ABC, abstractmethod

import sys
from typing import List, Tuple
sys.path.append('..')

from dataclasses import dataclass, field
import pandas as pd
import streamlit as st

from app.app import App



class Signal:
    def __init__(self) -> None:
        self._fun = None

    def connect(self, fun) -> None:
        self._fun = fun

    def send(self, *args, **kwargs) -> None:
        self._fun(*args, **kwargs)


class IView(ABC):

    @abstractmethod
    def render(self, model: ViewModel) -> None:
        ...


@dataclass
class ViewModel:
    app: App
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    update: Signal = field(default_factory=Signal)

    def get_all(self, workshop_id):
        self.app.list_registrants(workshop_id=workshop_id)

    def update_table(self, table: pd.DataFrame):
        self.table = table
        self.update.send(self)

    def change_status(self, row: int, status: str):
        reg = self.table.iloc[row]
        self.app.update_registration_status(registration_id=reg.name, workshop_id=reg['workshop_id'], to_status=status)

    def update_registrant(self, id, status):
        self.table.loc[id, 'status'] = status
        self.table.loc[id, 'state'] = status
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
                    self.model.change_status(row=i, status=new_status)
                case _:
                    st.write(updated_rows)
        
    def _get_button_clicked(self):
        self.model.get_all(workshop_id='12345')


