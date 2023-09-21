from typing import List
from app import ListRegistrantPresenter, RegistrantSummary
import streamlit as st
import pandas as pd

class View:

    def __init__(self) -> None:
        st.write("## Registrants")
        self._table = st.empty()

    def update_registrants_table(self, table: pd.DataFrame) -> None:
        self._table.data_editor(
            data=table,
            # width=None,
            # height=None,
            # use_container_width=False,
            # hide_index=None,
            # column_order=None,
            column_config=dict(  # todo: add more specific rendering options
                name=st.column_config.TextColumn(
                    label="Registrant Name",
                    disabled=True,
                ),
                email=st.column_config.TextColumn(
                    label="Email",
                    disabled=True
                ),
                status=st.column_config.SelectboxColumn(
                    label="Status",
                    options=['approved', 'rejected', 'waitlisted'],
                    disabled=True,
                ),
                registered_on=st.column_config.TextColumn(
                    label="Date Registered",
                    disabled=True,
                ),
                group_name=st.column_config.TextColumn(
                    label="Affiliation",
                    disabled=True,
                ),
                workshop_id=st.column_config.TextColumn(
                    label="Workshop ID",
                    disabled=True,
                ),
                id=st.column_config.TextColumn(
                    label="ID",
                    disabled=True,
                ),
            ),
            # num_rows='fixed',
            # key=None,
            # on_change=None,
            # args=None,
            # kwargs=None
        )



class StreamlitRegistrantPresenter(ListRegistrantPresenter):

    def __init__(self, view: View = View()) -> None:
        self.df = None
        self._view = view

    def show(self, registrants: List[RegistrantSummary]) -> None:
        self.df = pd.DataFrame([registrant.to_dict() for registrant in registrants])
        self.df.set_index("id", inplace=True)
        self._view.update_registrants_table(table=self.df)
    
    def show_update(self, registrant: RegistrantSummary) -> None:
        self.df.loc[registrant.id] = pd.Series(registrant.to_dict())
        self._view.update_registrants_table(table=self.df)