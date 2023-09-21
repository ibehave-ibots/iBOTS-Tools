import sys
sys.path.append('..')

import time
from adapters import StreamlitRegistrantPresenter
from app import RegistrantSummary

registrants = [
    RegistrantSummary(
        name="eve",
        email="e@e.com",
        status="approved",
        registered_on="25092023",
        workshop_id="12345",
        id="54321",
        group_name="Prof. Sangee"
    ),
    RegistrantSummary(
        name="adam",
        email="a@a.com",
        status="waitlisted",
        registered_on="29102023",
        workshop_id="7890",
        id="0987",
        group_name="Prof. Bee"
    )
]
presenter = StreamlitRegistrantPresenter()
presenter.show(registrants=registrants)

new = RegistrantSummary(
        name="adam",
        email="a@a.com",
        status="rejected",
        registered_on="29102023",
        workshop_id="7890",
        id="0987",
        group_name="Prof. Bee"
    )

time.sleep(5)
presenter.show_update(registrant=new)

