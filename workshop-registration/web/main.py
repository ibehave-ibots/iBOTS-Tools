import sys
sys.path.append('..')

import streamlit as st

from unittest.mock import Mock
from app import App, RegistrantWorkflows
from web.webapp import Presenter, View, Model, Controller


from web.create_repo import create_repo


if 'initialized' not in st.session_state:
    view = View()
    model = Model(view=view)
    controller = Controller(model=model)
    app = App(
        workshop_workflow=Mock(),
        registrant_workflows=RegistrantWorkflows(
            registration_repo=create_repo(),
            presenter=Presenter(model=model),
        )
    )
    view.on_status_update.connect(controller.update_status)
    controller.on_update_status.connect(app.update_registration_status)

    app.list_registrants(workshop_id="12345")
    st.session_state['initialized'] = True
    