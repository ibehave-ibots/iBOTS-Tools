import sys
sys.path.append('..')

import streamlit as st

from web.wapp import App
from web.webapp import View, PandasModel
from web.create_repo import create_reg_repo


if 'initialized' not in st.session_state:
    view = View(
        model=PandasModel(
            app=App(
                repo=create_reg_repo()
            )
        )
    )
    st.session_state['initialized'] = True
    