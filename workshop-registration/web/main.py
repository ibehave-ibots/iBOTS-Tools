import sys
from unittest.mock import Mock
sys.path.append('..')

import streamlit as st

from app.app import App
from app import WorkshopRepo, RegistrantWorkflows
from web.wapp import ToViewModelListRegistrantPresenter
from web.webapp import View, ViewModel
from web.create_repo import create_reg_repo


if 'initialized' not in st.session_state:
    presenter = ToViewModelListRegistrantPresenter()
    view = View(
        model=ViewModel(
            app=App(
                workshop_workflow=Mock(),
                registrant_workflows=RegistrantWorkflows(
                    registration_repo=create_reg_repo(),
                    presenter=presenter,
                )
            )
        )
    )
    presenter.register(model=view.model)
    st.session_state['initialized'] = True
    