import sys
from unittest.mock import Mock
sys.path.append('..')
import os
import streamlit as st
from dotenv import load_dotenv
from app.app import App
from app import RegistrantWorkflows, RegistrationRecord, ListWorkshopsWorkflow, AttendanceWorkflow
from web.presenter import Presenter
from web.view import View
from web.view_model import AppState, ViewModel
from adapters import ZoomRegistrationRepo, ZoomWorkshopRepo
from external.zoom_api import list_registrants, OAuthGetToken, zoom_call_update_registration, list_group_members, get_meeting, get_meetings


if 'initialized' not in st.session_state: 
    load_dotenv()
    oauth_get_token = OAuthGetToken(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        account_id=os.environ["ACCOUNT_ID"],
    )
    workshop_repo = ZoomWorkshopRepo(
        oauth_get_token=oauth_get_token, 
        get_meeting=get_meeting, 
        get_meetings=get_meetings, 
        list_group_members=list_group_members, 
        group_id=os.environ['TEST_GROUP_ID']
        )
    registration_repo = ZoomRegistrationRepo(
        oauth_get_token=oauth_get_token,
        list_registrants=list_registrants,
        zoom_call_update_registration=zoom_call_update_registration
        )
    
    app_state = AppState(data=ViewModel())
    presenter = Presenter(state=app_state)
    view = View(
        controller=App(
            workshop_workflow=Mock(),
            # ListWorkshopsWorkflow(
            #     workshop_repo=workshop_repo, 
            #     registration_repo=registration_repo, 
            #     presenter=presenter),
            registrant_workflows=RegistrantWorkflows(
                registration_repo=registration_repo,
                presenter=presenter,
            ),
            attendance_workflow=Mock(AttendanceWorkflow)
        )
    )
    st.session_state['initialized'] = True
    st.session_state['render'] = lambda: view.render(app_state.data)
    
st.session_state['render']()