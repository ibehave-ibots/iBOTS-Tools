import sys
from unittest.mock import Mock
sys.path.append('..')

import streamlit as st

from app.app import App
from app import RegistrantWorkflows
from web.presenter import Controller, Presenter, AppModel
from web.view import View


from adapters import InMemoryRegistrationRepo
from app.registrationrepo import RegistrationRecord


if 'initialized' not in st.session_state:

    repo = InMemoryRegistrationRepo(
        registrations=[
            RegistrationRecord(
                id="54321",
                workshop_id="12345",
                name="eve",
                email="e@e.com",
                registered_on="25092023",
                custom_questions=[{'value': 'Prof. Sangee'}],
                status='approved',
            ),
            RegistrationRecord(
                id="11111",
                workshop_id="12345",
                name="adam",
                email="a@a.com",
                registered_on="26092023",
                custom_questions=[{'value': 'Prof. Bee'}],
                status='waitlisted',
            ),
        ],
    )

    
    app_state = Controller()
    presenter = Presenter(controller=app_state)
    view = View(
        controller=App(
            workshop_workflow=Mock(),
            registrant_workflows=RegistrantWorkflows(
                registration_repo=repo,
                presenter=presenter,
            )
        )
    )
    app_state.updated.connect(view.render)
    app_state.send_update()
    st.session_state['initialized'] = True
    