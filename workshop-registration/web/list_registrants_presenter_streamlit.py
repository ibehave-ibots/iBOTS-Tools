from typing import List
from app import ListRegistrantPresenter, RegistrantSummary
import streamlit as st
import pandas as pd

class StreamlitRegistrantPresenter(ListRegistrantPresenter):

    def __init__(self) -> None:
        self.df = None
        self.df_widget = st.empty()

    def show(self, registrants: List[RegistrantSummary]) -> None:
        self.df = pd.DataFrame([registrant._asdict() for registrant in registrants])
        self.df.set_index("id", inplace=True)
        self.df_widget.write(self.df) 
    
    def show_update(self, registrant: RegistrantSummary) -> None:
        self.df.loc[registrant.id] = pd.Series(registrant._asdict())
        self.df_widget.write(self.df)