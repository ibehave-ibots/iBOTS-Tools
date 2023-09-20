from typing import List
from app import ListRegistrantPresenter, RegistrantSummary
import streamlit as st
import pandas as pd

class StreamlitRegistrantPresenter(ListRegistrantPresenter):
    def show(self, registrants: List[RegistrantSummary]) -> None:
        df = pd.DataFrame([registrant._asdict() for registrant in registrants])
        df.set_index("id", inplace=True)
        st.write(df) 
    
    def show_update(self, registrant: RegistrantSummary) -> None:
        df = pd.DataFrame([registrant._asdict()])
        df.set_index("id", inplace=True)
        st.write(df)