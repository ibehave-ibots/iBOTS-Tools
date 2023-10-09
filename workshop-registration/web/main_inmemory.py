import sys
from unittest.mock import Mock
sys.path.append('..')

import streamlit as st

from app.app import App
from app import RegistrantWorkflows, RegistrationRecord, AttendanceWorkflow
from web.presenters import RegistrantPresenter
from web.view import View
from web.view_model import AppState, ViewModel
from adapters import InMemoryRegistrationRepo


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

    
    app_state = AppState(data=ViewModel())
    presenter = RegistrantPresenter(state=app_state)
    view = View(
        controller=App(
            workshop_workflow=Mock(),
            registrant_workflows=RegistrantWorkflows(
                registration_repo=repo,
                presenter=presenter,
            ),
            attendance_workflow=Mock(AttendanceWorkflow)
        )
    )
    st.session_state['initialized'] = True
    st.session_state['render'] = lambda: view.render(app_state.data)
    
st.session_state['render']()