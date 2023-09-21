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
            # column_config=dict(  # todo: add more specific rendering options
            #     name=,
            #     email: str
            #     status: Literal['approved','waitlisted','rejected']
            #     registered_on: str
            #     group_name: str
            #     workshop_id: str
            #     id: str = field(default_factory=lambda: str(uuid4()))
            # ),
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