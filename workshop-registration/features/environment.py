from functools import partial
import os
import random
from typing import Generator, Literal
from unittest.mock import Mock
from behave import fixture
from dotenv import load_dotenv
import requests
from adapters.registrationrepo_zoom import ZoomRegistrationRepo
from adapters.workshoprepo_zoom import ZoomWorkshopRepo

from app import App, ListWorkshopsPresenter, ListWorkshopsWorkflow, RegistrantWorkflows
from adapters import InMemoryWorkshopRepo, InMemoryRegistrationRepo

from app.list_registrant_presenter import ListRegistrantPresenter, RegistrantSummary
from external.zoom_api import get_meeting, get_meetings, list_group_members, list_registrants
from external.zoom_api.update_registration import zoom_call_update_registration
from external.zoom_api.zoom_oauth import OAuthGetToken

@fixture
def before_scenario(context, scenario):
    if 'change_status_on_zoom_side' in scenario.tags:
        context.meeting_id: Literal['824 9123 9311'] = '824 9123 9311'
        context.access_token = access_token
        context.create_zoom_registrant = partial(create_zoom_registrant, meeting_id=context.meeting_id, access_token=context.access_token())
        mock_oauth_get_token = Mock()
        mock_oauth_get_token.create_access_token.return_value = {"access_token": context.access_token()}
        context.presenter = Mock(ListWorkshopsPresenter)
        context.workshop_repo = ZoomWorkshopRepo(
                                oauth_get_token=mock_oauth_get_token,
                                get_meetings= get_meetings,
                                get_meeting= get_meeting,
                                list_group_members= list_group_members,
                                group_id= os.environ["TEST_GROUP_ID"])
        context.registration_repo = ZoomRegistrationRepo(
                                oauth_get_token = mock_oauth_get_token,
                                zoom_call_update_registration = zoom_call_update_registration,
                                list_registrants=list_registrants
        )
    
    else:
        context.presenter = Mock(ListWorkshopsPresenter)
        context.workshop_repo = InMemoryWorkshopRepo()
        context.registration_repo = InMemoryRegistrationRepo()

    context.list_registrants_presenter = Mock(ListRegistrantPresenter)
    context.app = App(
        workshop_workflow = ListWorkshopsWorkflow(
            workshop_repo=context.workshop_repo, 
            registration_repo=context.registration_repo, 
            presenter=context.presenter,
        ),
        registrant_workflows=RegistrantWorkflows(
                registration_repo=context.registration_repo,
                presenter=context.list_registrants_presenter,
        )
    )


def access_token():
    load_dotenv()
    oauth = OAuthGetToken(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        account_id=os.environ["ACCOUNT_ID"],
    )
    access_data = oauth.create_access_token()
    return access_data["access_token"]



@fixture
def create_zoom_registrant(access_token: str, meeting_id: str, status: Literal["approved","pending","denied"]) -> str:
    fname = 'test'+str(random.randint(1, 100))
    params = {
    "first_name": fname,
    "last_name": 'last_name',
    "email": f'eve{random.randint(1, 100)}@lname.com',
    "custom_questions": [{'title':'Research Group', 'value': 'AG Bashiri'}],
    "status": status
    }
    response = requests.post(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ','')}/registrants",
        headers={"Authorization": f"Bearer {access_token}"},
        json=params,
        )
    response.raise_for_status()
    return response.json()['registrant_id']
    

@fixture
def after_scenario(context, scenario):
     if 'change_status_on_zoom_side' in scenario.tags:
        registrant_id = context.registrant_id
        response = requests.delete(
            url=f"https://api.zoom.us/v2/meetings/{context.meeting_id.replace(' ', '')}/registrants/{registrant_id}",
            headers={"Authorization": f"Bearer {context.access_token()}"},
            )
        response.raise_for_status()