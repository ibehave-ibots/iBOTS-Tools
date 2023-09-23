import sys
sys.path.append('..')

import streamlit as st

from unittest.mock import Mock
from app import App, RegistrantWorkflows
from web.webapp import Presenter, View, Model


from web.create_repo import create_reg_repo


if 'initialized' not in st.session_state:
    view = View()
    model = Model(view=view)
    view.on_status_update.connect(model.update_status)

    app = App(
        workshop_workflow=Mock(),
        registrant_workflows=RegistrantWorkflows(
            registration_repo=create_reg_repo(),
            presenter=Presenter(model=model),
        )
    )
    model.on_update_status.connect(app.update_registration_status)

    app.list_registrants(workshop_id="12345")
    st.session_state['initialized'] = True
    