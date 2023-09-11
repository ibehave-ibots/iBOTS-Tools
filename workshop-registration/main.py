from typing import NamedTuple
from adapters import PPrintListWorkshopPresenter, PandasListRegistrantPresenter
from app import ListWorkshopsWorkflow, ListRegistrantsWorkflow, App
from adapters.workshoprepo_zoom import ZoomWorkshopRepo 
from adapters.registrationrepo_zoom import ZoomRegistrationRepo
from external.zoom_api import list_registrants, get_meeting, get_meetings
import os


app = App(
    workshop_workflow= ListWorkshopsWorkflow(
        workshop_repo=ZoomWorkshopRepo(
            user_id=os.environ['TEST_USER_ID'],
            get_meeting=get_meeting,
            get_meetings=get_meetings,
        ),
        registration_repo=ZoomRegistrationRepo(
            list_registrants=list_registrants,
        ),
        presenter=PPrintListWorkshopPresenter(),
)
,
    registrants_workflow= ListRegistrantsWorkflow(
        registration_repo= ZoomRegistrationRepo(
            list_registrants=list_registrants
        ), 
        #presenter=ConsoleListRegistrantPresenter(),
        presenter=PandasListRegistrantPresenter(),
)


)
app.list_upcoming_workshops()
app.list_registrants(workshop_id="86061267458")