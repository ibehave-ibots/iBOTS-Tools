from app import App, AppModel
from adapters.workshoprepo_zoom import ZoomWorkshopRepo 
from adapters.registrationrepo_zoom import ZoomRegistrationRepo
from external.zoom_api import list_registrants, get_meeting, get_meetings
import os

app = App(
    workshop_repo=ZoomWorkshopRepo(
        user_id=os.environ['TEST_USER_ID'],
        get_meeting=get_meeting,
        get_meetings=get_meetings,
    ),
    registration_repo=ZoomRegistrationRepo(
        list_registrants=list_registrants
    ),
    model=AppModel(),
)

app.check_upcoming_workshops()
print(app.model.upcoming_workshops)