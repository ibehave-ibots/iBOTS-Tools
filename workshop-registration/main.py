import json
from pprint import pprint



from app import ListRegistrantsApp
from adapters import ConsoleListRegistrantPresenter, PandasListRegistrantPresenter, PPrintListWorkshopPresenter
from app import ListWorkshopsApp, AppModel
from adapters.workshoprepo_zoom import ZoomWorkshopRepo 
from adapters.registrationrepo_zoom import ZoomRegistrationRepo
from external.zoom_api import list_registrants, get_meeting, get_meetings
import os

app = ListWorkshopsApp(
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
app.check_upcoming_workshops()
# pprint(app.model.upcoming_workshops)

# list_registrants_app = ListRegistrantsApp(
#     registration_repo= ZoomRegistrationRepo(
#         list_registrants=list_registrants
#     ), 
#     # presenter=ConsoleListRegistrantPresenter(),
#     presenter=PandasListRegistrantPresenter(),
# )
# list_registrants_app.list_registrants(workshop_id="86061267458")