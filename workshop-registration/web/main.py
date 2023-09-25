import sys
from unittest.mock import Mock
sys.path.append('..')

import streamlit as st

from app.app import App
from app import RegistrantWorkflows
from web.presenter import Presenter
from web.webapp import View
from web.create_repo import create_reg_repo


if 'initialized' not in st.session_state:
    presenter = Presenter()
    view = View(
        controller=App(
            workshop_workflow=Mock(),
            registrant_workflows=RegistrantWorkflows(
                registration_repo=create_reg_repo(),
                presenter=presenter,
            )
        )
    )
    presenter.update.connect(view.render)
    view.render(presenter.model)
    st.session_state['initialized'] = True
    