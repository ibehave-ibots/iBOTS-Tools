from typing import NamedTuple
from adapters import PPrintListWorkshopPresenter, PandasListRegistrantPresenter
from app import ListWorkshopsWorkflow, ListRegistrantsWorkflow, App
from adapters.workshoprepo_zoom import ZoomWorkshopRepo 
import os
from dotenv import load_dotenv
from adapters.registrationrepo_zoom import ZoomRegistrationRepo
from external.zoom_api import list_registrants, get_meeting, get_meetings
from external.zoom_api import OAuthGetToken

load_dotenv()
oauth = OAuthGetToken(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    account_id=os.environ["ACCOUNT_ID"],
)

app = App(
    workshop_workflow = ListWorkshopsWorkflow(
        workshop_repo =ZoomWorkshopRepo(
            user_id=os.environ['TEST_USER_ID'],
            get_meeting=get_meeting,
            get_meetings=get_meetings,
            oauth_get_token=oauth
        ),
        registration_repo=ZoomRegistrationRepo(
            list_registrants=list_registrants,
            oauth_get_token=oauth
        ),
        presenter=PPrintListWorkshopPresenter(),
    ),
    registrants_workflow= ListRegistrantsWorkflow(
        registration_repo= ZoomRegistrationRepo(
            list_registrants=list_registrants,
            oauth_get_token=oauth
        ), 
        #presenter=ConsoleListRegistrantPresenter(),
        presenter=PandasListRegistrantPresenter(),
    ),
)

app.list_upcoming_workshops()
app.list_registrants(workshop_id="86061267458")
